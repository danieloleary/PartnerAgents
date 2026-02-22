## 2025-05-22 - [Monolithic UI Accessibility]
**Learning:** In projects where the frontend is served as a monolithic HTML string from a backend file (like scripts/partner_agents/web.py), accessibility features (labels, ARIA attributes) and interactive states (loading indicators) are often overlooked because they aren't part of a structured component library.
**Action:** Always audit the HTML string for missing <label> elements and ensure that asynchronous JavaScript functions (fetch calls) properly toggle disabled and textContent states on trigger buttons to prevent multiple submissions and provide feedback.

## 2025-05-23 - [Modal Focus and Keyboard Nav Indicators]
**Learning:** Monolithic UIs often lack standard browser focus behavior. Implementing `focus-visible` styles ensures keyboard users have clear navigation indicators without cluttering the UI for mouse users. Additionally, programmatically focusing the first input in a modal via `setTimeout` significantly improves the "time-to-action" for new entries.
**Action:** When working with dynamically shown modals in the monolithic `web.py`, always add a focus call to the primary input. Ensure `button:focus-visible` styles are present in the CSS block to support accessible navigation.
