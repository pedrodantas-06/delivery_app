# Deliverer Design System

Last updated: 2026-06-09

## Visual Direction

The visual system should feel like a modern operational app inspired by iFood, but with liquid glass surfaces and softer depth. The goal is speed and trust, not decorative complexity.

## Color Palette

### Core

| Token | Value | Use |
|---|---|---|
| Primary | #FF5A1F | Primary CTA, highlights, active states |
| Primary Hover | #E84B12 | Pressed and hover feedback |
| Primary Soft | #FFF0E9 | Subtle emphasis backgrounds |
| Surface | rgba(255,255,255,0.72) | Glass cards and panels |
| Surface Strong | rgba(255,255,255,0.92) | Elevated cards and sheets |
| Border | rgba(255,255,255,0.24) | Glass borders |
| Text Primary | #111827 | Main copy |
| Text Secondary | #6B7280 | Supporting copy |
| Backdrop | #F5F7FB | Page base |

### Semantic

| Token | Value | Meaning |
|---|---|---|
| Success | #16A34A | Available, completed, healthy |
| Warning | #F59E0B | Pending, attention needed |
| Error | #DC2626 | Failed, blocked, invalid |
| Info | #2563EB | Active, in progress, informational |

### Status Chips

| Status | Background | Text |
|---|---|---|
| AVAILABLE | #DCFCE7 | #166534 |
| BUSY | #DBEAFE | #1D4ED8 |
| OCCUPIED | #FEF9C3 | #854D0E |
| OFFLINE | #E5E7EB | #374151 |

## Typography

### Font Stack

- Primary: Inter
- Fallback: system-ui, sans-serif

### Scale

| Style | Size | Weight | Use |
|---|---|---|---|
| Display | 32-36px | 700 | Login hero and screen titles |
| Heading Large | 24px | 700 | Main sections |
| Heading Medium | 20px | 600 | Card titles and subheads |
| Body Large | 16px | 400 | Key descriptions |
| Body Medium | 14px | 400 | Supporting UI copy |
| Caption | 12px | 400 | Metadata and timestamps |

### Type Rules

- Keep line height generous on mobile.
- Never rely on uppercase for long text blocks.
- Use short labels for operational controls.

## Spacing

Use an 8-point system only.

Allowed values: 4, 8, 12, 16, 24, 32, 40, 48, 64.

Rules:

- 4 and 8 for chip and metadata spacing.
- 12 and 16 for internal card padding.
- 24 and 32 for section separation.
- 40 and 48 only for large layout breathing room.

## Radius

| Token | Value | Use |
|---|---|---|
| Small | 8px | Inputs and compact buttons |
| Medium | 12px | Chips and control surfaces |
| Large | 16px | Cards and sheets |
| Card | 20px | Primary glass cards |
| Pill | 999px | Status pills and floating controls |

## Elevation

### Soft Elevation Levels

| Level | Use |
|---|---|
| 1 | Subtle components and list rows |
| 2 | Cards and grouped surfaces |
| 3 | Floating shell navigation and primary sheets |

Rules:

- Avoid harsh shadows.
- Prefer blur, border, and slight lift over heavy drop shadows.
- Use contrast sparingly so the interface remains calm.

## Motion

### Duration

| Token | Value |
|---|---|
| Fast | 120ms |
| Base | 180ms |
| Slow | 240ms |

### Easing

- Use ease-out for entry.
- Use ease-in for exit.
- Keep status transitions short and clear.

### Motion Rules

- Animate only state changes that matter.
- Use subtle scale or fade on card entrance.
- Use micro-motion for chips, badges, and refresh actions.
- Respect reduced-motion preferences.

## Buttons

### Variants

- Primary: strongest CTA, orange.
- Secondary: supportive action, cool neutral or blue.
- Ghost: low emphasis, transparent or soft surface.

### Rules

- Minimum touch size: 44px height.
- Primary button should be reserved for the next operational step.
- Use full-width buttons in login and confirmation states.

## Cards

### Card Types

- Glass card: translucent primary container.
- Subtle card: lower-emphasis grouping.
- Action card: card with a footer action area.
- Status card: summary card for availability or metrics.

### Card Rules

- Titles should be short and actionable.
- Metadata should be compact and scannable.
- Do not overload cards with more than one dominant action.

## Navigation

### Floating Dock

- Bottom floating navigation is the default shell pattern.
- Use four destinations: Dashboard, Active, History, Profile.
- The active state should be visually obvious without using only color.

### Rules

- Keep navigation fixed and reachable.
- Avoid hidden navigation for core screens.
- Make the current context visible in the shell header.

## Inputs

### Styles

- Soft border, medium radius, light background.
- Clear focus ring.
- Large enough for quick mobile data entry.

### Rules

- Use label above field, not placeholder only.
- Keep field count minimal.
- Do not stack more fields than necessary in one screen.

## Badges

### Meaning

- Badges must represent operational state, not decoration.
- Use concise labels only.
- A badge should always be accompanied by nearby text context when the state is important.

### Status Chips

- Available
- Busy
- Occupied
- Offline

### Delivery Chips

- Waiting
- Assigned
- In Delivery
- Picked Up
- Delivered
- Cancelled

## Icons

- Use simple line icons with minimal visual noise.
- Icons should support, not replace, text labels.
- Keep icon use consistent across navigation and actions.

## Backgrounds

- Use layered gradients and atmospheric blur for the page shell.
- Use glass surfaces to create depth hierarchy.
- Avoid flat single-color screens.

## Accessibility Notes

- High contrast text is mandatory.
- Target touch size must never fall below 44x44.
- Focus states must be visible in all themes.
- Motion must be optional for users who prefer reduced motion.

## Practical Implementation Guidance

- Reuse current shared primitives, but replace hardcoded styles with tokens.
- Keep the design system small enough to implement incrementally.
- Use CSS variables for the core palette and surface system.
- Avoid introducing a complex component library before the new shell is stable.
