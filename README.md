# Dúnedain Data Atlas — complete source export

This ZIP contains the application source from commit `7c2b2c527c75c7828093ade7ceb5a94d7affcdd6`, with export documentation and analytical SQL schema added. The live Site is not modified by this export.

## Contents

- `app/`: server-rendered route, layout, error pages and optional ChatGPT authentication helpers.
- `components/`, `hooks/`, `lib/`, `vendor/`: application, chart, genealogy, SQL editor and UI source.
- `public/`: all tracked public assets, including the DuckDB worker/WASM, CSV/JSON/Parquet data, favicon and existing source-download ZIP.
- `data/raw/`, `analytics/`, `notebooks/`: source facts, curation, validation and analytical transformations.
- `database/schema.sql`, `database/load.sql`: the 13 analytical tables, two views and loading statements for DuckDB.
- `db/`, `drizzle/`, `drizzle.config.ts`, `examples/d1/`: original optional D1 scaffolding. `db/schema.ts` is intentionally empty; the running atlas does not use a hosted transactional database. The notes API under `examples/` is an example, not an active endpoint.
- `package.json`, `pnpm-lock.yaml`, `pnpm-workspace.yaml`, `.npmrc`: dependency manifest, exact lockfile and package-manager policy.
- `vite.config.ts`, `next.config.ts`, `postcss.config.mjs`, `tsconfig.json`, `build/`, `scripts/`: complete build configuration and server build integration.
- `tests/`, `.github/workflows/validate.yml`: regression tests and CI.
- `LICENSE`, third-party license files and data source citations.
- `.env.example`: intentionally empty because this app has no required application environment variables.

Installed dependencies, build outputs, Git history, local caches, logs, actual environment files and hosting credentials are excluded. `.openai/hosting.json` keeps the no-database/no-storage configuration but removes the original Site identifier. The bundled `public/data/source.zip` is the existing public download; this outer export has the additional installation/deployment documentation and SQL schema.

## Installation

Use Node.js 22.13 or newer (a supported Node LTS), pnpm 11.25.0 as pinned in `package.json`, and Python 3.10+ only if rebuilding or validating the data. The checked-in data lets the website run without Python. WSL is suitable for Windows users running the provided shell helpers.

Extract this archive and enter its `dunedain-data-atlas` directory. Install pnpm 11.25.0 through your preferred package-manager installation method; if Corepack is available:

```sh
corepack enable
corepack prepare pnpm@11.25.0 --activate
pnpm install --frozen-lockfile
pnpm dev
```

The portable development script uses port 5173. No `.env` file, API key or database credentials are needed. The scripts' optional tool/runtime settings already have defaults and are not required variables.

For the Python analysis tools:

```sh
python -m venv .venv
# macOS/Linux/WSL:
. .venv/bin/activate
# Windows PowerShell alternative: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python analytics/pipeline.py
```

`data/raw/` is the source of truth. `analytics/seed.py` followed by its curation step reproduces the initial transcription; do not run it over intentional manual data edits. Normal rebuilds use `analytics/pipeline.py`.

## Validate

```sh
python -m unittest discover -s analytics/tests -v
node tests/app-logic.mjs
node tests/render-app.cjs
node tests/sql-engine.mjs
pnpm exec tsc --noEmit
pnpm build
```

The automated test suite validates data transformations, relational integrity, server-rendered routes, internal links and the WebAssembly SQL engine. Browser interaction, keyboard navigation, responsive layouts and reduced-motion states are verified against the local development server.

## Production build and local smoke test

```sh
pnpm build
pnpm start
```

The build produces a Cloudflare Worker at `dist/server/index.js`, a generated `dist/server/wrangler.json`, and static assets in `dist/client/`. The start command runs the generated Worker locally through Wrangler; use the address printed by the command. Keep `dist/server` and `dist/client` together. This project uses the Next App Router API through Vinext; it is not a standard `next start` or Vercel package.

## Deploy to your Cloudflare Workers account

Create/use your own Cloudflare account, authenticate locally, build, then deploy the generated configuration:

```sh
pnpm exec wrangler login
pnpm build
pnpm exec wrangler deploy --config dist/server/wrangler.json --name dunedain-data-atlas
```

Use a different Worker name if that name is already used in your account. The generated configuration includes the Worker entry point, asset binding and Node compatibility flags. No D1/R2 resources or database migrations are required for this app. Do not commit Wrangler login state or credentials; interactive login stores them outside the source archive.

The original ChatGPT Site's owner-only access policy is platform-managed and is not portable. A Worker deployed to your own account does not inherit it. Configure Cloudflare Access before exposing the deployment if you need equivalent restricted access. The app does not call the bundled optional ChatGPT user-header helpers; those headers must not be treated as authenticated identity on an untrusted standalone deployment.

## Import into ChatGPT Sites

Provide the extracted source to Sites and create/select the destination Site through its normal publishing flow. Have Sites assign the destination project identifier; never copy credentials or an existing private project's identity into another deployment. The included `.openai/hosting.json` declares no D1 or R2 bindings. Build and publish through Sites to restore its platform-managed hosting/access controls. Publishing requires access to your own destination account; none is included in this ZIP.

## Use the analytical schema separately

The browser automatically creates its local DuckDB tables from the shipped Parquet assets. To reproduce them with a separately installed DuckDB CLI, run from the project root on a new database:

```sh
duckdb atlas.duckdb < database/schema.sql
duckdb atlas.duckdb < database/load.sql
```

The schema/load pair is for a fresh database, not an idempotent migration. `ruler_reigns` contains 129 tenures; `rulers` contains 125 officeholders; `persons` includes 28 additional connecting relatives. No live user database or private data exists to export.

