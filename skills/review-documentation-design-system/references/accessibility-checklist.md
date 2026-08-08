# Accessibility And Responsive Behavior Checklist

| ID | Observable pass criterion | Required evidence |
| --- | --- | --- |
| DDS-ACC-001 | Header, distinctly named navigation regions, unique main, sections, articles, asides, figures, and footer form a logical landmark/reading order; sections are named by visible headings. | Accessibility-tree landmark inventory and DOM-order comparison. |
| DDS-ACC-002 | The logo has meaningful alt text; decorative arrows/gears are hidden; icon-only controls are named; meaningful SVGs have `title`/`desc`; CSS diagrams have `role="img"` and a relationship-focused alternative. | Accessible-name audit for every applicable visual/control. |
| DDS-ACC-003 | Every interactive component has a complete keyboard path and visible focus; skip link bypasses repeated navigation; native disclosure works; dialogs move/contain/return focus and close on Escape. | End-to-end keyboard trace with active element and focus-style evidence. |
| DDS-ACC-004 | Successful preferences/completion use `role="status"`, failures use `role="alert"`, non-urgent step changes use `aria-live="polite"`, and inactive steps/messages use `hidden`. | Triggered state matrix showing DOM semantics and announced text. |
| DDS-ACC-005 | Content-driven breakpoints from 520–900px preserve all information and interaction while reducing padding, stacking columns/complex visuals, wrapping navigation, and putting wide tables in wrapper overflow. | Checks near each documented failure range (520–560, 620–720, 780–900) with viewport and layout evidence. |
| DDS-ACC-006 | Breakpoints are justified by observed component failure points; the implementation does not collapse them into one global threshold without component testing. | Breakpoint-to-component mapping and responsive test evidence. |
| DDS-ACC-007 | Print output hides navigation and controls, uses a white background, prevents important cards from splitting, and retains readable content. | Print stylesheet inspection and print-preview/PDF evidence. |
| DDS-ACC-008 | The observed-gaps section truthfully reports inconsistent skip links/main targets, lifecycle hero labeling, table overflow ownership, limited explicit print coverage, and the deliberate unlabeled-input fixture without presenting defects as patterns. | Exact gap list and comparison to authoritative source inventory/snapshot. |
