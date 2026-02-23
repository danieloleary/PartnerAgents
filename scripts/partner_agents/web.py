#!/usr/bin/env python3
"""
PartnerOS Web Interface
A beautiful web UI for the multi-agent partner team.
"""

import os
import sys
import re

# Import fastapi BEFORE adding scripts to path (to avoid local test shim)
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import httpx

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import uvicorn

from partner_agents.drivers import (
    DanAgent,
    ArchitectAgent,
    StrategistAgent,
    EngineAgent,
    SparkAgent,
    ChampionAgent,
    BuilderAgent,
)
from partner_agents import Orchestrator
from partner_agents import partner_state
from partner_agents import router
from partner_agents import document_generator
from partner_agents import chat_orchestrator

# In-memory rate limiting
import time
from collections import deque

rate_limit_store = {}
response_cache = {}

# Cache settings
CACHE_ENABLED = True
CACHE_TTL_SECONDS = 300


def check_rate_limit(ip: str, max_requests: int = 20, window_seconds: int = 60) -> bool:
    """Simple rate limiter using deque for efficient pruning."""
    now = time.time()

    # Defensive: prevent memory exhaustion if store grows too large
    if len(rate_limit_store) > 1000:
        # Clear entries older than the window
        expired_ips = [
            ip_key
            for ip_key, times in rate_limit_store.items()
            if not times or (now - times[-1] > window_seconds)
        ]
        for ip_key in expired_ips:
            del rate_limit_store[ip_key]

    if ip not in rate_limit_store:
        rate_limit_store[ip] = deque()

    # Efficiently remove old requests from the left
    window_start = now - window_seconds
    while rate_limit_store[ip] and rate_limit_store[ip][0] < window_start:
        rate_limit_store[ip].popleft()

    if len(rate_limit_store[ip]) >= max_requests:
        return False

    rate_limit_store[ip].append(now)
    return True


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan and shared resources."""
    # Initialize shared client
    app.state.http_client = httpx.AsyncClient()
    yield
    # Clean up
    await app.state.http_client.aclose()


app = FastAPI(title="PartnerOS", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Initialize agents
agents = {
    "dan": DanAgent(),
    "architect": ArchitectAgent(),
    "strategist": StrategistAgent(),
    "engine": EngineAgent(),
    "spark": SparkAgent(),
    "champion": ChampionAgent(),
    "builder": BuilderAgent(),
}

orchestrator = Orchestrator()
for name, agent in agents.items():
    orchestrator.register_driver(agent)


@app.get("/", response_class=HTMLResponse)
async def home():
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PartnerOS</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dompurify@3.0.6/dist/purify.min.js"></script>
    <!-- Inline critical CSS as fallback if CDN fails -->
    <style>
        *,*::before,*::after{box-sizing:border-box}:root{--bg:#0f172a;--bg2:#1e293b;--text:#f8fafc;--text2:#94a3b8}.bg-gradient-to-r{background:linear-gradient(to right)}.text-white{color:#fff}.min-h-screen{min-height:100vh}.max-w-6xl{max-width:72rem}.mx-auto{margin-left:auto;margin-right:auto}.px-4{padding-left:1rem;padding-right:1rem}.py-8{padding-top:2rem;padding-bottom:2rem}.text-center{text-align:center}.mb-6{margin-bottom:1.5rem}.mb-2{margin-bottom:.5rem}.gap-3{gap:.75rem}.flex{display:flex}.items-center{align-items:center}.justify-center{justify-content:center}.rounded-full{border-radius:9999px}.rounded-xl{border-radius:.75rem}.rounded-lg{border-radius:.5rem}.bg-slate-700{background:#334155}.bg-slate-800{background:#1e293b}.bg-cyan-500{background:#06b6d4}.bg-purple-500{background:#a855f7}.bg-green-500{background:#22c55e}.bg-emerald-500{background:#10b981}.bg-yellow-600{background:#ca8a04}.bg-orange-600{background:#ea580c}.bg-gray-400{background:#9ca3af}.text-3xl{font-size:1.875rem}.text-xl{font-size:1.25rem}.text-sm{font-size:.875rem}.text-xs{font-size:.75rem}.font-bold{font-weight:700}.font-semibold{font-weight:600}.text-transparent{color:transparent}.bg-clip-text{-webkit-background-clip:text;background-clip:text}.from-cyan-400{--tw-gradient-from:#22d3ee;--tw-gradient-stops:var(--tw-gradient-from),var(--tw-gradient-to,rgba(34,211,238,0))}.to-purple-500{--tw-gradient-to:#a855f7}.from-green-500{--tw-gradient-from:#22c55e;--tw-gradient-stops:var(--tw-gradient-from),var(--tw-gradient-to,rgba(34,197,94,0))}.to-emerald-500{--tw-gradient-to:#10b981}.from-cyan-500{--tw-gradient-from:#06b6d4;--tw-gradient-stops:var(--tw-gradient-from),var(--tw-gradient-to,rgba(6,182,212,0))}.grid{display:grid}.grid-cols-2{grid-template-columns:repeat(2,minmax(0,1fr))}.gap-4{gap:1rem}.sm\:text-5xl{font-size:3rem}@media (min-width:640px){.sm\:text-5xl{font-size:3rem}}input,textarea{width:100%;background:#1e293b;border:1px solid #334155;color:#fff;padding:.75rem;border-radius:.5rem;outline:none}input:focus,textarea:focus{border-color:#06b6d4}button{background:linear-gradient(to right,#06b6d4,#a855f7);border:none;color:#fff;padding:.75rem 1.5rem;border-radius:.5rem;cursor:pointer;font-weight:600;transition:opacity .2s}button:hover{opacity:.9}button:disabled{opacity:.5;cursor:not-allowed}.max-w-lg{max-width:32rem}.w-8{width:2rem}.h-8{height:2rem}.flex-shrink-0{flex-shrink:0}.overflow-auto{overflow:auto}.border{border-width:1px}.border-slate-700{border-color:#334155}.bg-slate-700\/50{background:rgba(51,65,85,.5)}.bg-slate-800\/50{background:rgba(30,41,59,.5)}.text-slate-400{color:#94a3b8}.text-slate-500{color:#64748b}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}.px-2{padding-left:.5rem;padding-right:.5rem}.py-1{padding-top:.25rem;padding-bottom:.25rem}.bg-gradient-to-r{background:linear-gradient(to right,var(--tw-gradient-stops))}.gradient-bg{background:linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#0f172a 100%)}body{background:#0f172a;color:#f8fafc}
    </style>
    <script>
    // Fallback: load Tailwind CSS with integrity check
    (function() {
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdn.tailwindcss.com';
        link.onerror = function() { console.log('CDN failed, using inline styles'); };
        document.head.appendChild(link);
    })();
    </script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        .gradient-bg {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        }
        .agent-card { transition: all 0.2s ease; }
        .agent-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.3); }
        .typing-indicator span {
            animation: bounce 1.4s infinite ease-in-out both;
        }
        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        .message-enter { animation: slideIn 0.3s ease; }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* Markdown styling */
        .markdown-body { font-size: 0.875rem; line-height: 1.6; }
        .markdown-body h1, .markdown-body h2, .markdown-body h3 { font-weight: 600; margin: 1rem 0 0.5rem; color: #fff; }
        .markdown-body h1 { font-size: 1.25rem; }
        .markdown-body h2 { font-size: 1.1rem; }
        .markdown-body h3 { font-size: 1rem; }
        .markdown-body p { margin: 0.5rem 0; }
        .markdown-body ul, .markdown-body ol { margin: 0.5rem 0; padding-left: 1.5rem; }
        .markdown-body li { margin: 0.25rem 0; }
        .markdown-body table { width: 100%; border-collapse: collapse; margin: 0.75rem 0; font-size: 0.8rem; }
        .markdown-body th, .markdown-body td { border: 1px solid #475569; padding: 0.5rem; text-align: left; }
        .markdown-body th { background: #334155; }
        .markdown-body code { background: #334155; padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.8rem; }
        .markdown-body pre { background: #334155; padding: 0.75rem; border-radius: 0.5rem; overflow-x: auto; margin: 0.5rem 0; }
        .markdown-body pre code { background: none; padding: 0; }
        .markdown-body blockquote { border-left: 3px solid #06b6d4; padding-left: 0.75rem; margin: 0.5rem 0; color: #94a3b8; }
        .markdown-body strong { color: #fff; font-weight: 600; }
        .markdown-body a { color: #22d3ee; text-decoration: underline; }
        .markdown-body hr { border: none; border-top: 1px solid #475569; margin: 1rem 0; }
    </style>
    <style>
        /* ChatGPT-like styles */
        html, body { margin: 0; padding: 0; height: 100%; }
        .chatgpt-container { 
            display: flex; 
            height: 100vh; 
            background: #171717; 
        }
        .chatgpt-sidebar {
            width: 260px; 
            background: #202123; 
            padding: 10px; 
            display: flex; 
            flex-direction: column;
            border-right: 1px solid #2e2e2e;
        }
        .chatgpt-main { 
            flex: 1; 
            display: flex; 
            flex-direction: column; 
            background: #343541;
        }
        .chatgpt-messages { 
            flex: 1; 
            overflow-y: auto; 
            padding: 20px;
        }
        .chatgpt-input-area { 
            padding: 20px; 
            background: #343541;
        }
        .chatgpt-input-wrapper {
            max-width: 768px;
            margin: 0 auto;
            position: relative;
        }
        .chatgpt-input {
            width: 100%;
            background: #40414f;
            border: none;
            border-radius: 12px;
            color: #fff;
            padding: 14px 50px 14px 16px;
            font-size: 16px;
            resize: none;
            outline: none;
        }
        .chatgpt-input:focus { box-shadow: 0 0 0 2px #10a37f; }
        .chatgpt-send {
            position: absolute;
            right: 12px;
            bottom: 10px;
            background: #10a37f;
            border: none;
            border-radius: 6px;
            color: #fff;
            padding: 6px 12px;
            cursor: pointer;
            font-size: 14px;
        }
        .chatgpt-send:hover { background: #0d8a6e; }
        .chatgpt-message {
            display: flex;
            padding: 24px 0;
            border-bottom: 1px solid #2e2e2e;
        }
        .chatgpt-message-user { background: #5436da; padding: 14px 16px; border-radius: 12px; }
        .chatgpt-message-assistant { padding: 14px 16px; border-radius: 12px; }
        .chatgpt-avatar {
            width: 30px;
            height: 30px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 16px;
            flex-shrink: 0;
        }
        .chatgpt-avatar-user { background: #5436da; }
        .chatgpt-avatar-assistant { background: #10a37f; }
        .chatgpt-content { 
            max-width: 768px; 
            line-height: 1.6;
        }
        .chatgpt-content p { margin: 0 0 12px 0; }
        .chatgpt-welcome {
            text-align: center;
            padding: 40px 20px;
            color: #8e8ea0;
        }
        .chatgpt-welcome h1 { color: #fff; font-size: 32px; margin: 0 0 16px 0; }
        .chatgpt-welcome-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            max-width: 600px;
            margin: 0 auto;
        }
        .chatgpt-welcome-card {
            background: #2e2e2e;
            border-radius: 8px;
            padding: 16px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .chatgpt-welcome-card:hover { background: #3e3e3e; }
        .chatgpt-welcome-card h3 { color: #fff; font-size: 14px; margin: 0 0 4px 0; }
        .chatgpt-welcome-card p { color: #8e8ea0; font-size: 12px; margin: 0; }
        .chatgpt-settings-btn {
            background: #007acc;
            border: none;
            border-radius: 8px;
            color: #fff;
            padding: 12px;
            text-align: left;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: auto;
        }
        .chatgpt-settings-modal {
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
        }
        .chatgpt-settings-content {
            background: #202123;
            border-radius: 12px;
            padding: 24px;
            width: 400px;
            max-width: 90vw;
        }
        .chatgpt-settings-content h2 { color: #fff; margin: 0 0 20px 0; }
        .chatgpt-settings-content label { display: block; color: #8e8ea0; margin-bottom: 8px; font-size: 14px; }
        .chatgpt-settings-content input, .chatgpt-settings-content select {
            width: 100%;
            background: #2e2e2e;
            border: 1px solid #2e2e2e;
            border-radius: 8px;
            color: #fff;
            padding: 10px;
            margin-bottom: 16px;
            font-size: 14px;
        }
        .chatgpt-settings-content button {
            background: #10a37f;
            border: none;
            border-radius: 8px;
            color: #fff;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 14px;
        }
        .chatgpt-typing {
            display: flex;
            padding: 24px 0;
            align-items: center;
        }
        .chatgpt-typing-dot {
            width: 8px;
            height: 8px;
            background: #8e8ea0;
            border-radius: 50%;
            margin-right: 4px;
            animation: typing 1.4s infinite;
        }
        .chatgpt-typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .chatgpt-typing-dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-4px); }
        }
    </style>
</head>
<body>
    <div class="chatgpt-container">
        <!-- Sidebar -->
        <div class="chatgpt-sidebar">
            <button class="chatgpt-settings-btn" onclick="showSettings()">
                ⚙️ Settings
            </button>
        </div>
        
        <!-- Main Chat -->
        <div class="chatgpt-main">
            <div class="chatgpt-messages" id="messages">
                <div class="chatgpt-welcome" id="welcome">
                    <h1>PartnerOS</h1>
                    <p>Your AI partner team. Try these:</p>
                    <div class="chatgpt-welcome-grid">
                        <div class="chatgpt-welcome-card" onclick="sendMessage('onboard Auror')">
                            <h3>Onboard Partner</h3>
                            <p>Start onboarding a new partner</p>
                        </div>
                        <div class="chatgpt-welcome-card" onclick="sendMessage('status of Auror')">
                            <h3>Check Status</h3>
                            <p>See where things stand</p>
                        </div>
                        <div class="chatgpt-welcome-card" onclick="sendMessage('launch campaign for Auror')">
                            <h3>Launch Campaign</h3>
                            <p>Start a co-marketing campaign</p>
                        </div>
                        <div class="chatgpt-welcome-card" onclick="sendMessage('register a deal for Auror, $50000')">
                            <h3>Register Deal</h3>
                            <p>Record a new deal</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="chatgpt-input-area">
                <div class="chatgpt-input-wrapper">
                    <textarea id="messageInput" class="chatgpt-input" placeholder="Message PartnerOS..." rows="1" onkeydown="if(event.key==='Enter' && !event.shiftKey) { event.preventDefault(); sendMessage(); }"></textarea>
                    <button class="chatgpt-send" onclick="sendMessage()">↑</button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Settings Modal -->
    <div id="settingsModal" class="chatgpt-settings-modal hidden">
        <div class="chatgpt-settings-content">
            <h2>Settings</h2>
            <label>OpenRouter API Key</label>
            <input id="apiKey" type="password" placeholder="sk-or-...">
            <label>Model</label>
            <select id="modelSelect">
                <option value="openai/gpt-4o-mini">GPT-4o Mini</option>
                <option value="openai/gpt-4o">GPT-4o</option>
                <option value="anthropic/claude-3.5-sonnet">Claude 3.5 Sonnet</option>
                <option value="anthropic/claude-3-haiku">Claude 3 Haiku</option>
            </select>
            <button onclick="saveSettings()">Save</button>
        </div>
    </div>

    <script>
        const escapeHTML = (str) => String(str).replace(/[&<>"']/g, m => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        })[m]);

        // API key should be provided by the user at runtime when needed
        let apiKey = getApiKey();
        
        // Helper to escape quotes for onclick handlers
        const escapeQuotes = (str) => String(str).replace(/'/g, "'\\\\''");

        async function sendMessage(text) {
            const input = document.getElementById('messageInput');
            const btn = document.getElementById('sendBtn');
            const message = text || input.value.trim();
            if (!message) return;
            
            // Get fresh API key from localStorage in case settings were just saved
            apiKey = getApiKey();
            
            input.value = '';
            input.disabled = true;
            btn.disabled = true;
            
            // Add user message
            addMessage(message, 'user');
            
            // Show typing
            showTyping();
            
            // Get settings from localStorage
            const model = localStorage.getItem('partneros_model') || 'openai/gpt-4o-mini';
            const cacheEnabled = localStorage.getItem('partneros_cache') !== 'false';
            
            try {
                console.log('Sending message:', message, 'API key:', apiKey ? 'present' : 'missing', 'model:', model);
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        message: message, 
                        apiKey: apiKey || '',
                        model: model,
                        cache: cacheEnabled
                    })
                });
                
                console.log('Response status:', response.status);
                const data = await response.json();
                console.log('Response data:', data);
                hideTyping();
                
                // Handle rate limiting response
                if (data.rate_limited) {
                    addMessage('⚠️ Too many requests. Please wait a moment before sending another message.', 'assistant');
                } else {
                    addMessage(data.response, 'assistant', data.agent);
                }
            } catch (e) {
                console.error('Error:', e);
                hideTyping();
                addMessage('⚠️ Something went wrong. Please try again or refresh the page.', 'assistant');
            } finally {
                input.disabled = false;
                btn.disabled = false;
                input.focus();
            }
        }
        
        function addMessage(text, role, agent = null) {
            const container = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = 'message-enter flex gap-3';
            
            if (role === 'user') {
                div.innerHTML = `
                    <div role="img" aria-label="User" class="w-8 h-8 rounded-full bg-gradient-to-r from-green-500 to-emerald-500 flex items-center justify-center flex-shrink-0">👤</div>
                    <div class="bg-slate-700/50 rounded-xl p-4 max-w-lg">${escapeHTML(text)}</div>
                `;
            } else {
                const emoji = agent === 'ARCHITECT' ? '🏗️' : 
                              agent === 'ENGINE' ? '⚙️' : 
                              agent === 'SPARK' ? '✨' : 
                              agent === 'CHAMPION' ? '🏆' : 
                              agent === 'BUILDER' ? '🔧' : 
                              agent === 'STRATEGIST' ? '🎯' : '👑';
                const agentName = agent || 'Assistant';
                // Render Markdown for assistant messages
                let renderedContent = text;
                if (typeof marked !== 'undefined') {
                    try {
                        renderedContent = marked.parse(text);
                        // Sanitize the HTML output from marked to prevent XSS
                        if (typeof DOMPurify !== 'undefined') {
                            renderedContent = DOMPurify.sanitize(renderedContent);
                        }
                    } catch (e) {
                        console.warn('Markdown parse error:', e);
                    }
                }
                div.innerHTML = `
                    <div role="img" aria-label="${agentName}" class="w-8 h-8 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center flex-shrink-0">${emoji}</div>
                    <div class="bg-slate-700/50 rounded-xl p-4 max-w-lg markdown-body">
                        <span class="sr-only">${agentName}: </span>
                        ${renderedContent}
                    </div>
                `;
            }
            
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
        
        function showTyping() {
            const container = document.getElementById('messages');
            const div = document.createElement('div');
            div.id = 'typing';
            div.className = 'message-enter flex gap-3';
            div.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center flex-shrink-0">🤖</div>
                <div class="bg-slate-700/50 rounded-xl p-4">
                    <div class="typing-indicator flex gap-1">
                        <span class="w-2 h-2 bg-slate-400 rounded-full"></span>
                        <span class="w-2 h-2 bg-slate-400 rounded-full"></span>
                        <span class="w-2 h-2 bg-slate-400 rounded-full"></span>
                    </div>
                </div>
            `;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
        
        function hideTyping() {
            const typing = document.getElementById('typing');
            if (typing) typing.remove();
        }
        
        // Settings
        function showSettings() {
            document.getElementById('settingsModal').classList.remove('hidden');
            // Load saved settings from localStorage
            const savedKey = localStorage.getItem('partneros_api_key');
            const savedModel = localStorage.getItem('partneros_model') || 'openai/gpt-4o-mini';
            const savedCache = localStorage.getItem('partneros_cache') !== 'false';
            if (savedKey) document.getElementById('apiKey').value = savedKey;
            document.getElementById('modelSelect').value = savedModel;
            document.getElementById('enableCache').checked = savedCache;
        }
        
        function hideSettings() {
            document.getElementById('settingsModal').classList.add('hidden');
        }
        
        function saveSettings() {
            const apiKey = document.getElementById('apiKey').value;
            const model = document.getElementById('modelSelect').value;
            const cache = document.getElementById('enableCache').checked;
            localStorage.setItem('partneros_api_key', apiKey);
            localStorage.setItem('partneros_model', model);
            localStorage.setItem('partneros_cache', cache);
            hideSettings();
            alert('Settings saved!');
        }
        
        function getApiKey() {
            return localStorage.getItem('partneros_api_key') || '';
        }
        
        // Keyboard shortcuts
        document.getElementById('messageInput').addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>"""


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    api_key = data.get("apiKey", "") or os.environ.get("OPENROUTER_API_KEY", "")
    model = data.get("model", "openai/gpt-4o-mini")
    use_cache = data.get("cache", True)

    # Input sanitization - prevent injection
    if not user_message or len(user_message.strip()) == 0:
        return JSONResponse({"response": "Please enter a message.", "agent": "system"})

    # Limit message length to prevent abuse
    if len(user_message) > 5000:
        return JSONResponse(
            {
                "response": "Message too long. Please limit to 5000 characters.",
                "agent": "system",
            }
        )

    # Sanitize: remove potentially dangerous HTML tags
    sanitized = re.sub(r"<[^>]*?>", "", user_message)

    # Rate limiting check
    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_ip):
        return JSONResponse(
            {
                "response": "⚠️ Too many requests. Please wait a moment and try again.",
                "agent": "system",
                "rate_limited": True,
            },
            status_code=429,
        )

    # Route to document generation if detected (works without API key!)
    # This runs FIRST - keyword-based routing doesn't need LLM
    try:
        # Use router to detect document intents
        router_instance = router.Router()

        # Get context for routing (existing partners)
        context = {"partners": partner_state.list_partners()}

        # Route the message
        route_result = await router_instance.route(sanitized, context)

        # Check if this is a document request
        if route_result.is_document_request and route_result.intents:
            intent = route_result.intents[0]

            # Get partner name from entities
            partner_name = intent.entities.get("partner_name")

            if not partner_name:
                # Ask for partner name
                return JSONResponse(
                    {
                        "response": "I'd be happy to create that document! What's the partner company name?",
                        "agent": "system",
                        "awaiting_field": "partner_name",
                    }
                )

            # Create the partner if they don't exist
            partner = partner_state.get_partner(partner_name)
            if not partner:
                partner = partner_state.add_partner(
                    name=partner_name,
                    tier=intent.entities.get("tier", "Bronze"),
                )

            # Generate the document
            doc_result = document_generator.create_document(
                doc_type=intent.name,
                partner_name=partner_name,
                fields=intent.entities,
            )

            if doc_result:
                # Track in partner state
                partner_state.add_document(
                    partner_name=partner_name,
                    doc_type=intent.name,
                    template=doc_result["template"],
                    file_path=doc_result["path"],
                    fields=doc_result["fields"],
                    status="draft",
                )

                return JSONResponse(
                    {
                        "response": f"✅ Created **{intent.name.upper()}** for **{partner_name}**!\n\n"
                        f"Document saved to: `{doc_result['relative_path']}`\n\n"
                        f"The partner has been added to your dashboard.",
                        "agent": "engine",
                        "document": {
                            "type": intent.name,
                            "partner": partner_name,
                            "path": doc_result["relative_path"],
                        },
                    }
                )
            else:
                return JSONResponse(
                    {
                        "response": f"I understood you want a {intent.name}, but couldn't generate it. Please try again.",
                        "agent": "system",
                    }
                )

        # Not a document request - use the chat orchestrator with agent swarm
        raise Exception("Not a document request - use orchestrator")

    except Exception as router_error:
        # Use the new Chat Orchestrator (agent swarm with memory)
        try:
            # Get shared client from app state
            app_state = getattr(request.app, "state", None)
            http_client = getattr(app_state, "http_client", None) if app_state else None

            # Build LLM client wrapper for orchestrator
            api_key_value = api_key  # Capture for closure

            async def llm_wrapper(
                system_prompt: str, user_message: str, history: list
            ) -> str:
                if not api_key_value:
                    return chat_orchestrator.orchestrator._fallback_response(
                        user_message
                    )

                # Validate API key
                key = api_key_value.strip()
                if len(key) < 20 or not key.startswith("sk-"):
                    return "Please provide a valid OpenRouter API key in Settings."

                # Build messages for LLM
                messages = [{"role": "system", "content": system_prompt}]
                for msg in history:
                    messages.append({"role": msg["role"], "content": msg["content"]})
                messages.append({"role": "user", "content": user_message})

                try:
                    response = await http_client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": model,
                            "messages": messages,
                        },
                        timeout=30.0,
                    )
                    if response.status_code != 200:
                        return f"API Error: {response.status_code}"

                    result = response.json()
                    choices = result.get("choices", [])
                    if not choices:
                        return "No response from AI."

                    return choices[0].get("message", {}).get("content", "No response")
                except Exception as e:
                    return f"Error: {str(e)}"

            # Call the orchestrator
            result = await chat_orchestrator.chat(
                sanitized,
                conv_id="default",  # TODO: session-based
                llm_client=llm_wrapper if api_key else None,
            )

            return JSONResponse(
                {
                    "response": result.get("response", "No response"),
                    "agent": result.get("agent", "swarm"),
                }
            )

        except Exception as e:
            # Ultimate fallback
            return JSONResponse(get_fallback_response(sanitized))


