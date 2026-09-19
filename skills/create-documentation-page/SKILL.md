---
name: create-documentation-page
description: Create or update a consumer HTML documentation page using this repository's adopted design-system patterns, shared stylesheet, and starter. Use for project guides, reference pages, and documentation landing pages; not for changing the design system itself or running review-model tournaments.
---

# Create Documentation Page

Create a useful document for its audience, then verify its use of the design system. Keep this skill in the repository: its relative dependencies are part of the package contract.

## Inputs

Establish the audience, task or topic, authoritative content sources, destination, new-page or update scope, and adopted design-system version. For a suite, identify its existing navigation and asset layout. Ask only for missing information that materially affects the result; do not invent project behavior or overwrite an unrelated page.

## Workflow

1. Read the [authoring guide](../../docs/design-system/getting-started.html), [page shell](../../docs/design-system/page-shell.html), and the adopted version's `VERSION`. For an existing consumer, use its pinned assets and matching references; do not silently upgrade it to this checkout. If matching version references are unavailable, report the gap before claiming conformance.
2. For a new page, start from the [consumer starter](../../docs/design-system/templates/page.html). Use the [completed example](../../docs/design-system/examples/first-page.html) to understand composition. Copy the stylesheet and version file from the same source checkout into the target's asset layout; adjust relative URLs and record the source commit. Do not copy the entire catalog or its navigation into a consumer site.
3. Write source-backed content with one page purpose and a clear heading structure. Choose only necessary adopted components from the [content](../../docs/design-system/content.html), [data display](../../docs/design-system/data-display.html), [diagram](../../docs/design-system/diagrams.html), and [interaction](../../docs/design-system/forms-and-actions.html) references. Unresolved examples in the variation audit are not adopted patterns.
4. Preserve the supported `.ds-header`, `.ds-footer`, `.page-nav`, skip-link, hero, and main-landmark structure. Use project-specific text branding or an appropriate logo. Single pages need no suite navigation; multi-page suites use their own stable destinations and current-page marker. Sequence links require an actual reading sequence.
5. Replace starter instructions with finished content. Keep accurate copyright and source provenance. Match the exact metadata/footer version to the adopted assets, not the repository's newest version.
6. Use native HTML behavior when sufficient. The catalog's JavaScript is demonstration code, not a reusable application runtime. Implement and test any custom interactions needed by the consumer; do not imply persistence, uploads, or other behavior that is not implemented.
7. Preview locally using the guide. Check links and fragments, desktop and narrow rendering, keyboard operation, and applicable interactions. Apply [review-documentation-design-system](../review-documentation-design-system/SKILL.md) in `consumer` mode to the final page. That skill owns the conformance criteria and evidence format. Correct failures and repeat the affected checks; missing browser evidence remains `NOT TESTED`.

## Result

Return the page and asset paths, adopted version and source commit, content-source references, review result and evidence, and any remaining limitations. Do not claim conformance from source checks alone. Publishing is a separate action governed by the user's task scope.
