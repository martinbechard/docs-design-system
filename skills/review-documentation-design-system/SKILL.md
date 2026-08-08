---
name: review-documentation-design-system
description: Review a documentation HTML page against the adopted Documentation Design System v0.1.0 contracts and return evidence-backed pass or fail results. Use for design-system conformance reviews of an index, foundation, shell, content, data-display, form, diagram, accessibility, variation-audit, or source-inventory page.
---

# Review Documentation Design System

Review one rendered HTML page and its source. Do not treat the audit examples in `variations.html` as adopted patterns unless that page explicitly marks them adopted or resolved.

## Inputs

- The HTML file or rendered URL under review.
- Its intended page type.
- The design-system version it claims.
- Browser access when behavior or responsive rendering is in scope.

If the page type or claimed version is unavailable, report that as missing evidence; do not infer conformance.

## Workflow

1. Open [shared-checklist.md](references/shared-checklist.md) and the one page-type checklist listed below.
2. Inspect source for semantic, metadata, link, and text requirements.
3. Inspect the rendered page at desktop and narrow width for visual and behavioral requirements. Exercise keyboard interactions when the page contains controls.
4. Record every checklist ID as `PASS`, `FAIL`, or `NOT TESTED`. Use `NOT TESTED` only when required evidence cannot be obtained, and name the missing evidence.
5. For each result, cite concrete evidence: file and line, DOM selector or snippet, browser viewport, interaction performed, screenshot, or audit command and output.
6. Return an overall `PASS` only when every applicable item passes. Any `FAIL` or `NOT TESTED` prevents an overall pass.

## Page Checklists

- [Index](references/index-checklist.md)
- [Foundations](references/foundations-checklist.md)
- [Page shell](references/page-shell-checklist.md)
- [Content](references/content-checklist.md)
- [Data display](references/data-display-checklist.md)
- [Forms and actions](references/forms-and-actions-checklist.md)
- [Diagrams](references/diagrams-checklist.md)
- [Accessibility and responsive behavior](references/accessibility-checklist.md)
- [Variation audit](references/variations-checklist.md)
- [Source inventory](references/source-inventory-checklist.md)

## Result Format

Report the page, claimed version, overall result, and a table with `ID`, `Result`, `Evidence`, and `Remediation`. Keep remediation specific to failed criteria. End with untested evidence and remaining uncertainty.
