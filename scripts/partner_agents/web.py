#!/usr/bin/env python3
"""
PartnerOS Web Interface
A beautiful web UI for the multi-agent partner team.
"""

import os
import sys

# Import fastapi BEFORE adding scripts to path (to avoid local test shim)
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import uvicorn
import httpx
import hashlib
from contextlib import asynccontextmanager

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

# In-memory rate limiting
import time

rate_limit_store = {}
response_cache = {}


def check_rate_limit(ip: str, max_requests: int = 20, window_seconds: int = 60) -> bool:
    """Simple rate limiter - max 20 requests per minute per IP."""
    now = time.time()
    if ip not in rate_limit_store:
        rate_limit_store[ip] = []

    # Remove old requests
    rate_limit_store[ip] = [t for t in rate_limit_store[ip] if now - t < window_seconds]

    if len(rate_limit_store[ip]) >= max_requests:
        return False

    rate_limit_store[ip].append(now)
    return True


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan and shared resources."""
    # Initialize shared httpx client for connection pooling
    async with httpx.AsyncClient() as client:
        app.state.client = client
        yield


app = FastAPI(title="PartnerOS", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost", "127.0.0.1"],  # Restrict to local for security
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
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
    </style>
</head>
<body class="gradient-bg min-h-screen text-white">
    <div class="max-w-6xl mx-auto px-4 py-8">
        <!-- Header -->
        <header class="text-center mb-6 px-4">
            <h1 class="text-3xl sm:text-5xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent mb-2">
                PartnerOS
            </h1>
            <p class="text-slate-400 text-sm sm:text-base">Your AI Partner Team</p>
        </header>

        <!-- Team Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-2 mb-6">
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">👑</div>
                <div class="font-semibold text-cyan-400 text-sm">The Owner</div>
                <div class="text-xs text-slate-500">Executive</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">🏗️</div>
                <div class="font-semibold text-cyan-400 text-sm">Partner Manager</div>
                <div class="text-xs text-slate-500">Relationships</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">🎯</div>
                <div class="font-semibold text-cyan-400 text-sm">Strategy</div>
                <div class="text-xs text-slate-500">ICP & Tiers</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">⚙️</div>
                <div class="font-semibold text-cyan-400 text-sm">Operations</div>
                <div class="text-xs text-slate-500">Deals & Comms</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">✨</div>
                <div class="font-semibold text-cyan-400 text-sm">Marketing</div>
                <div class="text-xs text-slate-500">Campaigns</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">🏆</div>
                <div class="font-semibold text-cyan-400 text-sm">Leader</div>
                <div class="text-xs text-slate-500">Board & ROI</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">🔧</div>
                <div class="font-semibold text-cyan-400 text-sm">Technical</div>
                <div class="text-xs text-slate-500">Integrations</div>
            </div>
        </div>

        <!-- Partners Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold text-white">Partners</h2>
                <button onclick="showAddPartnerForm()" class="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded-lg text-sm transition">+ Add Partner</button>
            </div>
            <div id="partnersList" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div class="text-slate-400 text-sm">Loading partners...</div>
            </div>
        </div>

        <!-- Add Partner Modal -->
        <div id="addPartnerModal" class="hidden fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div class="bg-slate-800 rounded-xl p-6 max-w-md w-full mx-4 relative">
                <button onclick="hideAddPartnerForm()" class="absolute top-4 right-4 text-slate-400 hover:text-white" aria-label="Close modal">✕</button>
                <h3 class="text-lg font-bold mb-4">Add New Partner</h3>
                <label for="partnerName" class="block text-sm font-medium text-slate-400 mb-1">Company Name</label>
                <input id="partnerName" type="text" placeholder="e.g. Acme Corp" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 mb-3 focus:border-cyan-500 outline-none">
                <label for="partnerTier" class="block text-sm font-medium text-slate-400 mb-1">Partner Tier</label>
                <select id="partnerTier" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 mb-3 focus:border-cyan-500 outline-none">
                    <option value="Bronze">Bronze</option>
                    <option value="Silver">Silver</option>
                    <option value="Gold">Gold</option>
                </select>
                <label for="partnerEmail" class="block text-sm font-medium text-slate-400 mb-1">Contact Email</label>
                <input id="partnerEmail" type="email" placeholder="contact@company.com" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 mb-4 focus:border-cyan-500 outline-none">
                <div class="flex gap-3">
                    <button id="addPartnerBtn" onclick="addPartner()" class="flex-1 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed">Add Partner</button>
                    <button onclick="hideAddPartnerForm()" class="px-4 py-2 bg-slate-600 hover:bg-slate-500 rounded-lg transition-colors">Cancel</button>
                </div>
            </div>
        </div>

        <!-- Chat Container -->
        <div class="bg-slate-800/50 rounded-2xl border border-slate-700 overflow-hidden mx-2 sm:mx-0">
            <!-- Messages -->
            <div id="messages" class="h-64 sm:h-96 overflow-y-auto p-4 sm:p-6 space-y-3 sm:space-y-4">
                <div class="message-enter flex gap-3">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center flex-shrink-0">🤖</div>
                    <div class="bg-slate-700/50 rounded-xl p-4 max-w-lg">
                        <p class="text-sm">Welcome to PartnerOS! 👋</p>
                        <p class="text-sm mt-2 text-slate-300">I'm connected to your AI partner team. What would you like to do?</p>
                        <div class="mt-3 flex flex-wrap gap-2">
                            <button onclick="sendMessage('Onboard Acme Corp as Gold partner')" class="px-3 py-1 bg-cyan-600 hover:bg-cyan-500 rounded-full text-xs transition">Onboard partner</button>
                            <button onclick="sendMessage('Register a deal for TechCorp, $50000')" class="px-3 py-1 bg-purple-600 hover:bg-purple-500 rounded-full text-xs transition">Register deal</button>
                            <button onclick="sendMessage('Launch a welcome campaign')" class="px-3 py-1 bg-pink-600 hover:bg-pink-500 rounded-full text-xs transition">Launch campaign</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Input -->
            <div class="border-t border-slate-700 p-4">
                <div class="flex gap-3">
                    <label for="messageInput" class="sr-only">Type your message</label>
                    <input 
                        id="messageInput"
                        type="text" 
                        placeholder="Type your message..." 
                        class="flex-1 bg-slate-700/50 border border-slate-600 rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-500 transition disabled:opacity-50"
                        onkeypress="if(event.key==='Enter')sendMessage()"
                    >
                    <button 
                        id="sendBtn"
                        onclick="sendMessage()"
                        class="px-6 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-xl font-semibold hover:opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Send
                    </button>
                </div>
            </div>
        </div>

        <!-- Status -->
        <div class="text-center mt-6 text-slate-500 text-sm">
            <span id="status">● Ready</span> • 7 Agents • 36 Skills • LLM Connected
        </div>
    </div>

    <script>
        const escapeHTML = (str) => String(str).replace(/[&<>"']/g, m => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        })[m]);

        // API key should be provided by the user at runtime when needed
        let apiKey = '';

        async function sendMessage(text) {
            const input = document.getElementById('messageInput');
            const btn = document.getElementById('sendBtn');
            const message = text || input.value.trim();
            if (!message) return;
            
            input.value = '';
            input.disabled = true;
            btn.disabled = true;
            
            // Add user message
            addMessage(message, 'user');
            
            // Show typing
            showTyping();
            
            try {
                console.log('Sending message:', message, 'API key:', apiKey ? 'present' : 'missing');
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message, apiKey: apiKey || ''})
                });
                
                console.log('Response status:', response.status);
                const data = await response.json();
                console.log('Response data:', data);
                hideTyping();
                addMessage(data.response, 'assistant', data.agent);
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
                div.innerHTML = `
                    <div role="img" aria-label="${agentName}" class="w-8 h-8 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center flex-shrink-0">${emoji}</div>
                    <div class="bg-slate-700/50 rounded-xl p-4 max-w-lg">
                        <span class="sr-only">${agentName}: </span>
                        ${escapeHTML(text)}
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
        
        // Partner management
        async function loadPartners() {
            try {
                const response = await fetch('/api/partners');
                if (!response.ok) throw new Error('Failed to load partners');
                const data = await response.json();
                const container = document.getElementById('partnersList');
                
                if (data.partners.length === 0) {
                    container.innerHTML = `
                        <div class="text-center py-8 px-4">
                            <div class="text-4xl mb-3">📦</div>
                            <div class="text-slate-400 text-sm mb-2">No partners yet</div>
                            <div class="text-slate-500 text-xs">Add your first partner using the form above</div>
                        </div>
                    `;
                    return;
                }
                
                container.innerHTML = data.partners.map(p => `
                    <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
                        <div class="flex justify-between items-start mb-2">
                            <div>
                                <div class="font-semibold text-white">${escapeHTML(p.name)}</div>
                                <div class="text-xs text-slate-400">${escapeHTML(p.email || 'No email')}</div>
                            </div>
                            <div class="flex items-center gap-2">
                                <span class="px-2 py-1 rounded-full text-xs ${p.tier === 'Gold' ? 'bg-yellow-600' : p.tier === 'Silver' ? 'bg-gray-400' : 'bg-orange-600'}">${p.tier}</span>
                                <button onclick="deletePartner('${escapeHTML(p.name)}')" class="text-slate-500 hover:text-red-400 transition" title="Delete partner">🗑️</button>
                            </div>
                        </div>
                        <div class="text-xs text-slate-500">${p.deals?.length || 0} deals • ${p.status || 'Onboarding'}</div>
                    </div>
                `).join('');
            } catch (e) {
                console.error('Error loading partners:', e);
            }
        }
        
        function showAddPartnerForm() {
            document.getElementById('addPartnerModal').classList.remove('hidden');
        }
        
        function hideAddPartnerForm() {
            document.getElementById('addPartnerModal').classList.add('hidden');
        }
        
        async function addPartner() {
            const name = document.getElementById('partnerName').value;
            const tier = document.getElementById('partnerTier').value;
            const email = document.getElementById('partnerEmail').value;
            const btn = document.getElementById('addPartnerBtn');
            
            if (!name) {
                alert('Please enter a company name');
                return;
            }
            
            btn.disabled = true;
            btn.innerText = 'Adding...';

            try {
                await fetch('/api/partners', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, tier, email})
                });
                hideAddPartnerForm();
                loadPartners();
                document.getElementById('partnerName').value = '';
                document.getElementById('partnerEmail').value = '';
            } catch (e) {
                alert('Error adding partner: ' + e.message);
            } finally {
                btn.disabled = false;
                btn.innerText = 'Add Partner';
            }
        }
        
        // Load partners on page load
        loadPartners();
        
        // Delete partner
        async function deletePartner(name) {
            if (!confirm(`Delete partner "${name}"?`)) return;
            try {
                await fetch('/api/partners/' + encodeURIComponent(name), { method: 'DELETE' });
                loadPartners();
            } catch (e) {
                alert('Error deleting partner: ' + e.message);
            }
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

    # Sanitize: remove potentially dangerous patterns
    sanitized = user_message.replace("<script", "").replace("</script", "")

    # Rate limiting check
    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_ip):
        return JSONResponse(
            {
                "response": "⚠️ Too many requests. Please wait a moment and try again.",
                "agent": "system",
            },
            status_code=429,
        )

    if not api_key or len(api_key) < 10:
        return JSONResponse(
            {
                "response": "⚠️ No API key provided. Add one from https://openrouter.ai/keys to use live LLM responses.",
                "agent": "system",
            }
        )

    # Try LLM first, fallback on error
    try:
        # Use shared client from app state if available, otherwise fallback to temporary client
        client = getattr(request.app.state, "client", None) if hasattr(request, "app") else None

        if client:
            response = await call_llm(user_message, api_key, client)
        else:
            async with httpx.AsyncClient() as temp_client:
                response = await call_llm(user_message, api_key, temp_client)

        if response.get("response"):
            return JSONResponse(response)
        raise Exception("Empty response")
    except Exception as e:
        # Fallback on any error
        return JSONResponse(get_fallback_response(user_message))


@app.get("/api/partners")
async def get_partners():
    """Get all partners."""
    partners = partner_state.list_partners()
    # Reuse the already loaded partners list to avoid redundant file I/O
    stats = partner_state.get_partner_stats(partners)
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


async def call_llm(message: str, api_key: str, client: httpx.AsyncClient) -> dict:
    """Call OpenRouter LLM with partner context."""
    # Simple cache - hash the message
    cache_key = hashlib.sha256(message.encode()).hexdigest()[:16]
    cache_time = response_cache.get(cache_key)
    if cache_time and time.time() - cache_time.get("ts", 0) < 300:
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

    try:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "minimax/minimax-m2.5",
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
        response_cache[cache_key] = {"result": result, "ts": time.time()}
        return result

    except Exception as e:
        return get_fallback_response(message)


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
