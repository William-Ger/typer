# typer

Typing practice in your terminal. Like [monkeytype](https://monkeytype.com), but in the CLI.

## Install

**Homebrew** (macOS/Linux):

```
brew tap William-Ger/typer
brew install typer
```

**pip**:

```
pip install typer-cli-tool
```

Then just run:

```
typer
```

## Usage

```
typer              # 30s medium (default)
typer -t 15        # 15 second test
typer -t 60        # 60 second test
typer -d hard      # hard difficulty
typer -t 15 -d easy # quick easy warmup
```

## Controls

| Key       | Action              |
|-----------|---------------------|
| `tab`     | restart / home      |
| `ctrl+q`  | quit                |
| `←` `→`  | change time         |
| `↑` `↓`  | change difficulty   |
| `click`   | click time/difficulty|
| `s`       | stats               |

## Features

- Timed tests: 15s, 30s, 60s, 120s
- Three difficulty levels (easy, medium, hard)
- Live WPM and accuracy while typing
- Personal stats: best WPM, streaks, per-difficulty averages, sparkline
- User profiles stored locally at `~/.config/typer/`
- Passive update check — shows update command if a new version is available

## Update

Homebrew:

```
brew update && brew upgrade typer
```

pip:

```
pip install --upgrade typer-cli-tool
```

## Zero dependencies

Pure Python. Only uses `curses` (built-in). Works on macOS and Linux out of the box.
