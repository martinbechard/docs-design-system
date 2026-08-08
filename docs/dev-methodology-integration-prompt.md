# Prompt for the `dev-methodology` Owner

You are the source owner and maintainer of `/Users/martinbechard/dev/dev-methodology`.

Implement the approved Documentation Design System and its portable conformance-review workflow in `dev-methodology`. The purpose is to give methodology authors one versioned, reusable standard for creating consistent HTML documentation and an evidence-based way to verify that each page follows it.

This is a source-level methodology change only. Do not deploy, install, or publish the result into user-level skill or agent directories. When implementation and source verification are complete, return the evidence to the originating `/Users/martinbechard/dev/docs-design-system` Codex task for confirmation. Wait for that confirmation and explicit user approval before any user-level publication.

## Local Prototype and Evidence

Use this local project as the design candidate and evaluation evidence:

- `/Users/martinbechard/dev/docs-design-system/docs/design-system/`
- `/Users/martinbechard/dev/docs-design-system/skills/review-documentation-design-system/`
- `/Users/martinbechard/dev/docs-design-system/agents/documentation-design-system-checklist-runner.role.yaml`
- `/Users/martinbechard/dev/docs-design-system/agents/documentation-design-system-review-coordinator.role.yaml`
- `/Users/martinbechard/dev/docs-design-system/docs/portable-review-system-proposal.md`
- `/Users/martinbechard/dev/docs-design-system/evals/results/tournament-report.md`
- `/Users/martinbechard/dev/docs-design-system/evals/results/coordinator-tournament-report.md`

Treat these files as candidate inputs, not authoritative methodology sources. Adapt them to the repository's source schemas, catalogs, generators, terminology, and tests. Do not copy generated artifacts into source locations or hardcode provider model identifiers into reusable conceptual agent definitions.

## What Was Designed

The prototype contains a versioned, single-entry HTML documentation design system with an index and cross-cutting concern pages. It was derived by reviewing the existing `dev-methodology` HTML documentation for shared elements and inconsistent variations.

Preserve the intent and coverage of the prototype:

- Document the normal page shell, official `dev-methodology` brand and logo, page badges, document-sequence navigation, section navigation, and a link back to the page top.
- Establish the regular hero as the default with an inline example. Document the two-column hero as an intentional optional pattern, including when it is appropriate.
- Cover foundations, content, data display, forms and actions, accessibility and responsive behavior, diagrams, source inventory, and variation auditing.
- Give every variation its own subsection with an inline visual example, source-page attribution, advantages, disadvantages, and standardization status.
- Preserve the version number and the requirement that conforming pages declare the design-system version they target.
- Keep source-observed variations distinct from adopted standards. An audit example must not silently become a recommended pattern.
- Do not retroactively modify existing source documentation pages as part of this integration unless a separately authorized migration explicitly places those pages in scope.

The diagram standard must include reusable accessible SVG patterns, especially the connector and block-entry-arrow geometry:

- Keep connectors separate from short-stem block-entry arrows.
- End connectors at the beginning of the arrow stem; do not carry `marker-end` into a destination block.
- Make the stem length equal the arrowhead depth, align connector, stem, arrowhead, and block entrance on one centerline, and place the arrowhead tip on the block boundary.
- Provide reusable `<symbol>` and `<use>` examples for ordinary and stronger combined-flow arrows.
- Include explained Do and Don't examples for fan-out and fan-in layouts.
- Cover curve routing, intentional convergence, line weight, whitespace, label clearance, clipping, overflow, narrow-width rendering, `<title>`, and `<desc>` requirements.

## Portable Review Architecture

Implement the review mechanism as methodology-owned portable artifacts:

