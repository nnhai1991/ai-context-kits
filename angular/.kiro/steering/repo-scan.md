---
inclusion: manual
---
# REPO SCAN — fill the Angular AI-context templates from this repository

# ROLE
Senior Angular architect performing a READ-ONLY scan. Do not modify source. Only create/overwrite files under `docs/ai/`
(and `.kiro/steering/` if docs/ai does not exist). Every non-placeholder value cites a file path, count, or command output.
If you cannot prove a fact, write `UNKNOWN – ask tech lead`. Never print secret values.

# TOOLS
Angular CLI MCP if available (`list_projects`, `get_best_practices`, `search_documentation`); `nx show projects` / `nx graph --file=docs/ai/graph.json` if Nx;
ripgrep (`rg`) for counts.

# STEP 1 — Inventory
package.json (+ packageManager, engines), lockfile, .nvmrc/.node-version, angular.json, **/project.json, nx.json, tsconfig*.json (angularCompilerOptions),
eslint.config.* / .eslintrc*, .prettierrc*, .editorconfig, .browserslistrc, src/main.ts, src/main.server.ts, server.ts, app.config*.ts, app.routes*.ts,
src/environments/**, proxy.conf.*, polyfills, .storybook/**, jest.config.*, vitest.config.*, karma.conf.*, test-setup.ts, playwright.config.*, cypress.config.*,
CI configs, CODEOWNERS, openapi*.{yaml,json}, **/generated/**, codegen.ts, orval.config.*, ng-openapi-gen.json, existing AI files (AGENTS.md, CLAUDE.md,
.claude/, .cursor/, .github/copilot-instructions.md, .github/instructions/, .windsurf/, .devin/, .junie/, .kiro/, GEMINI.md), docs/adr/**, README*, CONTRIBUTING*.
Hot files: `git log --since=6.months --name-only --pretty=format: | sort | uniq -c | sort -rn | head -50`.

# STEP 2 — Detection heuristics (report counts + 2 example paths each)
- Versions: @angular/core, @angular/cli, @angular/build vs @angular-devkit/build-angular, typescript, rxjs, zone.js, @nx/*.
- Builder: angular.json "builder" values. Standalone vs NgModule: `rg -c "@NgModule\("`; `standalone: false`; `rg -c "@Component\("`.
- Zoneless: zone.js in polyfills/package.json; `provideZonelessChangeDetection` / `provideZoneChangeDetection`; `NgZone`.
- Change detection: counts of `OnPush`, `.Default`, `.Eager`.
- DI: `inject(` vs constructor params; `@Service(` vs `@Injectable(`; `InjectionToken`.
- Signals vs RxJS: `signal(`, `computed(`, `linkedSignal(`, `effect(`, `toSignal(`, `httpResource(`, `rxResource(`, `resource(` vs `BehaviorSubject`, `.subscribe(`, `| async`, `takeUntilDestroyed`, `takeUntil(this.destroy`.
- Inputs/outputs: `input(`/`output(`/`model(` vs `@Input(`/`@Output(`; `viewChild(` vs `@ViewChild(`.
- Templates: `@if (`/`@for (` vs `*ngIf`/`*ngFor`/`*ngSwitch`; `ngClass`/`ngStyle`; `@HostBinding`/`@HostListener` vs `host:`.
- State: @ngrx/store (`createReducer`, `createEffect`, `createFeature`), @ngrx/signals (`signalStore(`, `withState(`, `rxMethod(`), @ngxs (`@State(`), Akita/Elf, services+signals (`signal(` inside injectable classes), facades (`class \w+Facade`).
- Smart/dumb: pages/, containers/, *-page.ts vs ui/, components/. Nx: libs/ tree, project.json tags, `@nx/enforce-module-boundaries` depConstraints.
- Forms: `@angular/forms/signals` / `form(` / `[formField]` vs `FormBuilder`/`NonNullableFormBuilder`/`FormGroup<` vs `ngModel`; `ControlValueAccessor` vs `FormValueControl`.
- HTTP: `provideHttpClient(` features; `HttpInterceptorFn` vs class interceptors; raw `fetch(`/axios; base URL tokens.
- Routing: `loadComponent`/`loadChildren`, functional vs class guards, `withComponentInputBinding`, `paramsInheritanceStrategy`.
- Errors: `implements ErrorHandler`, `provideBrowserGlobalErrorListeners`, `retry(`. i18n: `$localize`, `i18n` attrs, transloco, ngx-translate.
- UI: @angular/material (+version), @angular/cdk, @angular/aria, primeng, tailwind config, in-house lib.
- SSR: @angular/ssr, server.ts, `outputMode`, `provideClientHydration`, `withIncrementalHydration`, `isPlatformBrowser`, `afterNextRender`; raw `window.`/`document.`/`localStorage` occurrences.
- Tests: runner + config; `TestBed` vs `@testing-library/angular`; `HarnessLoader`; `fakeAsync`; `jasmine.` vs `vi.`/`jest.`; spec count vs component count.
- Naming: `*.component.ts` vs suffix-less ratio; selector prefixes. Security: `bypassSecurityTrust`, `innerHTML`, `localStorage.setItem(.*token`, secret-looking keys in environments.

# STEP 3 — Pick the exemplar feature
Score each feature folder: +3 has page+store/facade+api+mapper+ui+spec; +2 uses the dominant patterns; +2 modified in last 6 months; +1 e2e coverage;
-3 in legacy/deprecated; -2 lint warnings. Choose the highest; list runner-up. Never choose generated code. List every file per layer + 1–3 anti-exemplars.

# STEP 4 — Decide, don't guess
Dominant pattern = >=70% share -> rule. 30–70% -> "MIXED: new code uses {{X}} (ask)" + questions.md. Security/architecture items without evidence -> UNKNOWN.

# STEP 5 — Output
1. `docs/ai/scan-report.md`: versions, counts with evidence, architecture + confidence, exemplar + score, risks (legacy islands, SSR hazards, security), existing AI files and conflicts.
2. Filled `docs/ai/*.md`: product (facts only), tech, structure, architecture, conventions, testing, api-contracts, exemplars, angular-api-guardrails, security. Always-loaded files <= ~120 lines.
3. `docs/ai/questions.md` "UNKNOWN – ask tech lead": numbered; why it matters; options observed; recommendation. Always include: new-dependency policy; forms style for NEW code; signals-vs-RxJS policy; test runner for NEW specs; token storage; legacy islands policy; target pattern for NEW code if mixed.
4. Then STOP and print a summary. Do not start feature work.

# STEP — Build the code index (after the scan, before any feature work)
Follow `docs/ai/code-index/prompts/build-code-index.md` and `docs/ai/code-index/PLATFORM.md`. Generate with
`python3 scripts/ai/build_code_index.py --platform angular --root . --out docs/ai/code-index` (every file gets a row, flows from each routed component,
contracts with all parties; with Nx, mirror depConstraints in `rules/allowed-edges.json`). Then: fix entry points and rules, write one-line summaries in
`annotations.json` (exemplar → hotspots → shared files → the rest), write invariants on flow, directory and promoted component cards, and make
`build_code_index.py --check` pass. Design work must run `prompts/impact-analysis.md` (`query_code_index.py impact`) first.
