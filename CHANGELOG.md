# Changelog

## 0.2.0 — 2026-09-19

- Add a consumer authoring guide, copyable HTML starter, and completed example.
- Document the reusable `.ds-header`, `.ds-footer`, and `.page-nav` classes already supported by the stylesheet; historical source class names remain provenance only.
- Add a local `create-documentation-page` skill and consumer review criteria. Preserve catalog-specific checks as a separate review mode.
- Introduce pinned consumer adoption: metadata and footer match the copied asset bundle's VERSION, with the source commit recorded separately.
- Add Get started to catalog navigation and make the README and catalog introduction focus on creating documentation.

Existing 0.1.0 consumer pages can remain pinned. To adopt 0.2.0, use the matching stylesheet and VERSION, check shell classes against the starter, apply consumer review, and then update the declared version. No CSS selectors were removed by this release. Do not copy the catalog's eleven navigation destinations into an unrelated consumer suite.

## 0.1.0

Initial source-backed catalog, adopted pattern documentation, shared styles, interaction demonstrations, catalog review checklists, and local review-model experiments.
