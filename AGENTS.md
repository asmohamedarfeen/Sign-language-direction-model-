# Repository Guidelines

## Project Structure & Module Organization

This workspace currently contains an empty `signlanguage-model/` directory. No source code, tests, assets, dependency manifests, or build configuration are present. Place work for that component inside `signlanguage-model/`; document its internal layout when implementation begins. Keep source code, tests, and assets in clearly separated directories as they are introduced.

## Build, Test, and Development Commands

No build, test, or development commands are configured yet. Do not assume that `npm test`, `make build`, or other ecosystem commands apply. When adding a toolchain, include its dependency manifest and a README with exact installation, local execution, build, and test commands. Run commands from the directory containing the relevant configuration, such as `cd signlanguage-model` for component-specific tooling.

## Coding Style & Naming Conventions

No language, formatter, linter, or indentation standard has been established. When introducing code, select idiomatic conventions for its language and commit the corresponding formatting and lint configuration. Use descriptive names, follow a consistent filename pattern within each module, and avoid unrelated formatting changes. Use Markdown headings and short, actionable explanations in documentation.

## Testing Guidelines

No testing framework or coverage threshold is configured. Add automated tests alongside new executable behavior and document how to run them. Follow the selected framework’s discovery and filename conventions. Cover expected behavior, invalid input, and relevant edge cases; keep fixtures small and reproducible.

## Commit & Pull Request Guidelines

No Git metadata or commit history is available in this workspace, so existing commit conventions cannot be inferred. Until a convention is established, use concise, imperative messages such as `Add model input validation`. Keep changes focused. Pull requests should explain the purpose, list validation performed, link relevant issues, and include screenshots when changing a visual interface. Explicitly identify checks that could not be run.

## Security & Configuration

Keep credentials, private datasets, and local environment files out of version control. Document required configuration with placeholder values rather than real secrets. Review large datasets and model artifacts before committing them, and document how contributors can obtain required resources.
