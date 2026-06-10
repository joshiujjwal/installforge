# Flutter — curation notes

Human-readable context behind `recipe.yaml`. Keep the machine-runnable truth in the
YAML; use this file for nuance, links, and decisions an agent or maintainer should know.

## Scope

- "Flutter on iOS" means: install Flutter **on a macOS host** and set up the iOS
  toolchain (Xcode CLT + CocoaPods). iOS itself is a *build target*, not an install host.
- Linux target installs via `snap`. A tarball-based target is a future addition
  (see Parking Lot in `TODO.md`).

## Common bugs sourced from the field

| Symptom | Root cause | Curated fix |
|---|---|---|
| `CocoaPods not installed` in `flutter doctor` | CocoaPods not bundled | `brew install cocoapods` |
| `bad CPU type` on Apple Silicon | Rosetta 2 missing | `softwareupdate --install-rosetta` |
| `cannot find -lGLU` (Linux) | Mesa GLU dev lib missing | `apt-get install libglu1-mesa` |
| `snap: command not found` | snapd missing on server distros | `apt-get install snapd` |

## Sources

- https://docs.flutter.dev/get-started/install/macos
- https://docs.flutter.dev/get-started/install/linux