1. Create a reusable `review-documentation-design-system` skill with one shared checklist and one checklist for each design-system page type. Preserve unique stable checklist IDs and the evidence-backed `PASS`, `FAIL`, or `NOT TESTED` contract.
2. Create a deliberately small, read-only checklist-runner conceptual agent. It receives exactly one page and one checklist, uses the review skill, records every assigned item exactly once, cannot mutate files, cannot delegate, and does not make the integrated acceptance decision.
3. Create a read-only review-coordinator conceptual agent. It dispatches one page-checklist assignment per runner invocation, validates report completeness, reconciles and de-duplicates evidence, preserves contradictions, and alone returns `ACCEPTED`, `REJECTED`, or `BLOCKED` for the complete review.
4. Keep procedure in the skill and the coordinator. Do not duplicate the checklist methodology in the small runner definition.
5. Preserve the ranking policy used by the evaluation harness: accuracy first, then estimated cost with a plus-or-minus 15 percent equivalence tolerance, then wall-clock speed. Never invent a price for an unpriced model.

The local model tournaments established these candidate settings:

- Checklist runner: Luna medium is the fixed control. It achieved perfect final-fixture precision, recall, F1, verdict accuracy, and aggregate accuracy.
- Coordinator: Terra low scored 40 of 40 fields and tied GPT-5.5 high for accuracy while using fewer estimated credits and less time. Luna medium scored 39 of 40; Spark medium scored 37 of 40.

Represent these choices through the methodology's semantic model-profile sources and runtime mappings. If the existing semantic profiles cannot express the tested coordinator setting, propose or add the smallest appropriate semantic profile through the repository's normal source and generator workflow. Keep provider model IDs out of the conceptual role definitions.

## Required Methodology Integration

Follow the repository's current maintenance instructions and source-first ownership boundaries. At minimum:

1. Update the authoritative skill sources, conceptual agent definitions, model-profile sources or mappings where required, catalogs, suite/scenario declarations, and hand-authored methodology documentation.
2. Add all required schema, inventory, generator, installer, and regression-test coverage in the same change.
3. Regenerate every owned derivative, including supported Codex, Claude Code, Gemini CLI, and Junie CLI adapters and generated HTML/catalog data.
4. Confirm that each generated adapter preserves repository mutation authority, agent dependencies, skill assignment, output contracts, and semantic model mappings.
5. Keep the maintenance repository-local. Do not write to user-home skill or agent locations as a verification shortcut.

## Acceptance Checks

Demonstrate all of the following before requesting confirmation:

- Every checklist ID is unique and resolves from the skill.
- Every design-system page and page-type checklist is discoverable from the appropriate index.
- The runner loads only the required review skill, receives one checklist, remains read-only, cannot delegate, and reports each assigned checklist item exactly once.
- The coordinator depends on the runner, never substitutes its own checklist review, and correctly handles complete passes, confirmed failures, missing reports, malformed reports, unavailable runners, duplicate findings, and irreconcilable conflicts.
- Ranking tests cover accuracy precedence, the 15 percent cost-equivalence boundary, speed tie-breaking, cached-input accounting, and unpriced candidates.
- The HTML design-system pages render without broken navigation, clipping, or horizontal overflow at desktop and narrow widths.
- Meaningful diagrams have accessible titles and descriptions and pass the documented arrow and connector checks.
- Generated-output checks, Markdown and link checks, Agent Skill validation, repository regression tests, and `git diff --check` pass.

## Return for Confirmation Before Publication

When the source implementation is complete, do not publish it to the user level. Return a concise implementation dossier to the originating `docs-design-system` task containing:

- the commit hash and branch or worktree;
- the authoritative source files added or changed;
- the generated artifacts and the commands used to regenerate them;
- the exact semantic runner and coordinator profiles and every runtime mapping;
- the validation and regression commands run, with pass/fail totals;
- focused evidence for the runner and coordinator edge cases;
- browser-verification evidence for the design-system pages;
- any deviations from the prototype, with reasons;
- unresolved limitations, failed gates, or decisions requiring user approval.

Explicitly ask the originating task to confirm that the portable artifacts, generated adapters, documentation, tests, and publication boundary were implemented correctly. If you cannot contact that task directly, provide the complete dossier to the user with instructions to paste it back into the originating task.

Stop after source implementation and this confirmation request. User-level deployment or publication requires both confirmation from the originating task and a subsequent explicit user instruction.
