# Angular AI-Context Template Kit: Steering, Specs, Repo-Scan and Portability (October 2026)

The safest way to get correct AI-generated code in an existing Angular repo is to treat the repo as the source of truth: scan first, record findings in version-aware steering files, and only then let Angular's official guidance fill gaps. Angular 22's "modern defaults" (OnPush, Signal Forms, `@Service()`, zoneless, Vitest, suffix-less names) differ enough from what most repos contain that an agent following angular.dev alone will break legacy code, and an agent following its training data alone will write 2023-era Angular. The kit mirrors the iOS and Android kits.

## TL;DR

- **Verified 2026 baseline:** Angular 22 (June 3, 2026; angular.dev builds at v22.2.x) requires TypeScript 6 and Node 22+; OnPush is the default change-detection strategy (old default renamed `Eager`); `strictTemplates` on by default; HttpClient uses Fetch by default (`withXhr()` to keep XHR); Signal Forms and `resource()/rxResource()/httpResource()` are stable; `@Service()` and `injectAsync()` added; router `paramsInheritanceStrategy` defaults to `'always'`. Zoneless and Vitest are defaults for new projects since v21; suffix-less file names since v20; `*ngIf/*ngFor/*ngSwitch` deprecated since v20 (still present). All of these are "new projects only" or "migration-preserved" defaults, so the template detects them rather than assumes them.
- **Structure:** small always-on core (`product`, `tech`, `structure`, `angular-api-guardrails`), everything else `fileMatch`/`auto`. EARS specs with a Saved Payment Methods example; three hooks; Angular CLI MCP server wired in so the agent can verify APIs (`search_documentation`, `get_best_practices`).
- **Precedence rule the kit encodes:** task/spec > repo steering + exemplar > angular.dev / MCP > model memory. Plus "never modernize by side effect".

## Key Findings

