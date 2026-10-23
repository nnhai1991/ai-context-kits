---
inclusion: always
---
# Project Structure
- Project source of truth: {{App.xcodeproj | Project.swift (Tuist) | project.yml (XcodeGen) | Package.swift}}
- Adding files: {{synchronized folder groups pick up new files | regenerate with tuist | update project.yml}}

## Targets
| Target | Type | Path | Depends on |
|---|---|---|---|
| {{App}} | app | `{{App/}}` | {{Core, FeatureX}} |

## Feature folder layout (copy exactly)
```
{{Features/<Name>/Presentation/<Name>View.swift, <Name>ViewModel.swift
Features/<Name>/Domain/<Action>UseCase.swift, <Entity>.swift
Features/<Name>/Data/<Entity>Repository.swift, <Entity>DTO.swift, <Entity>Mapper.swift
Features/<Name>/<Name>Assembly.swift}}
```

## Module import rules
- {{Core}} imports no Feature module. Features may import {{Core, DesignSystem, Networking}} only.
- Cross-feature navigation only via {{AppRouter / Coordinator protocol in Core}}.

## Do-not-touch
- Generated: {{Generated/**, *.generated.swift}} · Vendored/legacy: {{Vendor/**, LegacyObjC/**}}
- `project.pbxproj`: {{never hand-edit | only via tuist / Xcode tools}}