@app.get("/api/partners")
async def get_partners():
    """Get all partners."""
    partners = partner_state.list_partners()
    stats = partner_state.get_partner_stats()
    return JSONResponse({"partners": partners, "stats": stats})


@app.post("/api/partners")
async def create_partner(request: Request):
    """Create a new partner."""
    data = await request.json()
    partner = partner_state.add_partner(
        name=data.get("name", ""),
        tier=data.get("tier", "Bronze"),
        contact=data.get("contact", ""),
        email=data.get("email", ""),
    )
    return JSONResponse(partner)


@app.get("/api/partners/{name}")
async def get_partner(name: str):
    """Get a specific partner."""
    partner = partner_state.get_partner(name)
    if partner:
        return JSONResponse(partner)
    return JSONResponse({"error": "Partner not found"}, status_code=404)


async def delete_partner(name: str):
    """Delete a partner."""
    success = partner_state.delete_partner(name)
    if success:
        return JSONResponse({"success": True, "message": f"Partner '{name}' deleted"})
    return JSONResponse({"error": "Partner not found"}, status_code=404)


app.add_api_route("/api/partners/{name}", delete_partner, methods=["DELETE"])


async def call_llm(
    message: str,
    api_key: str,
    model: str = "openai/gpt-4o-mini",
    use_cache: bool = True,
    client: httpx.AsyncClient = None,
) -> dict:
    """Call OpenRouter LLM with partner context."""
    import hashlib

    # Simple cache - hash the message AND model
    cache_key = hashlib.sha256(f"{model}:{message}".encode()).hexdigest()[:16]

    # Check cache settings - if cache disabled, skip it
    if use_cache:
        cache_time = response_cache.get(cache_key)
        if cache_time and time.time() - cache_time.get("ts", 0) < CACHE_TTL_SECONDS:
            return cache_time.get("result")

    # Build context about agents
    system_prompt = """You are the orchestrator of PartnerOS - an AI partner team. 
You have 7 specialized agents:
- The Owner: Runs everything, makes final decisions
- Partner Manager: Owns relationships, onboarding, day-to-day
- Strategy: ICP, tiers, competitive, partner selection
- Operations: Deal registration, commissions, portal, compliance
- Marketing: Campaigns, leads, content, co-marketing
- Leader: Board decks, ROI, executive communication
- Technical: Integrations, APIs, developer experience

When user asks something, respond as the most appropriate agent(s).
Be helpful, concise, and actionable."""

    # Internal function to do the actual call
    async def _do_call(c: httpx.AsyncClient):
        try:
            response = await c.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,  # Use user-selected model from settings
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message},
                    ],
                },
                timeout=30.0,
            )

            if response.status_code == 401:
                # API key invalid - use fallback responses
                return get_fallback_response(message)

            # Check for invalid API key errors (2049)
            try:
                result = response.json()
                if (
                    "base_resp" in result
                    and result.get("base_resp", {}).get("status_code") == 2049
                ):
                    return get_fallback_response(message)
            except:
                pass

            if response.status_code != 200:
                return {
                    "response": f"API Error ({response.status_code}): {response.text[:200]}",
                    "agent": "system",
                }

            result = response.json()

            choices = result.get("choices")
            if not choices:
                return {
                    "response": f"API returned no choices: {result}",
                    "agent": "system",
                }

            reply = choices[0].get("message", {}).get("content", "No response")

            result = {"response": reply, "agent": "Partner Manager"}

            # Only cache if user has caching enabled
            if use_cache:
                response_cache[cache_key] = {"result": result, "ts": time.time()}

            return result

        except Exception as e:
            return get_fallback_response(message)

    if client:
        return await _do_call(client)
    else:
        # Fallback if no shared client provided
        async with httpx.AsyncClient() as new_client:
            return await _do_call(new_client)