## Export verification

`EXPORT-MANIFEST.json` lists a SHA-256 digest for every included file except the manifest itself. No application secrets are required. Environment files, private hosting metadata and credential-bearing package-manager settings were excluded or sanitized. Source and dependency licenses remain in place.

---

# Dúnedain Data Atlas

An independent analytical portfolio by Zendevve: 125 rulers plus 28 connecting relatives, 129 tenures, seven political institutions. The app explores referenced records through a timeline, ruler explorer, individual profiles, six analyses, comparisons, a curated lineage graph and a real DuckDB-Wasm SQL lab.

## Local development

Node 22.13+ and Python 3.10+ are required.

```sh
corepack pnpm install --frozen-lockfile
python -m pip install -r requirements.txt
python analytics/pipeline.py
python -m unittest discover -s analytics/tests -v
node tests/sql-engine.mjs
node tests/app-logic.mjs
node tests/render-app.cjs
pnpm dev
```

The Sites checkout uses pnpm; its lockfile pins the hosted build. Outside Sites, install using pnpm for identical dependencies. The frontend uses React, TypeScript, the Next App Router API through Vinext, Tailwind and the included accessible UI primitives. It builds a Cloudflare Worker for Sites hosting. It is not a Vercel deployment.

## Reproducible data

`data/raw/` is the source of truth. `analytics/seed.py` documents the initial manual transcription and is not required for normal rebuilds. Edit normalized records directly, then execute `analytics/pipeline.py`. It validates relational references, chronology and field provenance before producing Parquet, CSV, JSON and the frontend bundle. `analytics/tests/` exercises cross-age calculations, interrupted reigns, exceptional records and acyclic parentage.

Tables: persons, aliases, houses, realms, offices, reigns, relationships, events, sources and field_sources. Derived marts: mart_ruler_reigns, mart_realm_summary and mart_succession. SQL aliases `rulers` and `ruler_reigns` are provided.

The browser initializes DuckDB only after Run is selected, registers local Parquet files, disables external access and accepts one SELECT/WITH statement. The loader accepts both the original gzip asset and WASM already decompressed by HTTP content encoding. Results are capped at 1,000 rows. A 20-second timeout terminates expensive queries and resets the worker (60 seconds on initial engine load). The SQL-engine integration test runs the actual WebAssembly build against all 13 Parquet tables. Regression checks cover filters and accent-insensitive search, read-only SQL validation, all example queries, failure recovery, the result limit, engine asset integrity, and server rendering of all 161 routes with 167 internal links/download targets. Browser checks additionally exercise real query execution, keyboard submission, cancellation and restart, empty results, and both WASM delivery formats.

## Method and exclusions

Year-level chronology adds 3441 for TA and 6462 for FA; durations are end minus start. First Age births are not normalized. The Fourth Age boundary is a year-level approximation, not exact calendar arithmetic. A person is distinct from a tenure. Eldacar's ten-year exile is excluded. Overlapping southern co-rulers and overlordship, usurpers, titular rule and Aranarth's uncertain accession are excluded from default descriptive summaries. All remain inspectable.

Source tables were checked against secondary references, with underlying primary works cited for subsequent edition-level review. No claim is made of a full primary-source audit. All 125 ruler life records and ancestral branches are reviewed, with 123 known lifespans. Eärnur and Ar-Pharazôn retain unresolved death dates. Supporting relatives connect collateral branches; ancestor edges preserve unnamed intervening generations. Elros and Aragorn use reported lifespans of 500 and 210. The event list is selective and is not a measure of importance. No causal or predictive claims are made.

## Routes

`/`, `/timeline`, `/rulers`, `/rulers/[slug]`, `/analysis`, `/compare`, `/lineage`, `/sql`, `/methodology`.

## Interface behavior

The archive keeps data and navigation immediate: charts, filtering, sorting and lineage selection do not animate. Shared interaction tokens live in `app/globals.css`; pointer presses receive subtle feedback, while occasional selects and filter sheets use short, origin-aware motion. Keyboard interactions are instant, reduced motion removes spatial movement, and hover styling is limited to fine pointers.

Keyboard focus remains visible across search, navigation and SVG controls. Escape closes mobile navigation or the filter sheet and returns focus to its trigger. Empty ruler searches offer an inline reset. Timeline zoom controls indicate their limits, and the last-inspected caption never describes a filtered-out tenure.

The SQL editor distinguishes engine loading, execution, cancellation, errors and results. Query changes clear previous results; execution keeps the editor read-only until completion or cancellation. CSV feedback reports download initiation, not completion.

For browser QA, exercise the main routes at desktop and narrow mobile widths, then repeat keyboard navigation and filter-sheet/select interactions with reduced motion enabled. Physical-device touch and screen-reader testing remain separate checks from Chromium emulation.

## Source attribution

Tolkien Gateway institutional lists (accessed 2026-09-28) and Zarkanya's Appendix 1 recorded Númenórean life dates; source URLs and field associations are included in `data/raw/sources.json` and `field_sources.json`. No estimated Andúnië lifespans or narrative prose are imported. Raw data and derivatives are distributed under CC BY-SA 4.0 with attribution; application source is MIT licensed. Tolkien's underlying works, names and trademarks remain those of their respective owners.

Unofficial educational project. Not affiliated with the Tolkien Estate or adaptation rights holders.

## Current coverage limits

The seven principal institutions are represented, including all 26 Ruling Stewards. Faramir's short transitional stewardship is excluded from that count. Cardolan/Rhudaur royal fragments, genealogy beyond the included rulers and their connecting ancestors, complete event curation and an independent primary-edition audit remain outside this release. No fabricated records fill those gaps.
