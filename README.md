# Documentation Design System

Create consistent, accessible HTML documentation with shared styles, reusable page patterns, and practical authoring guidance. This repository provides the reference catalog, a working starter, a completed example, and local agent skills for creating and reviewing pages.

**[Explore the live design system](https://martinbechard.github.io/docs-design-system/)** · **[Create your first page](https://martinbechard.github.io/docs-design-system/getting-started.html)**

## Create a Page

The system uses plain HTML and CSS. Static pages need no build step or JavaScript.

1. Clone this repository and open its root directory.
2. Copy the [starter](docs/design-system/templates/page.html), shared stylesheet, and matching version file into a new documentation folder using the commands below.
3. Replace the starter's title, branding, navigation, and content. Use [page-shell guidance](https://martinbechard.github.io/docs-design-system/page-shell.html) and select components that help your reader.
4. Preview locally and review both source and rendered behavior before publishing.

```sh
git clone https://github.com/martinbechard/docs-design-system.git
cd docs-design-system
mkdir ../my-docs && mkdir ../my-docs/assets && \
cp docs/design-system/assets/design-system.css ../my-docs/assets/ && \
cp docs/design-system/VERSION ../my-docs/assets/VERSION && \
cp docs/design-system/templates/page.html ../my-docs/index.html && \
python3 -c 'from pathlib import Path; p=Path("../my-docs/index.html"); p.write_text(p.read_text().replace("../assets/", "assets/"))'
git rev-parse HEAD
python3 -m http.server 8000 --bind 127.0.0.1 --directory ../my-docs
```

Use a fresh destination name if `my-docs` already exists. Record the printed commit with your copied assets. Open `http://localhost:8000/`; stop the server with Ctrl+C. The [authoring guide](https://martinbechard.github.io/docs-design-system/getting-started.html) explains the complete workflow, and the [completed example](https://martinbechard.github.io/docs-design-system/examples/first-page.html) shows a realistic consumer document.

The supported shell uses `.ds-header`, `.ds-footer`, and `.page-nav`. A consuming project supplies its own branding and navigation. Catalog demonstrations and unresolved variations are reference material; the catalog's JavaScript does not provide a general application runtime.

## Use with an Agent

These skills are repository-local. They are not automatically installed into an agent runtime. Keep the complete checkout available because the skills reference the catalog and each other by relative path.

| Skill | Purpose |
| --- | --- |
| [create-documentation-page](skills/create-documentation-page/SKILL.md) | Create or update a consumer document from project sources using the starter and adopted components. |
| [review-documentation-design-system](skills/review-documentation-design-system/SKILL.md) | Review source and rendered behavior in consumer or catalog mode. |

Example requests from this checkout:

> Read `skills/create-documentation-page/SKILL.md` and create an onboarding guide from the supplied project sources. Write it to my project's documentation folder and review it in consumer mode.

> Read `skills/review-documentation-design-system/SKILL.md` and review my HTML document in consumer mode against its pinned asset version.

Consumer reviews check the page's own navigation and components. Catalog reviews additionally check reference specimens, adoption decisions, and historical audit evidence. A source-only review cannot establish visual or keyboard conformance; missing required evidence remains `NOT TESTED`.

## Versions and Adoption

The current version is recorded in [VERSION](docs/design-system/VERSION). Version 0.2.0 is a usable draft before 1.0.0. Copy assets from one selected checkout and retain its source commit. Each consumer page's metadata and visible footer must match its copied asset version; existing consumers do not automatically upgrade when this repository changes.

Review the [changelog](CHANGELOG.md) before replacing assets. Apply required markup changes and verify the page before changing its declared version. The [versioning contract](https://martinbechard.github.io/docs-design-system/page-shell.html#versioning) explains compatibility rules.

## Repository Layout

```text
docs/design-system/
├── index.html              # Catalog entry point
├── getting-started.html    # Authoring and adoption guide
├── templates/page.html     # Minimal consumer starter
├── examples/first-page.html # Completed consumer example
├── assets/                 # Shared CSS and catalog demonstrations
└── VERSION                 # Current asset/contract version
skills/
├── create-documentation-page/
└── review-documentation-design-system/
agents/                     # Local review-runner and coordinator definitions
evals/                      # Review-model experiments and historical results
scripts/                    # Static documentation checks
```

The remaining catalog HTML pages cover foundations, shell, content, data display, forms, diagrams, accessibility, source variations, and provenance.

## Preview, Validate, and Contribute

Preview the catalog from the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory docs/design-system
```

When changing an adopted pattern, update its reference, starter or example where applicable, review criteria, version, and changelog together. Preserve the distinction between adopted contracts and historical source variations. Run the static checks:

```sh
python3 scripts/check_docs.py
python3 -m unittest scripts.test_check_docs
python3 -m unittest discover -s evals -p 'test_*.py'
git diff --check
```

The checker verifies local links and fragments, duplicate IDs, version agreement, and catalog navigation consistency. It does not replace rendered desktop/narrow, keyboard, interaction, or content review.

The [Pages workflow](.github/workflows/pages.yml) runs static checks and publishes `docs/design-system/` on every push to `main`. It also supports manual runs. Other repository folders are not published by that workflow.

## Review Research and Integration

The [evaluation documentation](evals/README.md) describes the review-runner and coordinator experiments, ranking policy, and historical model results. Those experiments support review research; they are not prerequisites for authoring a page or evidence that every current page conforms.

The design system originated in an audit of `dev-methodology` documentation. The [source inventory](https://martinbechard.github.io/docs-design-system/source-inventory.html) preserves that provenance. [Portable review-system integration](docs/portable-review-system-proposal.md) remains a separate proposal; local authoring and review work does not install or modify anything in `dev-methodology`.
