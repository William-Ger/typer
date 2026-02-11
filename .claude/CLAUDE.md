# typer — Project Guide

## Overview

Terminal-based typing practice tool (like monkeytype for the CLI). Pure Python, zero dependencies — only uses `curses` from stdlib. Works on macOS and Linux.

## Repositories

### William-Ger/typer (this repo)
The main application. Published to PyPI as `typer-cli-tool`. Entry point is `typer` command.

### William-Ger/homebrew-typer
The Homebrew tap. Contains a single formula at `Formula/typer.rb` that installs via `brew tap William-Ger/typer && brew install typer`. This is a separate repo — when releasing, you must update it too.

## Project Structure

```
typer_cli/
  __init__.py      # version number (__version__)
  __main__.py      # python -m typer_cli support
  main.py          # curses UI, test loop, results screen, stats screen, CLI entry
  sentences.py     # template-grammar sentence generator with slot filling
  words.py         # categorized word banks by difficulty (nouns, verbs, adjectives, etc.)
  profile.py       # JSON profile at ~/.config/typer/profile.json — test history, stats, streaks
  update.py        # passive update checker — GitHub releases API, cached daily, install method detection
pyproject.toml     # package metadata, version, entry point
```

## Key Architecture

- **Sentence generation**: Templates like `"The {noun1} {v_past1} the {noun2}."` filled by `_Filler` class that picks random words from difficulty-tiered pools. Easy/medium/hard templates have increasing clause complexity.
- **Difficulty**: Controls both word bank complexity (easy words vs hard words like "kaleidoscope") AND template complexity (simple SVO vs compound sentences with semicolons).
- **UI**: All curses-based. Layout is responsive to terminal size. Text stays vertically centered. Uses 11 color pairs.
- **Profile**: Flat JSON file at `~/.config/typer/profile.json` with a `tests` array. Each test records wpm, raw, acc, ok, bad, time_limit, difficulty, elapsed.
- **Update check**: `get_update_info()` in update.py hits GitHub releases API (cached 24h). Detects install method by checking if `sys.executable` is in a Homebrew path. Shows version in bottom-left of home screen, and update command if outdated.

## Install Methods

Users install one of three ways:
1. **Homebrew**: `brew tap William-Ger/typer && brew install typer`
2. **pip (from PyPI)**: `pip install typer-cli-tool`
3. **pipx (recommended for CLI tools)**: `pipx install typer-cli-tool`

Update commands:
- Homebrew: `brew update && brew upgrade typer` (must include `brew update` to refresh the tap)
- pip/pipx: `pip install --upgrade typer-cli-tool`

The package is published on PyPI as `typer-cli-tool`.

## Release Process

When releasing a new version:

1. **Bump version** in two places:
   - `typer_cli/__init__.py` — `__version__ = "X.Y.Z"`
   - `pyproject.toml` — `version = "X.Y.Z"`

2. **Commit and push** to main.

3. **Create GitHub release**:
   ```
   gh release create vX.Y.Z --title "vX.Y.Z" --notes "release notes here"
   ```

4. **Get the tarball sha256**:
   ```
   curl -sL https://github.com/William-Ger/typer/archive/refs/tags/vX.Y.Z.tar.gz | shasum -a 256
   ```

5. **Update the Homebrew formula** in `William-Ger/homebrew-typer`:
   - Update `url` to point to the new tag
   - Update `sha256` with the hash from step 4
   - Commit with message like "bump typer to vX.Y.Z"
   - Can be done via GitHub API:
     ```
     FILE_SHA=$(gh api repos/William-Ger/homebrew-typer/contents/Formula/typer.rb --jq '.sha')
     # Then PUT the updated content
     ```

6. **Publish to PyPI**:
   ```
   ~/.local/bin/pyproject-build
   ~/.local/bin/twine upload dist/*
   ```
   Username is `__token__`, password is the PyPI API token.
   Clean old builds first if needed: `rm -rf dist/`

All 6 steps are required. If you skip step 5, `brew upgrade typer` won't pick up the new version. If you skip step 6, `pip install --upgrade typer-cli-tool` won't pick it up.

## Design Principles

- Zero dependencies — only stdlib `curses`. No pip packages.
- Everything runs in the terminal. No web server, no electron.
- Profile data is local-only (~/.config/typer/).
- Update checks are passive (just a notice in the UI), never blocking or interactive.
- Versioning follows semver. Patch for small fixes, minor for features/behavioral changes.

## Testing

No test suite currently. To test manually, run `typer` and verify:
- Home screen shows version bottom-left
- Arrow keys / mouse change settings
- Typing starts the timer
- Results screen shows after time runs out
- `s` opens stats screen
- `tab` restarts/home, `ctrl+q` quits
