# WebFactoryOS orchestration boundary

Modern Flat Image Pipeline is autonomous from WebFactoryOS and Caveman runtime systems.

## Ownership boundary

- Modern Flat Image Pipeline owns repository code, skill content, assets, validators, tests, issues, pull requests, tags, releases, and release evidence.
- WebFactoryOS owns external registry, routing, relations, naming, and orchestration status only.
- `grants_write_access=false`: registry or orchestration references do not grant external systems write authority over this repository.

## Dependency boundary

The skill has no WebFactoryOS or Caveman build, runtime, validation, generation, or release dependency. External orchestration may point to this repository, but local validation and release readiness are determined by this repository's canonical files and validators.

## Release evidence boundary

Social preview upload and public repository-card verification are owner-side GitHub Settings and public-web observations. Repository files may record committed preview assets, but they must not assert owner-side upload or public-card PASS without observable evidence.

## Public status links

- Repository: https://github.com/sevranty/modern-flat-image-pipeline
- Task status: repository-local validation ready; owner-side Social preview verification, merge, tag, and GitHub Release publication require public GitHub evidence before they can be reported as complete.
