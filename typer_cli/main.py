import curses
import time
import argparse
import sys

from typer_cli.sentences import generate
from typer_cli.update import get_update_info
from typer_cli.profile import (
    profile_exists, read_profile, create_profile, append_test,
    post_race_stats,
)

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


def hline(win, y, x, n, cp=C_BORDER):
    put(win, y, x, "-" * n, cp)


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

    # build the bar as: "  30 wpm   100.0% acc   24s  "
    bar = f"{_wpm} wpm   {_acc} acc   {ts}"
    sx = cx(w, len(bar))

    px = sx
    put(scr, y, px, _wpm, C_ACCENT, curses.A_BOLD)
    px += len(_wpm)
    put(scr, y, px, " wpm   ", C_DIM)
    px += 7
    ac = C_GOOD if _acc not in ("-",) and float(_acc.rstrip("%")) >= 90 else C_BAD if _acc != "-" else C_DIM
    put(scr, y, px, _acc, ac, curses.A_BOLD)
    px += len(_acc)
    put(scr, y, px, " acc   ", C_DIM)
    px += 7
    tc = C_BAD if remain < 5 else C_ACCENT
    put(scr, y, px, ts, tc, curses.A_BOLD)


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

def test(scr, ti, di, update_info=None):
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
    user_name = read_profile().get("name", "")

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

        # ── compute layout — text stays fixed at vertical center ──
        text_y = max(1, (h - text_vis) // 2)

        if not started:
            # place logo, settings, timer ABOVE the text
            timer_y = text_y - 2
            settings_y = timer_y - 2
            logo_y = settings_y - LOGO_H - 1
            hint_y = text_y + text_vis + 1
        else:
            # place stats ABOVE the text
            stats_y = text_y - 2
            hint_y = text_y + text_vis + 1

        tx = cx(w, aw)

        # ── draw ──
        if not started:
            draw_logo(scr, logo_y, w)
            hit_regions = draw_settings(scr, settings_y, w, ti, di, False)
            putc(scr, timer_y, w, f"{tlimit}s", C_ACCENT, curses.A_BOLD)
            draw_text(scr, lines, typed, target, text_y, tx, aw, h)
            putc(scr, hint_y, w, "start typing...", C_DIM)
            if update_info and update_info["update_available"]:
                notice = f"v{update_info['latest']} available: {update_info['update_cmd']}"
                putc(scr, h - 2, w, notice, C_DIM)
            putc(scr, h - 1, w, "s stats   tab new words   esc quit", C_HINT)
            ver = f"v{update_info['version']}" if update_info else ""
            if ver:
                put(scr, h - 1, 1, ver, C_DIM)
            if user_name:
                put(scr, h - 1, w - len(user_name) - 1, user_name, C_DIM)
        else:
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
            if k == ord('s'):
                return "stats", ti, di
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


# ── name prompt ──────────────────────────────────────────────────────────────

def name_prompt(scr, existing=""):
    curses.curs_set(1)
    scr.nodelay(False)
    scr.timeout(-1)

    buf = list(existing)
    MAX_LEN = 20

    while True:
        scr.erase()
        h, w = scr.getmaxyx()
        y = max(1, h // 2 - 3)

        title = "-- change name --" if existing else "-- welcome to typer --"
        putc(scr, y, w, title, C_TITLE, curses.A_BOLD)
        y += 2
        putc(scr, y, w, "enter your name:", C_DIM)
        y += 2

        name_str = "".join(buf)
        fx = cx(w, MAX_LEN + 4)
        put(scr, y, fx, ">", C_ACCENT, curses.A_BOLD)
        put(scr, y, fx + 2, name_str, C_TITLE)
        try:
            scr.move(y, fx + 2 + len(name_str))
        except curses.error:
            pass

        y += 2
        if existing:
            putc(scr, y, w, "enter to confirm   esc cancel", C_HINT)
        else:
            putc(scr, y, w, "enter to confirm", C_HINT)

        scr.refresh()

        k = scr.getch()
        if k == 27:
            curses.curs_set(0)
            return None
        elif k in (10, 13):
            name = "".join(buf).strip()
            if name:
                curses.curs_set(0)
                return name
        elif k in (curses.KEY_BACKSPACE, 127, 8):
            if buf:
                buf.pop()
        elif 32 <= k <= 126 and len(buf) < MAX_LEN:
            buf.append(chr(k))

    curses.curs_set(0)


# ── results screen ───────────────────────────────────────────────────────────

def show_results(scr, r, ti, di, race=None):
    curses.curs_set(0)
    scr.nodelay(False)
    scr.timeout(-1)

    # pre-compute rating
    if r['acc'] >= 97 and r['wpm'] >= 80:
        rating, rcp = "blazing", C_ACCENT
    elif r['acc'] >= 95 and r['wpm'] >= 60:
        rating, rcp = "great", C_GOOD
    elif r['acc'] >= 90:
        rating, rcp = "solid", C_STAT
    elif r['acc'] >= 80:
        rating, rcp = "keep practicing", C_DIM
    else:
        rating, rcp = "slow down, focus on accuracy", C_BAD

    has_errs = bool(r['errs'])
    acp = C_GOOD if r['acc'] >= 90 else C_BAD

    # leaderboard data
    top3 = race["top3"] if race else []
    avg_delta = race["avg_delta"] if race else 0.0
    new_rank = race["rank"] if race else None

    while True:
        scr.erase()
        h, w = scr.getmaxyx()

        content_h = 21 + (2 if has_errs else 0)
        y = max(1, (h - content_h) // 2)

        # title
        putc(scr, y, w, "-- results --", C_TITLE, curses.A_BOLD)
        y += 2

        # big wpm + avg delta
        wpm_str = f"{r['wpm']:.1f} wpm"
        if avg_delta != 0:
            sign = "+" if avg_delta > 0 else ""
            delta_str = f"  {sign}{avg_delta:.1f} avg"
            delta_cp = C_GOOD if avg_delta > 0 else C_BAD
            total = wpm_str + delta_str
            sx = cx(w, len(total))
            put(scr, y, sx, wpm_str, C_ACCENT, curses.A_BOLD)
            put(scr, y, sx + len(wpm_str), delta_str, delta_cp)
        else:
            putc(scr, y, w, wpm_str, C_ACCENT, curses.A_BOLD)
        y += 2

        # divider
        dw = min(38, w - 10)
        putc(scr, y, w, "-" * dw, C_BORDER)
        y += 2

        # stats — two columns, centered
        gap = "     "
        rows = [
            ("wpm  ", f"{r['wpm']:.1f}", C_ACCENT, "raw  ", f"{r['raw']:.1f}", C_STAT),
            ("acc  ", f"{r['acc']:.1f}%", acp,      "time ", f"{r['time']:.1f}s", C_ACCENT),
            ("ok   ", str(r['ok']), C_GOOD,         "err  ", str(r['bad']), C_BAD),
        ]
        for l_label, l_val, l_cp, r_label, r_val, r_cp in rows:
            line = l_label + l_val + gap + r_label + r_val
            sx = cx(w, len(line))
            put(scr, y, sx, l_label, C_DIM)
            put(scr, y, sx + len(l_label), l_val, l_cp, curses.A_BOLD)
            rx = sx + len(l_label) + len(l_val) + len(gap)
            put(scr, y, rx, r_label, C_DIM)
            put(scr, y, rx + len(r_label), r_val, r_cp, curses.A_BOLD)
            y += 1
        y += 2

        # divider
        putc(scr, y, w, "-" * dw, C_BORDER)
        y += 2

        # personal best leaderboard
        if top3:
            medals = ["1st", "2nd", "3rd"]
            parts = []
            for i, wpm in enumerate(top3):
                parts.append((medals[i], f"{wpm:.0f}", i + 1 == new_rank))
            # render: "1st 94   2nd 78   3rd 72"
            line_parts = []
            for medal, val, is_new in parts:
                line_parts.append(f"{medal} {val}")
            line = "   ".join(line_parts)
            sx = cx(w, len(line))
            px = sx
            for i, (medal, val, is_new) in enumerate(parts):
                put(scr, y, px, medal, C_DIM)
                px += len(medal) + 1
                cp = C_ACCENT if is_new else C_STAT
                attr = curses.A_BOLD
                put(scr, y, px, val, cp, attr)
                if is_new:
                    put(scr, y, px + len(val), "*", C_ACCENT)
                px += len(val) + 3
            y += 2

        # rating
        putc(scr, y, w, rating, rcp, curses.A_BOLD)
        y += 2

        # mode
        putc(scr, y, w, f"{TIMES[ti]}s  {DIFFS[di]}", C_DIM)

        # missed chars
        if has_errs:
            y += 2
            top = sorted(r['errs'].items(), key=lambda x: -x[1])[:6]
            putc(scr, y, w, "missed: " + "  ".join(f"'{c}'x{n}" for c, n in top), C_DIM)

        # bottom hint
        putc(scr, h - 1, w, "tab restart   esc new test   q quit", C_HINT)
        scr.refresh()

        k = scr.getch()
        if k == 9:
            return "restart"
        elif k == 27:
            return "new"
        elif k in (ord('q'), ord('Q')):
            return "quit"


# ── stats screen ─────────────────────────────────────────────────────────────

def show_stats(scr):
    from typer_cli.profile import read_profile, set_name, compute_stats

    curses.curs_set(0)
    scr.nodelay(False)
    scr.timeout(-1)

    while True:
        profile = read_profile()
        stats = compute_stats(profile)

        scr.erase()
        h, w = scr.getmaxyx()

        if h < 15 or w < 40:
            try:
                scr.addstr(0, 0, "terminal too small!")
            except curses.error:
                pass
            scr.refresh()
            k = scr.getch()
            if k in (27, ord('q'), ord('Q')):
                return
            continue

        dw = min(50, w - 10)
        lx = cx(w, dw)
        rx = lx + dw // 2

        content_h = 22
        y = max(1, (h - content_h) // 2)

        # title
        putc(scr, y, w, "-- stats --", C_TITLE, curses.A_BOLD)
        y += 2

        # name
        putc(scr, y, w, stats["name"] or "(no name)", C_ACCENT, curses.A_BOLD)
        y += 1
        putc(scr, y, w, f"member since {stats['member_since']}", C_DIM)
        y += 2

        # divider
        hline(scr, y, cx(w, dw), dw)
        y += 2

        if stats["tests_completed"] == 0:
            putc(scr, y, w, "no tests yet -- start typing!", C_DIM)
        else:
            # tests + total time
            put(scr, y, lx, "tests  ", C_DIM)
            put(scr, y, lx + 7, str(stats["tests_completed"]), C_STAT, curses.A_BOLD)
            put(scr, y, rx, "total time  ", C_DIM)
            put(scr, y, rx + 12, stats["total_time_fmt"], C_STAT, curses.A_BOLD)
            y += 1

            # best wpm
            put(scr, y, lx, "best   ", C_DIM)
            if stats["best_wpm"] is not None:
                put(scr, y, lx + 7, f"{stats['best_wpm']:.0f} wpm", C_ACCENT, curses.A_BOLD)
                ctx = f"({stats['best_wpm_diff']}, {stats['best_wpm_date']})"
                put(scr, y, rx, ctx, C_DIM)
            y += 1

            # avg wpm (last 10)
            put(scr, y, lx, "avg    ", C_DIM)
            if stats["avg_wpm_recent"] is not None:
                put(scr, y, lx + 7, f"{stats['avg_wpm_recent']:.0f} wpm", C_STAT, curses.A_BOLD)
                put(scr, y, rx, "(last 10 tests)", C_DIM)
            y += 1

            # avg accuracy
            put(scr, y, lx, "acc    ", C_DIM)
            if stats["avg_acc"] is not None:
                acp = C_GOOD if stats["avg_acc"] >= 90 else C_BAD
                put(scr, y, lx + 7, f"{stats['avg_acc']:.1f}%", acp, curses.A_BOLD)
            y += 1

            # streak
            put(scr, y, lx, "streak ", C_DIM)
            sv = stats["streak"]
            scp = C_ACCENT if sv > 0 else C_DIM
            put(scr, y, lx + 7, f"{sv} day{'s' if sv != 1 else ''}", scp, curses.A_BOLD)
            y += 2

            # divider
            hline(scr, y, cx(w, dw), dw)
            y += 2

            # sparkline
            if stats["sparkline"]:
                label = "last 10  "
                sl = stats["sparkline"]
                sx = cx(w, len(label) + len(sl))
                put(scr, y, sx, label, C_DIM)
                put(scr, y, sx + len(label), sl, C_ACCENT, curses.A_BOLD)
                y += 2

                # divider
                hline(scr, y, cx(w, dw), dw)
                y += 2

            # per-difficulty breakdown
            diff_colors = {"easy": C_GOOD, "medium": C_STAT, "hard": C_BAD}
            for diff_name in ("easy", "medium", "hard"):
                diff_avg = stats["per_diff"].get(diff_name)
                put(scr, y, lx, f"{diff_name:8s}", C_DIM)
                if diff_avg is not None:
                    put(scr, y, lx + 8, f"{diff_avg:.0f} wpm", diff_colors[diff_name], curses.A_BOLD)
                else:
                    put(scr, y, lx + 8, "--", C_DIM)
                y += 1

        # bottom hint
        putc(scr, h - 1, w, "n change name   esc back", C_HINT)
        scr.refresh()

        k = scr.getch()
        if k in (27, ord('q'), ord('Q')):
            return
        elif k == ord('n'):
            new_name = name_prompt(scr, profile.get("name", ""))
            if new_name is not None:
                set_name(new_name)


# ── main ─────────────────────────────────────────────────────────────────────

def run(scr, args):
    init_colors()
    curses.curs_set(0)

    # first-launch: prompt for name
    if not profile_exists():
        name = name_prompt(scr)
        if name:
            create_profile(name)
        else:
            create_profile("")

    update_info = get_update_info()

    ti = TIMES.index(args.time) if args.time and args.time in TIMES else 1
    di = DIFFS.index(args.diff) if args.diff and args.diff in DIFFS else 1

    while True:
        result, ti, di = test(scr, ti, di, update_info)

        if result is None:
            return
        if result == "restart":
            continue
        if result == "stats":
            show_stats(scr)
            continue

        # completed test — save, compute leaderboard, show results
        append_test(result, TIMES[ti], DIFFS[di])
        race = post_race_stats(result['wpm'])
        action = show_results(scr, result, ti, di, race)
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
