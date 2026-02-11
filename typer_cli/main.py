import curses
import time
import argparse
import sys

from typer_cli.sentences import generate

# ── colors ───────────────────────────────────────────────────────────────────

C_DIM = 1
C_OK = 2
C_ERR = 3
C_CURSOR = 4
C_ACCENT = 5
C_STAT = 6
C_TITLE = 7
C_BORDER = 8
C_GOOD = 9
C_BAD = 10
C_HINT = 11


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(C_DIM, 244, -1)
    curses.init_pair(C_OK, 114, -1)
    curses.init_pair(C_ERR, 203, -1)
    curses.init_pair(C_CURSOR, 0, 214)
    curses.init_pair(C_ACCENT, 214, -1)
    curses.init_pair(C_STAT, 75, -1)
    curses.init_pair(C_TITLE, 255, -1)
    curses.init_pair(C_BORDER, 239, -1)
    curses.init_pair(C_GOOD, 114, -1)
    curses.init_pair(C_BAD, 203, -1)
    curses.init_pair(C_HINT, 244, -1)


# ── draw helpers ─────────────────────────────────────────────────────────────

def cx(w, n):
    return max(0, (w - n) // 2)


def put(win, y, x, text, cp=0, attr=0):
    try:
        win.addstr(y, x, text, curses.color_pair(cp) | attr)
    except curses.error:
        pass


def putc(win, y, w, text, cp=0, attr=0):
    put(win, y, cx(w, len(text)), text, cp, attr)


def box(win, y, x, h, w):
    put(win, y, x, "╭", C_BORDER)
    put(win, y, x + w - 1, "╮", C_BORDER)
    put(win, y + h - 1, x, "╰", C_BORDER)
    put(win, y + h - 1, x + w - 1, "╯", C_BORDER)
    for i in range(1, w - 1):
        put(win, y, x + i, "─", C_BORDER)
        put(win, y + h - 1, x + i, "─", C_BORDER)
    for j in range(1, h - 1):
        put(win, y + j, x, "│", C_BORDER)
        put(win, y + j, x + w - 1, "│", C_BORDER)


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split(" "):
        test = f"{cur} {word}" if cur else word
        if len(test) <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ── logo ─────────────────────────────────────────────────────────────────────

LOGO = [
    " ▄▄▄▄▄ ▄· ▄▌ ▄▄▄·▄▄▄ .▄▄▄  ",
    " •██  ▐█▪██▌▐█ ▄█▀▄.▀·▀▄ █·",
    "  ▐█.▪▐█▌▐█▪ ██▀·▐▀▀▪▄▐▀▀▄ ",
    "  ▐█▌·▐█▀·.▐█▪·•▐█▄▄▌▐█•█▌",
    "  ▀▀▀  ▀ •  .▀    ▀▀▀ .▀  ▀",
]
LOGO_H = len(LOGO)


def draw_logo(win, y, w):
    for i, line in enumerate(LOGO):
        putc(win, y + i, w, line, C_ACCENT, curses.A_BOLD)


# ── settings bar (clickable) ────────────────────────────────────────────────

TIMES = [15, 30, 60, 120]
DIFFS = ["easy", "medium", "hard"]


def draw_settings(scr, y, w, ti, di, locked):
    """Draw settings bar and return click hit regions."""
    regions = []
    items = []
    total = 0
    for i, t in enumerate(TIMES):
        label = str(t)
        items.append(("time", i, label))
        total += len(label) + 2
    total += 3  # separator " | "
    for i, d in enumerate(DIFFS):
        items.append(("diff", i, d))
        total += len(d) + 2

    x = cx(w, total)
    for kind, idx, label in items:
        if kind == "diff" and idx == 0:
            put(scr, y, x, " | ", C_BORDER)
            x += 3

        active = (kind == "time" and idx == ti) or (kind == "diff" and idx == di)

        if active:
            cp = C_DIM if locked else C_ACCENT
            put(scr, y, x, label, cp, curses.A_BOLD)
        else:
            put(scr, y, x, label, C_DIM)

        regions.append((x, x + len(label), kind, idx))
        x += len(label) + 2

    return regions


# ── stats helpers ────────────────────────────────────────────────────────────

def calc_wpm(target, typed, elapsed):
    if elapsed < 0.5:
        return "-"
    ok = sum(1 for i in range(min(len(typed), len(target))) if typed[i] == target[i])
    return f"{(ok / 5) / (elapsed / 60):.0f}"


def calc_acc(target, typed):
    if not typed:
        return "-"
    ok = sum(1 for i in range(min(len(typed), len(target))) if typed[i] == target[i])
    return f"{ok / len(typed) * 100:.1f}%"


def calc_results(target, typed, elapsed):
    n = min(len(typed), len(target))
    ok = sum(1 for i in range(n) if typed[i] == target[i])
    bad = n - ok
    w = (ok / 5) / (elapsed / 60) if elapsed > 0 else 0
    rw = (len(typed) / 5) / (elapsed / 60) if elapsed > 0 else 0
    a = (ok / len(typed) * 100) if typed else 0
    errs = {}
    for i in range(n):
        if typed[i] != target[i]:
            errs[target[i]] = errs.get(target[i], 0) + 1
    return dict(wpm=w, raw=rw, acc=a, ok=ok, bad=bad,
                missed=max(0, len(target) - len(typed)),
                chars=len(typed), time=elapsed, errs=errs)


def draw_stats(scr, y, w, target, typed, elapsed, remain):
    _wpm = calc_wpm(target, typed, elapsed)
    _acc = calc_acc(target, typed)
    ts = f"{max(0, remain):.0f}s"

    bar = f"  {_wpm} wpm   {_acc} acc   {ts}  "
    bw = len(bar) + 4
    bx = cx(w, bw)
    box(scr, y, bx, 3, bw)

    px = bx + 3
    put(scr, y + 1, px, _wpm, C_ACCENT, curses.A_BOLD)
    put(scr, y + 1, px + len(_wpm), " wpm   ", C_DIM)
    px += len(_wpm) + 7
    ac = C_GOOD if _acc not in ("-",) and float(_acc.rstrip("%")) >= 90 else C_BAD if _acc != "-" else C_DIM
    put(scr, y + 1, px, _acc, ac, curses.A_BOLD)
    put(scr, y + 1, px + len(_acc), " acc   ", C_DIM)
    px += len(_acc) + 7
    tc = C_BAD if remain < 5 else C_ACCENT
    put(scr, y + 1, px, ts, tc, curses.A_BOLD)


# ── text drawing ─────────────────────────────────────────────────────────────

def draw_text(scr, lines, typed, target, sy, sx, aw, sh):
    pos = len(typed)
    maxl = sh - sy - 3
    cline, ci = 0, 0
    for i, line in enumerate(lines):
        if ci + len(line) >= pos:
            cline = i
            break
        ci += len(line) + 1

    vis = min(maxl, 3)
    ss = max(0, min(cline - 1, len(lines) - vis))
    off = sum(len(lines[i]) + 1 for i in range(ss))

    for li in range(ss, min(ss + vis, len(lines))):
        line = lines[li]
        y = sy + (li - ss)
        if y >= sh - 2:
            break
        for ci2, ch in enumerate(line):
            ri = off + ci2
            x = sx + ci2
            if x >= sx + aw:
                break
            if ri < pos:
                cp = C_OK if ri < len(typed) and typed[ri] == target[ri] else C_ERR
                at = curses.A_UNDERLINE if cp == C_ERR else 0
                put(scr, y, x, ch, cp, at)
            elif ri == pos:
                put(scr, y, x, ch, C_CURSOR, curses.A_BOLD)
            else:
                put(scr, y, x, ch, C_DIM)
        off += len(line) + 1


# ── main test loop ───────────────────────────────────────────────────────────

def test(scr, ti, di):
    curses.curs_set(0)
    scr.nodelay(True)
    scr.timeout(50)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    tlimit = TIMES[ti]
    diff = DIFFS[di]
    wc = max(80, tlimit * 3)
    target = generate(wc, diff)
    typed = []
    started = False
    t0 = 0.0

    settings_y = 0
    hit_regions = []

    while True:
        now = time.time()
        elapsed = (now - t0) if started else 0.0
        remain = tlimit - elapsed
        done = started and elapsed >= tlimit
        if done:
            break

        scr.erase()
        h, w = scr.getmaxyx()
        if h < 10 or w < 40:
            scr.addstr(0, 0, "terminal too small!")
            scr.refresh()
            if scr.getch() == 27:
                return None, ti, di
            continue

        # ── responsive text width ──
        aw = min(w - 6, 90)
        lines = wrap(target, aw)
        text_vis = min(3, len(lines))

        # ── compute centered layout ──
        if not started:
            # idle: logo + settings + timer_label + gap + text + hint
            content_h = LOGO_H + 2 + 1 + 2 + text_vis + 3
            top = max(0, (h - content_h) // 2)

            logo_y = top
            settings_y = top + LOGO_H + 2
            timer_y = settings_y + 2
            text_y = timer_y + 2
            hint_y = text_y + text_vis + 1
        else:
            # typing: settings + stats_box + gap + text + hint
            content_h = 1 + 4 + 1 + text_vis + 2
            top = max(0, (h - content_h) // 2)

            settings_y = top
            stats_y = top + 2
            text_y = stats_y + 4
            hint_y = text_y + text_vis + 1

        tx = cx(w, aw)

        # ── draw ──
        if not started:
            draw_logo(scr, logo_y, w)
            hit_regions = draw_settings(scr, settings_y, w, ti, di, False)
            putc(scr, timer_y, w, f"{tlimit}s", C_ACCENT, curses.A_BOLD)
            draw_text(scr, lines, typed, target, text_y, tx, aw, h)
            putc(scr, hint_y, w, "start typing...", C_DIM)
            putc(scr, h - 1, w, "←/→ time   ↑/↓ difficulty   tab new words   esc quit", C_HINT)
        else:
            hit_regions = draw_settings(scr, settings_y, w, ti, di, True)
            draw_stats(scr, stats_y, w, target, typed, elapsed, remain)
            draw_text(scr, lines, typed, target, text_y, tx, aw, h)
            putc(scr, h - 1, w, "tab restart   esc quit", C_HINT)

        scr.refresh()

        # ── input ──
        k = scr.getch()
        if k == -1:
            continue
        if k == 27:
            return None, ti, di
        if k == 9:  # tab
            return "restart", ti, di

        # mouse clicks (only before test starts)
        if k == curses.KEY_MOUSE and not started:
            try:
                _, mx, my, _, bstate = curses.getmouse()
                if bstate & (curses.BUTTON1_CLICKED | curses.BUTTON1_PRESSED):
                    if my == settings_y:
                        for x1, x2, kind, idx in hit_regions:
                            if x1 <= mx < x2:
                                changed = False
                                if kind == "time" and idx != ti:
                                    ti = idx
                                    tlimit = TIMES[ti]
                                    changed = True
                                elif kind == "diff" and idx != di:
                                    di = idx
                                    diff = DIFFS[di]
                                    changed = True
                                if changed:
                                    target = generate(max(80, tlimit * 3), DIFFS[di])
                                    typed = []
                                    lines = wrap(target, aw)
                                break
            except curses.error:
                pass
            continue

        if not started:
            # arrow keys for settings
            if k == curses.KEY_LEFT:
                ti = (ti - 1) % len(TIMES)
                tlimit = TIMES[ti]
                target = generate(max(80, tlimit * 3), DIFFS[di])
                typed = []
                continue
            elif k == curses.KEY_RIGHT:
                ti = (ti + 1) % len(TIMES)
                tlimit = TIMES[ti]
                target = generate(max(80, tlimit * 3), DIFFS[di])
                typed = []
                continue
            elif k == curses.KEY_UP:
                di = (di - 1) % len(DIFFS)
                target = generate(max(80, tlimit * 3), DIFFS[di])
                typed = []
                continue
            elif k == curses.KEY_DOWN:
                di = (di + 1) % len(DIFFS)
                target = generate(max(80, tlimit * 3), DIFFS[di])
                typed = []
                continue

        # typing
        if not started and 32 <= k <= 126:
            started = True
            t0 = time.time()

        if k in (curses.KEY_BACKSPACE, 127, 8):
            if typed:
                typed.pop()
        elif 32 <= k <= 126 and len(typed) < len(target):
            typed.append(chr(k))

    elapsed = time.time() - t0 if started else 0.001
    return calc_results(target, typed, elapsed), ti, di


# ── results screen ───────────────────────────────────────────────────────────

def show_results(scr, r, ti, di):
    curses.curs_set(0)
    scr.nodelay(False)
    scr.timeout(-1)

    while True:
        scr.erase()
        h, w = scr.getmaxyx()

        # centered layout: title + wpm + stats_box + bar + rating + errs + hint
        has_errs = bool(r['errs'])
        content_h = 2 + 2 + 8 + 2 + 2 + (2 if has_errs else 0) + 3
        y = max(1, (h - content_h) // 2)

        putc(scr, y, w, "── results ──", C_TITLE, curses.A_BOLD)
        y += 2
        putc(scr, y, w, f"{r['wpm']:.0f} wpm", C_ACCENT, curses.A_BOLD)
        y += 2

        bw = min(52, w - 4)
        bx = cx(w, bw)
        box(scr, y, bx, 8, bw)
        c1 = bx + 3
        c2 = bx + bw // 2 + 2
        ry = y + 1

        def sr(label, val, cp, col, row):
            put(scr, row, col, f"{label}: ", C_DIM)
            put(scr, row, col + len(label) + 2, str(val), cp, curses.A_BOLD)

        sr("wpm", f"{r['wpm']:.1f}", C_ACCENT, c1, ry)
        sr("raw", f"{r['raw']:.1f}", C_STAT, c2, ry)
        ry += 1
        sr("accuracy", f"{r['acc']:.1f}%", C_GOOD if r['acc'] >= 90 else C_BAD, c1, ry)
        sr("time", f"{r['time']:.1f}s", C_ACCENT, c2, ry)
        ry += 1
        sr("correct", str(r['ok']), C_GOOD, c1, ry)
        sr("incorrect", str(r['bad']), C_BAD, c2, ry)
        ry += 2

        blen = min(int(r['wpm']), bw - 6)
        put(scr, ry, c1, "█" * max(blen, 1), C_ACCENT)
        ry += 2

        if r['acc'] >= 97 and r['wpm'] >= 80:
            putc(scr, ry, w, "blazing", C_ACCENT, curses.A_BOLD)
        elif r['acc'] >= 95 and r['wpm'] >= 60:
            putc(scr, ry, w, "great", C_GOOD, curses.A_BOLD)
        elif r['acc'] >= 90:
            putc(scr, ry, w, "solid", C_STAT, curses.A_BOLD)
        elif r['acc'] >= 80:
            putc(scr, ry, w, "keep practicing", C_DIM, curses.A_BOLD)
        else:
            putc(scr, ry, w, "slow down, focus on accuracy", C_BAD, curses.A_BOLD)

        if has_errs:
            ry += 2
            top = sorted(r['errs'].items(), key=lambda x: -x[1])[:6]
            putc(scr, ry, w, "missed: " + "  ".join(f"'{c}'x{n}" for c, n in top), C_DIM)

        putc(scr, h - 3, w, f"{TIMES[ti]}s  {DIFFS[di]}", C_DIM)
        putc(scr, h - 1, w, "tab restart   esc new test   q quit", C_HINT)
        scr.refresh()

        k = scr.getch()
        if k == 9:
            return "restart"
        elif k == 27:
            return "new"
        elif k in (ord('q'), ord('Q')):
            return "quit"


# ── main ─────────────────────────────────────────────────────────────────────

def run(scr, args):
    init_colors()
    curses.curs_set(0)

    ti = TIMES.index(args.time) if args.time and args.time in TIMES else 1
    di = DIFFS.index(args.diff) if args.diff and args.diff in DIFFS else 1

    while True:
        result, ti, di = test(scr, ti, di)

        if result is None:
            return
        if result == "restart":
            continue

        action = show_results(scr, result, ti, di)
        if action == "restart":
            continue
        elif action == "quit":
            return
        else:
            continue


def entry():
    parser = argparse.ArgumentParser(
        prog="typer",
        description="typer — typing practice in your terminal",
    )
    parser.add_argument("-t", "--time", type=int, metavar="SEC",
                        help="time in seconds (15, 30, 60, 120)")
    parser.add_argument("-d", "--diff", type=str, metavar="LEVEL",
                        choices=["easy", "medium", "hard"],
                        help="difficulty (easy, medium, hard)")
    args = parser.parse_args()

    try:
        curses.wrapper(lambda scr: run(scr, args))
    except KeyboardInterrupt:
        pass
