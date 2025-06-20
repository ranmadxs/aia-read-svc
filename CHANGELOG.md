---
runme:
  id: 01HKVAHXZSFGZ3V400EMT13388
  version: v3
---

# RELEASE

## [0.6.1] - 2025-06-19
### Added/Changed/Fixed
- 🐛 Fix: Corrección de imports relativos para repositories tras mover el directorio dentro de aia_read_svc.

## [0.6.0] - 2025-06-19
### Added/Changed/Fixed
- 🚀 Nueva versión minor: tests unitarios de repositorios separados, comentarios de ejecución por test, y uso de mongomock para pruebas en memoria.

## [0.5.1] - 2025-06-19
### Added/Changed/Fixed
- ⬆️ Updated: aia-utils to 0.4.5 and rebuilt poetry.lock
- 🔧 Patch: Python version restored to >=3.11.2,<3.14 for compatibility

## [0.5.0] - 2025-06-19
### Added/Changed/Fixed
- ✨ Refactor: Encapsulated the logic for obtaining faction and unit tokens into a new method (get_faction_token_from_sentence)
- ✨ Feature: get_faction_token_from_sentence and process_wh40k_obj now accept a custom tokens file as a parameter
- 🛠️ Minor: Improved logging for token extraction

[0.4.1] 16-jun-2025

- ✨ Feature: Implemented HTTP client for Gemini API queries
- 🔄 Update: Python version requirement to >=3.13,<3.14
- 🔄 Update: aia-utils to version 0.4.0

[0.3.5] 16-jun-2025

- 🔄 Update: aia-utils-0.3.3

[0.3.2] 12-ago-2024

- 🔄 Update: aia-utils-0.3.0
- 🔄 Update: pywhatkit-5.4
- 🔄 Update: selenium-4.23.1

[0.3.1] 25-ene-2024

- Bug fix get image WH40k Unit

[0.3.0] 21-ene-2024

- Feature: Send Img to Kafka Queue, and remove file system.

[0.2.3] 11-ene-2024

- Feature: Send Img (WH40k Unit) to aia-device

[0.1.0] First Version 28-dic-2023

- Feature add Docker Config
- Feature: WH40K Wahapedia units, Yahoo Read Svc.

