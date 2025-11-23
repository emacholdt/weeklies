---
description: Release a beta version of the integration
---

1. Check the current version in `custom_components/weeklies/manifest.json`.
2. Ask the user for the new beta version number (e.g., `0.2.4-beta.1`).
3. Update `version` in `custom_components/weeklies/manifest.json`.
4. Run the following commands to commit and tag:

```bash
git add custom_components/weeklies/manifest.json
git commit -m "Bump version to <NEW_VERSION>"
git tag v<NEW_VERSION>
```

5. Notify the user that the beta version has been tagged and is ready to be pushed (if they want to push manually).
