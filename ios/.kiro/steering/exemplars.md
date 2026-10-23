---
inclusion: auto
name: exemplars
description: Golden-path feature and shared infrastructure to copy when creating or extending any feature, screen, use case, repository, or test.
---
# Exemplars — copy these shapes
## Golden path: {{FeatureName}}
| Role | File |
|---|---|
| Navigation entry | `{{App/Routing/AppRouter.swift}}` |
| View | `{{Features/Orders/Presentation/OrderListView.swift}}` |
| State/VM/Reducer | `{{…}}` |
| Use case | `{{…}}` |
| Repository protocol + impl | `{{…}}` |
| DTO + mapper | `{{…}}` |
| DI registration | `{{…/OrdersAssembly.swift}}` |
| Unit + snapshot tests | `{{…}}` |
Read these before writing a new feature; mirror structure, naming and test style.

## Shared infrastructure (reuse)
| Need | Use |
|---|---|
| HTTP / Persistence / Images | `{{APIClient}}` / `{{…}}` / `{{…}}` |
| Analytics / Flags / Keychain | `{{Analytics.track}}` / `{{…}}` / `{{KeychainStore}}` |
| Loading & error UI | `{{AsyncContentView / ErrorBanner}}` |

## Anti-exemplars (do NOT copy)
- `{{LegacyModule/**}}` — {{reason}}
