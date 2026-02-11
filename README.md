# typer

Typing practice in your terminal. Like [monkeytype](https://monkeytype.com), but in the CLI.

## Install

```
brew tap William-Ger/typer
brew install typer
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
| `tab`     | restart test        |
| `esc`     | quit                |
| `←` `→`  | change time         |
| `↑` `↓`  | change difficulty   |
| `click`   | click time/difficulty|
| `q`       | quit (results)      |

## Install from source

```
pip install .
```

## Zero dependencies

Pure Python. Only uses `curses` (built-in). Works on macOS and Linux out of the box.