| Fact (Oct 2026) | Why it matters |
|---|---|
| Angular 22 current; TS 6; Node 22+ | `{{ANGULAR_VERSION}}`/TS version read from `package.json`, never assumed |
| OnPush default in v22; `ng update` annotates legacy components with `ChangeDetectionStrategy.Eager` | Agents must not delete `Eager` as "noise" |
| Zoneless stable since 20.2, default for new apps since 21 | Scan checks `zone.js` in polyfills/package.json |
| Signal Forms stable in 22 (experimental in 21) | Forms style is a per-repo decision |
| `@Service()` requires `inject()`; `provideHttpClient()` optional since 21 | Generated services must match repo style |
| Vitest default since 21; Karma supported; `refactor-jasmine-vitest` schematic | Test steering filled from scan |
| Official AI assets: angular.dev best-practices prompt + per-IDE rules, `llms.txt`, Angular CLI MCP (`ng mcp`), `angular/skills` (`angular-developer`, `angular-new-app`) | Framework-knowledge layer; ranked below repo rules |
| Kiro: foundation files always included; `fileMatch` reportedly broken for *global* steering (#9176); hooks are `.kiro.hook` JSON (#4573) | Keep fileMatch files in workspace; use `.kiro.hook` extension |
| Nx `configure-ai-agents` may overwrite a CLAUDE.md that only imports `@AGENTS.md` (#37181) | Check your Nx version before running it |

---

## 1. Prioritized checklist (P0 = won't compile/breaks architecture/insecure; P1 = fails review; P2 = polish)

### 1A. Project facts
| P | Item | Failure without it |
|---|---|---|
| P0 | Angular version (exact) | `@Service()` in v20; `*ngIf` in lint-strict v22 |
| P0 | TS version + strict flags | Fails `tsc` |
| P0 | `angularCompilerOptions` (`strictTemplates`, `extendedDiagnostics`) | Templates fail in CI |
| P0 | Standalone vs NgModule counts | Wrong declaration model |
| P0 | Zoneless vs zone.js | UI silently doesn't refresh |
| P0 | Package manager + lockfile + Node version | Corrupted lockfile |
| P0 | Monorepo tool (Nx/CLI/none), project names | Code in wrong project; wrong commands |
| P0 | Builder per target | Webpack config suggested in esbuild app |
| P1 | angular.json projects/configurations/file replacements | Hard-coded env values |
| P1 | SSR/prerender/hydration | `window` crashes server render |
| P1 | Environment/runtime config strategy | Secrets in bundle |
| P2 | Polyfills, browserslist | Unsupported APIs |

### 1B. Architecture rules
| P | Item | Failure |
|---|---|---|
| P0 | State pattern (NgRx Store / SignalStore / NGXS / Akita / services+signals / RxJS services) | Second state system invented |
| P0 | Layering + dependency direction; Nx tags | Forbidden imports; boundary lint fails |
| P0 | Folder layout by feature | Files in `src/app/` root |
| P0 | DI style (`inject()` vs constructor; `@Service` vs `@Injectable`; tokens) | `@Service` with constructor params (invalid) |
| P0 | Routing (lazy, functional guards, route providers, input binding) | Eager imports; class guards in functional repo |
| P0 | Smart/presentational split, facades | HTTP in presentational components |
| P1 | Signals vs RxJS policy | Leaks; lost cancellation |
| P1 | Forms style; custom controls | Untyped forms; mixed systems |
| P1 | HTTP layer (interceptors, base URL token, generated client) | Bypassed auth; duplicate toasts |
| P1 | Error handling (ErrorHandler, interceptor, retry) | Swallowed/double errors |
| P1 | i18n mechanism | Hard-coded strings |
| P1 | Design system (Material/CDK/Aria/PrimeNG/Tailwind/in-house) | Hallucinated Material inputs |
| P1 | Accessibility baseline | Clickable `<div>`s |

### 1C–1H (conventions, code context, contracts, quality gates, security, process)
- **Conventions (P0):** file naming (suffix-less vs suffixed), selector prefix, ESLint config (`prefer-control-flow`, `prefer-inject`, `prefer-signals`, `no-uncalled-signals`). **P1:** `@if/@for` with `track`; signal inputs/outputs/queries; `host: {}`; `[class.x]` not `ngClass`; CD annotation policy (keep `Eager`); `protected` template members; **P2:** Prettier, import order, path aliases.
- **Existing code (P0):** golden-path exemplar slice (route → page → facade/store → API → HttpClient → DTO → mapper → model → presentational → tests); `app.config.ts`/`main.ts`/`app.routes.ts`; shared infra (auth, interceptors, shell, notifications, logger). **P1:** design-system public API; testing utilities. **P2:** legacy "do not touch" zones.
- **Contracts (P0):** OpenAPI/GraphQL source + generator + regen command; DTO vs model + mapper location. **P1:** base URL token / runtime config; feature flags. **P2:** error envelope, pagination, money/date formats.
- **Quality gates (P0):** unit runner + exact command; build/lint/test/e2e/typecheck/format commands; DoD. **P1:** TestBed vs Testing Library, harnesses, `HttpTestingController`, zoneless test setup; e2e selector policy; coverage + bundle budgets. **P2:** Storybook, Lighthouse, visual regression.
- **Security (P0):** never bypass sanitization; token storage policy (no `localStorage`); no secrets in `environment.ts`/bundle; PCI/PII rules. **P1:** CSP/Trusted Types; dependency policy + audit.
- **Process (P0):** EARS → design → tasks with requirement IDs; stop-and-ask rules. **P1:** task granularity; commit conventions. **P2:** "don't modernize untouched code" policy.

---

## 2. Kiro file set (shipped in this kit)

`docs/ai/` canonical → `.kiro/steering/`: `product`, `tech`, `structure`, `angular-api-guardrails` (always); `architecture` (fileMatch `**/*.ts`, `angular.json`, `nx.json`, `project.json`); `conventions` (`**/*.ts`, `**/*.html`, `**/*.scss`); `testing` (`**/*.spec.ts`, e2e); `api-contracts` (`**/data-access/**`, `**/api/**`, generated); `exemplars` and `security` (auto); `repo-scan` (manual). Specs in `.kiro/specs/_template/`; hooks in `.kiro/hooks/*.kiro.hook`; MCP config in `.kiro/settings/mcp.json`.

Design note: Kiro always includes AGENTS.md, so the "always" rules appear twice if AGENTS.md is generated into the same repo. Either let the generator skip always-rules in `.kiro/steering/` or add `AGENTS.md` to `.kiroignore`. The kit keeps the three foundation files as real Kiro steering (recommended) — if you also commit AGENTS.md for other tools, add it to `.kiroignore`.

---

## 3. Tool portability

| Tool | Location | Scoping | Quirks |
|---|---|---|---|
| **Kiro** | `.kiro/steering/*.md`; `~/.kiro/steering/`; specs; hooks `*.kiro.hook` | `inclusion` modes; `fileMatchPattern`; `#[[file:…]]` | Workspace > global; AGENTS.md always included; custom agents need `resources`; global fileMatch bug |
| **Claude Code** | `CLAUDE.md`, `.claude/rules/**/*.md` | `paths:` only | `@AGENTS.md` import pattern |
| **Cursor** | `.cursor/rules/*.mdc`; AGENTS.md | `description`/`globs`/`alwaysApply` | Plain `.md` ignored; `alwaysApply` overrides globs |
| **Copilot** | `.github/copilot-instructions.md`; `.github/instructions/*.instructions.md`; AGENTS.md | `applyTo`, `excludeAgent` | Path-specific only for cloud agent + code review on GitHub.com |
| **AGENTS.md** | root + nested | plain markdown; nearest wins | 60k+ projects; Linux Foundation (AAIF) |
| **Windsurf/Devin** | `.devin/rules/*.md` (preferred) | `trigger`, `globs` | 12,000 chars/workspace rule file; 6,000 global |
| **Junie** | `.junie/AGENTS.md` (exclusive) → root AGENTS.md + `.junie/rules/*.md` → legacy `.junie/guidelines.md` | plain | `.junie/AGENTS.md` silently shadows root |
| **Angular official** | angular.dev best-practices prompt, per-IDE rules, `llms.txt`, `ng new --ai-config` | generic, version-current | Knows nothing of your architecture; rank below repo rules |
| **Angular CLI MCP** | `npx -y @angular/cli mcp` in `.kiro/settings/mcp.json`, `.cursor/mcp.json`, `claude mcp add` | tools: `ai_tutor`, `get_best_practices`, `search_documentation`, `list_projects`, `onpush_zoneless_migration`, `run_target`, devserver tools | `--read-only`, `--local-only` flags |
| **Angular Agent Skills** | `npx skills add https://github.com/angular/skills` → `.agents/skills/` | `angular-developer`, `angular-new-app` | Targets v20+; legacy repos need the guardrail precedence rule |
| **Nx** | `npx nx configure-ai-agents` | writes agent config/MCP/skills | May overwrite CLAUDE.md (#37181) |

Single source of truth: `docs/ai/*.md` → `scripts/ai/generate.py` → all tool files; CI drift check in `.github/workflows/ai-context.yml`; CODEOWNERS on `docs/ai/**`.

---

## 4. REPO SCAN prompt
Shipped as `docs/ai/repo-scan-prompt.md` / `.kiro/steering/repo-scan.md` (manual). Read-only; uses Angular MCP + `nx graph` + ripgrep; inventories config; counts standalone/NgModule, zoneless, CD strategies, DI style, signals vs RxJS, inputs/outputs, control flow, state libs, smart/dumb, Nx tags, forms, HTTP, routing, errors, i18n, UI libs, SSR hazards, tests, naming, security; scores and picks the exemplar; writes `scan-report.md`, filled templates and `questions.md`; then STOPs.

---

## 5. Evidence and failure modes

Authoritative sources: angular.dev "LLM prompts and AI IDE setup" (official system prompt: standalone, no `standalone: true`, no explicit OnPush in v22+, `input()/output()/model()`, prefer Signal Forms, no `ngClass/ngStyle/CommonModule`, native control flow, `@Service` v22+, `inject()`); Angular v20/v21/v22 release notes (Angular blog, Ninja Squad, InfoQ); angular-eslint recommended set (`prefer-control-flow` added v21); Kiro docs; Claude Code memory docs; GitHub Copilot docs; Cursor; Windsurf/Devin; Junie; agents.md; Nx enforce-module-boundaries ("projects without tags cannot depend on any other projects").

| AI failure mode | Prevention |
|---|---|
| NgModules / `standalone: true` in standalone app | tech.md counts; guardrail ban; `prefer-standalone` |
| `*ngIf/*ngFor` | conventions; `prefer-control-flow`; lint hook |
| Constructor DI / `@Service` with ctor params | architecture DI rule; v22 gate |
| Manual `.subscribe()` leaks | signals-vs-RxJS policy; `takeUntilDestroyed` |
| Signal + BehaviorSubject double state | "one source of truth" rule |
| Hallucinated/wrong-version APIs (Material MDC, NgRx, Signal Forms in v21) | version-gate table; MCP `search_documentation`; ask if unsure |
| Deleting `Eager` / adding OnPush noise | guardrail row |
| Wrong zoneless patterns | guardrail + scan |
| `any`, untyped forms | TS + forms rules; `strictTemplates` captured |
| Direct DOM manipulation | hard ban |
| Invented dependencies | dependency policy |
| Bypassing interceptor/auth | api-contracts; scan flags raw `fetch(` |
| Wrong Nx boundaries | tags rule; `nx lint`; never edit depConstraints |
| SSR-unsafe globals | guardrail; scan counts; NFR in spec |
| Inaccessible markup | a11y rules; template a11y lint |
| Editing generated clients | READ-ONLY rule |
| Unrequested modernization | "never modernize by side effect" + legacy islands |
| "Done" without verification | tech.md commands; post-task hook |

---

## 6. Branching out

| Context | What changes | What stays |
|---|---|---|
| **Nx monorepo** | nx.json/project.json facts, tag taxonomy, `nx affected` commands, generators, per-lib AGENTS.md, `fileMatchPattern` per lib type (`libs/**/data-access/**`) | Conventions, guardrails, spec format |
| **Ionic/Capacitor** | `capacitor.config.ts`, platforms, `@ionic/angular/standalone` imports, native plugin policy, device commands; `mobile.md` steering scoped to `ios/**`, `android/**` | Architecture, state, HTTP, testing |
| **Micro-frontends (Module/Native Federation, Elements)** | host vs remote, federation config, shared singletons + version pinning, cross-MFE contracts, zone consistency, CSS isolation; stop-and-ask on shared deps | Per-remote steering = same template |
| **Hybrid with other frameworks** | directory-scoped steering; nested AGENTS.md per app; integration boundary docs | Generator, process, security |
| **Legacy NgModule + RxJS** | guardrail precedence keeps legacy style; legacy islands listed; migrations as separate specs (`onpush_zoneless_migration`, control-flow schematic) | Everything else |

## Recommendations
1. Week 1: commit `docs/ai/`, generator, CI check; run the scan with Angular MCP (`--read-only`); resolve `questions.md` in 30 minutes.
2. Pin knowledge sources: Angular CLI MCP in every tool; `angular/skills` only for v20+ repos.
3. Pilot one feature with a spec like the payment-methods example; iterate steering, not prompts.
4. Re-scan on every Angular major; steering changes ride the upgrade PR.
5. Keep always-on small; respect Windsurf limits.

## Caveats
Kiro hook schema/extension, Claude Code AGENTS.md handling, Nx `configure-ai-agents` output and the Angular MCP tool list change often; some details come from community write-ups/issues. `ngIf/ngFor` removal timing is contested (angular.dev API page says deprecated since v20, intent to remove). `ng new --ai-config` options are secondary-sourced. The payment example assumes a PSP with hosted fields.

## Sources
- https://angular.dev/ai/develop-with-ai · https://angular.dev/ai/mcp · https://angular.dev/api/common/NgFor
- https://blog.angular.dev/announcing-angular-v22-c52bb83a4664 · https://blog.angular.dev/announcing-angular-v20-b5c9c06cf301
- https://blog.ninja-squad.com/2026/06/03/what-is-new-angular-22.0 · https://blog.ninja-squad.com/2025/11/20/what-is-new-angular-21.0 · https://blog.ninja-squad.com/2025/05/28/what-is-new-angular-20.0
- https://www.infoq.com/news/2026/08/angular-v22-released/ · https://www.infoq.com/news/2026/06/angular-agent-skills/
- https://github.com/angular/angular/blob/main/skills/dev-skills/angular-developer/references/mcp.md
- https://www.npmjs.com/package/@angular-eslint/eslint-plugin · https://github.com/angular-eslint/angular-eslint/issues/2647
- https://kiro.dev/docs/steering/ · https://kiro.dev/docs/specs/ · https://kiro.dev/docs/specs/quick-spec/ · https://github.com/kirodotdev/Kiro/issues/9176 · https://github.com/kirodotdev/Kiro/issues/4573
- https://code.claude.com/docs/en/memory · https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot · https://junie.jetbrains.com/docs/guidelines-and-memory.html · https://agents.md/
- https://nx.dev/docs/getting-started/ai-setup · https://github.com/nrwl/nx/issues/37181
