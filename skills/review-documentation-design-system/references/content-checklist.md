# Content Page Checklist

| ID | Observable pass criterion | Required evidence |
| --- | --- | --- |
| DDS-CNT-001 | Text hierarchy demonstrates page, section, subsection, and boundary headings; an opening lede; focused body paragraphs; meaningful strong text; visual-only bold; links; exact inline code; and secondary small text. | DOM inventory and rendered specimen screenshot. |
| DDS-CNT-002 | Ordered lists represent sequences, unordered lists represent sets, and description lists pair stable terms with definitions. | One semantic DOM example of each plus content showing the stated role. |
| DDS-CNT-003 | Inline `code` is reserved for exact names, while `pre` blocks preserve commands, configuration, templates, or directory structure without truncation or lost whitespace. | DOM/source evidence and narrow-width rendering for each code treatment. |
| DDS-CNT-004 | Cards are independently scannable peer concepts, panels remain supporting parts of a parent section, and self-contained entries use `article`; a linked card exposes one unambiguous navigation target. | Role/content classification and DOM inspection for all specimens. |
| DDS-CNT-005 | Callouts state important boundaries, warning callouts identify unresolved decisions or risk, notes remain secondary, and asides contain related non-narrative information. | Visible examples and semantic element/class evidence. |
| DDS-CNT-006 | Optional detail uses native `details`/`summary` and is operable by keyboard with an observable open/closed state. | DOM evidence and keyboard interaction trace. |
| DDS-CNT-007 | The page visibly identifies source provenance for code blocks and component families and does not present unresolved variation examples as adopted contracts. | Source-path inventory and classification check. |