def get_fallback_response(message: str) -> dict:
    """Fallback responses when API is unavailable."""
    msg = message.lower()

    if "onboard" in msg or "new partner" in msg:
        return {
            "response": """I'll help onboard this partner! Here's the plan:

**Week 1: Setup**
- Complete partner agreement
- Set up in partner portal
- Configure deal registration

**Weeks 2-3: Enablement**
- Schedule orientation session
- Provide sales decks & demo access
- Technical training

**Week 4: Go-Live**
- Joint business planning
- Set commission structure
- Plan first co-sell opportunity

Would you like me to proceed? I can bring in other agents for specific tasks.""",
            "agent": "Partner Manager",
        }
    elif "deal" in msg or "register" in msg:
        return {
            "response": """Deal registered! 

**Details:**
- Deal protected for 90 days
- Commission will be calculated based on tier

Would you like me to calculate the commission?""",
            "agent": "Operations",
        }
    elif "campaign" in msg or "marketing" in msg:
        return {
            "response": """Campaign launched! 🎉

I've set up:
- Welcome email sequence (3 emails)
- Social media announcement
- Partner portal update

Need anything else?""",
            "agent": "Marketing",
        }
    elif "icp" in msg or "qualify" in msg or "evaluate" in msg:
        return {
            "response": """Based on the criteria, here's the evaluation:

**Score: 78/100 - Strong Fit**

- Revenue alignment: 80%
- Market fit: 75%
- Technical capability: 80%
- Cultural fit: 75%

**Recommendation: Proceed to next steps**

Want me to create a formal proposal?""",
            "agent": "Strategy",
        }
    elif "roi" in msg or "board" in msg or "executive" in msg:
        return {
            "response": """Here's the ROI analysis:

**Program ROI: 340%**
- Total investment: $50K
- Partner-sourced revenue: $220K
- Payback period: 3 months

**Board highlights:**
- 12 new partners this quarter
- $1.2M pipeline from partners
- 35% of revenue from channel

Need a formal deck?""",
            "agent": "Leader",
        }
    else:
        return {
            "response": """I'm here to help with your partner program! 

**What I can do:**
- Onboard new partners
- Register deals
- Launch marketing campaigns
- Evaluate prospects (ICP)
- Calculate ROI
- Create board decks

What would you like to do?""",
            "agent": "Partner Manager",
        }


if __name__ == "__main__":
    print("🚀 Starting PartnerOS Web Interface...")
    print("   Open http://localhost:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000)
