# Design System Document: High-End Dashboards

## 1. Overview & Creative North Star
**The Creative North Star: "The Neural Pulse"**

This design system is not a static interface; it is a living, breathing ecosystem. To move beyond the "SaaS-template" aesthetic, we are leaning into **The Neural Pulse**—a philosophy where data isn't just displayed, it is felt. We achieve this through a "Liquid Editorial" approach: combining the prestige of high-end typography with the kinetic energy of neon glassmorphism. 

By breaking the rigid grid with intentional asymmetry—such as overlapping glass cards and varying container heights—we create a sense of forward motion. The interface should feel like a high-tech command center that is both authoritative and vibrantly youthful.

---

## 2. Colors & Surface Philosophy
The palette is rooted in deep space blacks and high-energy neon accents. We do not use "flat" colors; we use light.

### Color Tokens (Material Convention)
*   **Background:** `#060e20` (The void)
*   **Primary (Neon Cyan):** `#a1faff` | **Container:** `#00f4fe`
*   **Secondary (Emerald):** `#69f6b8` | **Container:** `#006c49`
*   **Tertiary (Electric Amber):** `#ffb148` | **Container:** `#f8a010`
*   **Error (Vivid Crimson):** `#ff716c` | **Container:** `#9f0519`

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders to section off content. Boundaries must be defined through **Tonal Transitions**. 
*   Use `surface-container-low` for large section backgrounds.
*   Use `surface-container-high` for nested interactive modules.
*   Separation is achieved through contrast in luminance, never through a line.

### The Glass & Gradient Rule
To achieve the "Live" vibe, main CTAs and Hero elements must use a **linear gradient** transitioning from `primary` to `primary_container` at a 135-degree angle. Floating elements must utilize **Glassmorphism**:
*   **Fill:** `surface_variant` at 40-60% opacity.
*   **Effect:** Backdrop Blur (20px to 40px).
*   **Edge:** A "Ghost Border" (see Section 4).

---

## 3. Typography: The Editorial Edge
We pair the technical precision of **Inter** with the aggressive, wide-set personality of **Space Grotesk** for headers.

*   **Display (Space Grotesk):** 3.5rem (`display-lg`) down to 2.25rem. Use Bold weights for "Live" data points. This creates a high-tech, "headline" feel.
*   **Headline (Space Grotesk):** 2rem to 1.5rem. These act as the anchors for your asymmetrical layout.
*   **Body (Inter):** 1rem (`body-lg`) to 0.75rem. Inter provides the legibility required for dense traffic analytics.
*   **Labels (Inter):** 0.75rem. Use All-Caps with 0.05em letter spacing for a "NASA-spec" technical aesthetic.

---

## 4. Elevation & Depth
Depth in this system is an atmospheric effect, not a structural one.

### The Layering Principle
Stacking defines priority. 
1.  **Level 0:** `surface_dim` (The base).
2.  **Level 1:** `surface_container_low` (General content areas).
3.  **Level 2:** `surface_container_highest` (Active cards/Glass layers).

### Ambient Shadows & Ghost Borders
*   **Shadows:** Shadows are strictly prohibited on dark surfaces except for floating modals. Use a `4-8%` opacity shadow tinted with the `primary` color (Cyan) to simulate a light source from the screen.
*   **The Ghost Border:** For accessibility on glass elements, use a `1px` border with the `outline_variant` token at **15% opacity**. This creates a "specular highlight" on the edge of the glass rather than a hard stroke.

---

## 5. Components

### Buttons: Kinetic Triggers
*   **Primary:** Gradient fill (`primary` to `primary_container`). Use a `0 0 20px` outer glow (same color) on hover to simulate "powering up."
*   **Secondary:** Ghost Border style with `on_surface` text.
*   **Tertiary:** Text-only with `primary` color and bold weight.

### Cards & Lists: The Stream
*   **Cards:** No borders. Use `surface_container_low`. Apply `xl` (1.5rem) corner radius for a modern, approachable feel.
*   **Lists:** Forbid divider lines. Use `1.5rem` of vertical white space or a slight background shift (`surface_container_lowest` for even rows) to separate items.

### High-Tech Status Indicators
*   **Glow Chips:** Success/Danger states should not just be colored text. Use a small, high-intensity glow (`box-shadow`) behind the chip to indicate "Live" status.
*   **Input Fields:** Use `surface_container_highest` with a `2px` bottom-only "active" bar in `primary` (Cyan) when focused. No full box-outlines.

### Key Contextual Components
*   **The Pulse Meter:** A custom circular progress component using the `secondary` (Emerald) gradient to show traffic health.
*   **Glass Modals:** 40% opaque `surface_variant` with a heavy 40px backdrop blur for high-priority alerts.

---

## 6. Do’s and Don’ts

### Do:
*   **Do** overlap elements slightly (e.g., a glass card overlapping a gradient background) to create depth.
*   **Do** use `primary_fixed_dim` for "read-only" data to keep the screen from becoming a neon mess.
*   **Do** use asymmetrical margins (e.g., more padding on the left than the right in headers) to create an editorial feel.

### Don't:
*   **Don't** use pure white (#FFFFFF). Use `on_surface` (`#dee5ff`) for text to maintain the dark-mode immersion.
*   **Don't** use standard "Drop Shadows." If an element needs to pop, use a "Glow" or a Tonal Shift.
*   **Don't** use 1px dividers. If you feel the need for a line, increase your spacing by `0.5rem` instead.