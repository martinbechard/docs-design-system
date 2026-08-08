# Source Inventory Checklist

| ID | Observable pass criterion | Required evidence |
| --- | --- | --- |
| DDS-INV-001 | The hero names the repository, full source commit, and audit date; those values identify an available immutable snapshot. | Exact values plus successful revision-resolution evidence. |
| DDS-INV-002 | The primary-page table contains all 11 audited documentation pages and, for each, records source path, theme, section-navigation family, and distinctive elements. | Row/column inventory compared with tracked HTML at the declared commit. |
| DDS-INV-003 | The styled backlog report is classified as a tracked output example, lists its contributions, and explicitly excludes brand header, sequence, hero, section navigation, shared settings, and footer from its boundary. | Report card text and source inspection. |
| DDS-INV-004 | Exactly four fixtures are classified as test sources, with source path, purpose, and represented elements; the negative accessibility fixture is not classified as production styling. | Fixture table inventory and source inspection. |
| DDS-INV-005 | Element coverage includes metadata/viewport; skip/header/brand/main/sections/navigation/hero; `h1`–`h4` and prose semantics; lists; articles/asides/cards/panels/callouts/notes; code/trees; tables; metrics/labels; forms/actions/live feedback/dialog; figures/SVG/CSS diagrams/object fallback; and responsive/print behavior. | Coverage-list mapping to live examples in the nine concern pages. |
| DDS-INV-006 | The audit method lists tracked `*.html`, compares tracked and live files, classifies each surface, extracts semantic/style/asset/script data, inspects unique/accessibility structures, and records common patterns and variations with sources, pros, and cons. | Ordered method steps and reproducible command/output evidence. |
| DDS-INV-007 | Counts reconcile to 16 total tracked HTML files: 11 primary pages, one report example, and four fixtures, with no duplicate or unclassified path. | Machine-readable tracked-file list and one-to-one classification reconciliation. |
| DDS-INV-008 | Every source path exists at the declared commit, and every stated distinctive element, count, theme, navigation type, or behavior is directly observable there. | Per-row source evidence or deterministic extraction output. |
| DDS-INV-009 | The page records exclusions and unrelated worktree state truthfully without reading, modifying, staging, or overwriting excluded content. | Audit command scope, worktree status, and exact visible boundary statement. |
