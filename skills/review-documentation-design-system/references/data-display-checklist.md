# Data Display Page Checklist

| ID | Observable pass criterion | Required evidence |
| --- | --- | --- |
| DDS-DAT-001 | A table is used only for records sharing the same fields and includes semantic headers; wide tables retain native table display inside a dedicated horizontal-overflow wrapper. | Table DOM, header association, computed display, wrapper overflow, and narrow viewport evidence. |
| DDS-DAT-002 | Each metric has exactly one prominent value and one short interpretation and is used for a count, ratio, limit, or current state. | Metric DOM/content inventory. |
| DDS-DAT-003 | Statuses, badges, and tags are non-interactive labels whose visible text carries verdict, workflow-state, or taxonomy meaning without relying on color. | Role/link audit, text/color comparison, and accessibility-tree evidence. |
| DDS-DAT-004 | Pill-shaped navigation remains an anchor and is not mislabeled or implemented as a status/badge. | DOM evidence for every pill-shaped interactive specimen. |
| DDS-DAT-005 | Catalog cards contain repeated narrative records that need more content than table cells and expose a consistent record structure across peers. | Field/content mapping across all catalog specimens. |
| DDS-DAT-006 | Structured metadata uses a description list with explicit term/value pairs instead of prose forced into a comparison table. | `dl`/`dt`/`dd` DOM inventory and visible rendering. |
| DDS-DAT-007 | Source notes identify the observed metric, table, and compact-label families and explicitly acknowledge unresolved naming/overflow variants. | Visible source and variation statements. |
