# Changelog

## [0.2.4] - 2025-11-23
### Added
- ✨ **Services UI**: Added `services.yaml` to enable UI mode for `add_item` and `remove_item` services in Developer Tools.
- 🚀 **Workflows**: Added beta release workflow.

## [0.2.0] - 2025-11-22
### Added
- ✨ **Auto-Uncheck**: New option to automatically reset completed items at midnight. (Configure via Settings > Devices & Services > Weeklies > Configure).
- ☕ Added "Buy Me a Coffee" link to README.

## [0.1.3] - 2025-11-21
### Added
- 📚 Added Dashboard Card examples to README (Markdown & Time-based).
- 🖼️ Fixed logo display in HACS by using absolute URL.

## [0.1.2] - 2025-11-21
### Fixed
- 🐛 Fixed `TypeError` during setup (removed extra argument in `async_forward_entry_setups`).

## [0.1.1] - 2025-11-21
### Added
- 🎨 Added a new logo!
- 📝 Added `CHANGELOG.md`.

### Fixed
- 🔧 Fixed HACS installation issue by adding `hacs.json`.

## [0.1.0-beta] - 2025-11-21
### Added
- 🎉 Initial beta release.
- ✅ Todo List platform for managing weekly tasks.
- 🤖 Sensors for `today`, `tomorrow`, and each day of the week.
- 💾 Persistent storage using Home Assistant's `.storage`.
