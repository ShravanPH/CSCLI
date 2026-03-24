# Implementation Roadmap (Feature intentionally omitted)

## Stage 1: CLI foundation

- Add one command that receives shell command text as input.
- Add tests for argument parsing and command routing.

## Stage 2: On shell startup

- Attach cmd_shell_lab to a shell whenever a user starts a new terminal
- Should print out user command

## Stage 3: Randomizer module

- Define item schema and weighted selection model.
- Write unit tests for distribution sanity.

## Stage 4: Visual rendering

- Define animation frame budget and max runtime overhead.
- Add graceful fallback for non-interactive terminals.
- Keep rendering module independent from selection logic.

## Stage 5: Packaging and release

- Add versioning and changelog workflow.
- Add CI checks for lint, tests, and package build.
- Publish first pre-release package.
