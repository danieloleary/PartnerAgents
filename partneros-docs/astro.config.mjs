// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import react from '@astrojs/react';

export default defineConfig({
	base: '/PartnerOS',
	site: 'https://danieloleary.github.io',
	integrations: [
		react(),
		starlight({
			title: 'PartnerOS',
			description: 'The complete playbook for building and scaling strategic partnerships with AI-powered automation.',
			logo: {
				src: './src/assets/logo.svg',
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/danieloleary/PartnerOS' },
				{ icon: 'linkedin', label: 'LinkedIn', href: 'https://linkedin.com/in/danieloleary' },
			],
			customCss: [
				'./src/content/docs/stylesheets/extra.css',
			],
			head: [
				{
					tag: 'script',
					attrs: { type: 'text/javascript' },
					content: `
						// Mermaid setup
						mermaid.initialize({ 
							startOnLoad: false,
							theme: 'dark',
							securityLevel: 'loose',
						 flowchart: { useMaxWidth: true, htmlLabels: true }
						});
						
						// Interactive Checkboxes with localStorage
						function initChecklists() {
							const pageKey = window.location.pathname;
							const storageKey = 'partneros_checklist_' + pageKey;
							const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
							
							// Find all task list items
							document.querySelectorAll('input[type="checkbox"]').forEach((checkbox, index) => {
								const label = checkbox.closest('li')?.textContent?.substring(0, 50) || 'task-' + index;
								const taskKey = 'task-' + index;
								
								// Restore saved state
								if (saved[taskKey]) {
									checkbox.checked = true;
									checkbox.parentElement?.classList.add('completed');
								}
								
								// Add click handler
								checkbox.addEventListener('change', () => {
									const newState = {};
									document.querySelectorAll('input[type="checkbox"]').forEach((cb, i) => {
										newState['task-' + i] = cb.checked;
										if (cb.checked) {
											cb.parentElement?.classList.add('completed');
										} else {
											cb.parentElement?.classList.remove('completed');
										}
									});
									localStorage.setItem(storageKey, JSON.stringify(newState));
								});
							});
						}
						
						document.addEventListener('DOMContentLoaded', async () => {
							// Initialize Mermaid
							const diagrams = document.querySelectorAll('.language-mermaid, .mermaid');
							for (const diagram of diagrams) {
								const pre = diagram.closest('pre') || diagram;
								const code = diagram.textContent || diagram.innerText;
								if (code.trim()) {
									const div = document.createElement('div');
									div.className = 'mermaid-diagram';
									div.setAttribute('data-chart', code);
									pre.parentNode.replaceChild(div, pre);
								}
							}
							await mermaid.run({ nodes: document.querySelectorAll('.mermaid-diagram') });
							
							// Initialize checklists
							initChecklists();
							
							// Add feedback button to page
							const footer = document.querySelector('footer') || document.querySelector('.footer');
							if (footer) {
								const feedbackLink = document.createElement('a');
								feedbackLink.href = 'https://github.com/danieloleary/PartnerOS/issues/new?title=Feedback: ' + encodeURIComponent(document.title);
								feedbackLink.target = '_blank';
								feedbackLink.className = 'feedback-btn';
								feedbackLink.innerHTML = '💬 Give Feedback';
								feedbackLink.style.cssText = 'display:inline-flex;align-items:center;gap:0.5rem;padding:0.5rem 1rem;margin:1rem auto;background:var(--sl-color-accent);color:var(--sl-color-white);border-radius:6px;text-decoration:none;font-size:0.875rem;';
								footer.insertBefore(feedbackLink, footer.firstChild);
							}
						});
					`,
				},
			],
			sidebar: [
			{ label: 'Getting Started', autogenerate: { directory: 'getting-started' } },
			{ label: 'Strategy', autogenerate: { directory: 'strategy' } },
			{ label: 'Recruitment', autogenerate: { directory: 'recruitment' } },
			{ label: 'Enablement', autogenerate: { directory: 'enablement' } },
			{ label: 'Legal', autogenerate: { directory: 'legal' } },
			{ label: 'Finance', autogenerate: { directory: 'finance' } },
			{ label: 'Security', autogenerate: { directory: 'security' } },
			{ label: 'Operations', autogenerate: { directory: 'operations' } },
			{ label: 'Executive', autogenerate: { directory: 'executive' } },
			{ label: 'Analysis', autogenerate: { directory: 'analysis' } },
			{ label: 'Partner Agent', autogenerate: { directory: 'agent' } },
			{ label: 'Skills', autogenerate: { directory: 'skills' } },
		],
		}),
	],
});
