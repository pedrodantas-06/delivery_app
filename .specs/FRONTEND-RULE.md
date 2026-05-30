# FRONTEND-RULE.md
# Delivery Universitário — Design System & UX Rulebook

Version: 1.0
Audience: Designers, Frontend Engineers, AI Coding Agents

---

# 1. PRODUCT DESIGN PRINCIPLES

## Core Principles

1. Fast before beautiful
2. Reduce clicks whenever possible
3. Every screen must answer:
   - What happened?
   - What is happening?
   - What should I do next?
4. Never surprise the user
5. Optimize for hungry users under time pressure
6. Mobile-first always
7. Accessibility is not optional

---

# 2. MARKET RESEARCH SUMMARY

## Common User Pain Points

### Ordering

- Too many steps before checkout
- Confusing restaurant menus
- Hidden fees
- Unclear delivery times

### Delivery

- Poor order tracking
- Unclear status updates
- Delivery delays without explanation

### Support

- Hard to contact support
- Slow problem resolution
- Lack of transparency

---

## Best Features Found in Market Leaders

### iFood

- Strong restaurant discovery
- Personalized recommendations
- Fast checkout

### Uber Eats

- Clean navigation
- Strong tracking experience
- Reliable delivery estimates

### DoorDash

- Order status visibility
- Group ordering
- Scheduled delivery

### Rappi

- Multi-service ecosystem
- Strong promotional mechanics

### Zomato

- Restaurant information quality
- Reviews and ratings

---

## UX Trends

### Navigation

- Bottom Navigation
- Sticky Search Bar
- Persistent Cart

### Visual Design

- Large food imagery
- Rounded corners
- Clean spacing

### Feedback

- Skeleton loading
- Real-time status updates
- Subtle microinteractions

### Accessibility

- Minimum touch target: 44x44
- High contrast text
- Dynamic font support

---

# 3. DESIGN SYSTEM

## Design Philosophy

Simple
Friendly
Modern
Fast

---

# 4. COLOR SYSTEM

## Primary

Primary 500

#FF5A1F

Primary Hover

#E84B12

Primary Light

#FFF0E9

---

## Success

#16A34A

---

## Warning

#F59E0B

---

## Error

#DC2626

---

## Neutral

Gray 50  #F9FAFB
Gray 100 #F3F4F6
Gray 200 #E5E7EB
Gray 300 #D1D5DB
Gray 500 #6B7280
Gray 700 #374151
Gray 900 #111827

---

# 5. TYPOGRAPHY

Font Family

Inter

Fallback

system-ui

---

## Heading Large

32px
700

---

## Heading Medium

24px
700

---

## Heading Small

20px
600

---

## Body Large

16px
400

---

## Body Medium

14px
400

---

## Caption

12px
400

---

# 6. SPACING SYSTEM

Use 8-point grid.

Allowed spacing:

4
8
12
16
24
32
40
48
64

Never use arbitrary spacing.

---

# 7. BORDER RADIUS

Small

8px

Medium

12px

Large

16px

Card

20px

---

# 8. ELEVATION

Level 1

Cards

Level 2

Modals

Level 3

Floating Elements

Use subtle shadows only.

---

# 9. COMPONENT RULES

## Primary Button

Purpose

Main action

Height

48px

Radius

12px

State

Default
Hover
Disabled
Loading

Only one primary action per screen.

---

## Secondary Button

Outlined

Neutral border

Used for secondary actions.

---

## Restaurant Card

Must contain:

- Image
- Name
- Category
- Rating
- Delivery Time

Optional:

- Promotion Badge

---

## Delivery Badge

PREPARING

Yellow

READY

Blue

ON_ROUTE

Orange

DELIVERED

Green

CANCELLED

Red

---

## Bottom Navigation

Maximum:

5 tabs

Recommended:

Home
Search
Orders
Favorites
Profile

Always visible.

---

# 10. SCREEN RULES

## Splash

Maximum 2 seconds.

---

## Login

Only:

Email
Password

Avoid unnecessary fields.

---

## Registration

Request:

Name
Email
Password

Nothing else initially.

---

## Home

Priority:

1 Restaurants
2 Promotions
3 Categories

Search always visible.

---

## Restaurant Detail

Must show:

Hero image
Delivery estimate
Rating
Categories
Menu

Sticky cart button.

---

## Cart

Always show:

Items
Subtotal
Fees
Total

Never hide costs.

---

## Checkout

Single page preferred.

Must show:

Delivery location
Payment method
Order summary
Estimated delivery time

---

## Order Tracking

Display:

Progress timeline
Current status
Estimated arrival

No complex maps required for MVP.

---

# 11. UX RULES

## Onboarding

Never request permissions immediately.

Sequence:

1 Explain benefit
2 Request permission

Example:

"We use your location to find restaurants near you."

Only then ask.

---

## Search

Must support:

Restaurant name
Food name

Search visible from Home.

---

## Menu Browsing

Show images when available.

Categories must remain visible while scrolling.

---

## Cart Experience

Cart must persist.

User cannot lose items accidentally.

---

## Checkout Experience

Reduce abandonment.

Rules:

- No hidden fees
- Show final total early
- Keep payment selection simple

---

## Delivery Tracking

Statuses:

ORDER_CREATED
PAYMENT_CONFIRMED
PREPARING
READY
OUT_FOR_DELIVERY
DELIVERED

Maximum clarity.

---

## Ratings

Ask for evaluation only after delivery.

Maximum 10 seconds interaction.

---

# 12. ACCESSIBILITY RULES

Minimum contrast WCAG AA.

Minimum touch target:

44x44 px

Never rely only on color.

Every status needs:

- Color
- Icon
- Label

---

# 13. RESPONSIVENESS

Primary target:

Mobile

Breakpoints

Mobile
0–767

Tablet
768–1023

Desktop
1024+

Desktop is secondary.

---

# 14. AI IMPLEMENTATION RULES

AI agents generating frontend code must:

- Use React + Vite + TypeScript
- Reuse components
- Avoid duplicate UI
- Use design tokens
- Respect spacing scale
- Respect typography scale
- Follow accessibility rules

---

# 15. MVP SCREENS

Required

1 Login
2 Register
3 Home
4 Restaurant Details
5 Cart
6 Checkout
7 Order Tracking
8 Orders History
9 Profile

---

# 16. OUT OF SCOPE

Not allowed in MVP

- Dark mode
- Chat
- AI recommendations
- Loyalty program
- Gamification
- Group orders
- Live maps
- Advanced personalization

Focus on:
Order food quickly and successfully.
