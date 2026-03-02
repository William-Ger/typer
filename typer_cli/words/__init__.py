"""Categorized word banks for sentence generation."""

from typer_cli.words.nouns import NOUNS_EASY, NOUNS_MEDIUM, NOUNS_HARD
from typer_cli.words.nouns_plural import NOUNS_PL_EASY, NOUNS_PL_MEDIUM, NOUNS_PL_HARD
from typer_cli.words.verbs_past import VERBS_PAST_EASY, VERBS_PAST_MEDIUM, VERBS_PAST_HARD
from typer_cli.words.verbs_present import VERBS_PRES_EASY, VERBS_PRES_MEDIUM, VERBS_PRES_HARD
from typer_cli.words.verbs_base import VERBS_BASE_EASY, VERBS_BASE_MEDIUM, VERBS_BASE_HARD
from typer_cli.words.verbs_gerund import VERBS_ING_EASY, VERBS_ING_MEDIUM, VERBS_ING_HARD
from typer_cli.words.adjectives import ADJ_EASY, ADJ_MEDIUM, ADJ_HARD
from typer_cli.words.adverbs import ADV_EASY, ADV_MEDIUM, ADV_HARD
from typer_cli.words.phrases import PREPOSITIONS, TIME_PHRASES, PRONOUNS


def _pool(easy, medium=None, hard=None, difficulty="medium"):
    """Build a cumulative word pool based on difficulty."""
    if difficulty == "easy":
        return easy
    elif difficulty == "medium":
        return easy + (medium or [])
    else:
        return easy + (medium or []) + (hard or [])


def get_pools(difficulty="medium"):
    """Return all word category pools for a given difficulty."""
    return {
        "noun": _pool(NOUNS_EASY, NOUNS_MEDIUM, NOUNS_HARD, difficulty),
        "nouns": _pool(NOUNS_PL_EASY, NOUNS_PL_MEDIUM, NOUNS_PL_HARD, difficulty),
        "v_past": _pool(VERBS_PAST_EASY, VERBS_PAST_MEDIUM, VERBS_PAST_HARD, difficulty),
        "v_pres": _pool(VERBS_PRES_EASY, VERBS_PRES_MEDIUM, VERBS_PRES_HARD, difficulty),
        "v_base": _pool(VERBS_BASE_EASY, VERBS_BASE_MEDIUM, VERBS_BASE_HARD, difficulty),
        "v_ing": _pool(VERBS_ING_EASY, VERBS_ING_MEDIUM, VERBS_ING_HARD, difficulty),
        "adj": _pool(ADJ_EASY, ADJ_MEDIUM, ADJ_HARD, difficulty),
        "adv": _pool(ADV_EASY, ADV_MEDIUM, ADV_HARD, difficulty),
        "pron": PRONOUNS,
        "prep": PREPOSITIONS,
        "time": TIME_PHRASES,
    }
