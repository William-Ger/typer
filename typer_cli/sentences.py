"""Template grammar sentence generator."""

import random
from typer_cli.words import get_pools


# ── slot filler ──────────────────────────────────────────────────────────────

class _Filler:
    """Mapping that picks a fresh random word for each unique slot.

    Slot names like 'noun1', 'noun2' both resolve to the 'noun' category
    but get independent random picks.
    """
    def __init__(self, pools):
        self._pools = pools
        self._cache = {}

    def __getitem__(self, key):
        if key in self._cache:
            return self._cache[key]
        cat = key.rstrip("0123456789")
        pool = self._pools.get(cat)
        if not pool:
            raise KeyError(f"unknown category: {cat}")
        val = random.choice(pool)
        self._cache[key] = val
        return val


# ── templates ────────────────────────────────────────────────────────────────

EASY_TEMPLATES = [
    # simple subject-verb-object
    "The {noun1} {v_past1} the {noun2}.",
    "{name1} {v_past1} a {adj1} {noun1}.",
    "The {adj1} {noun1} was very {adj2}.",
    "I {v_past1} the {noun1} {prep1} the {noun2}.",
    "{name1} {v_past1} {adv1} and {v_past2} away.",
    "The {noun1} {v_past1} {prep1} the {adj1} {noun2}.",
    "A {adj1} {noun1} sat {prep1} the {noun2}.",
    "{name1} could see the {adj1} {noun1}.",
    "The {adj1} {noun1} {v_past1} {adv1}.",
    "We {v_past1} the {noun1} and the {noun2}.",
    "She {v_past1} the {adj1} {noun1} {prep1} the {noun2}.",
    "He {v_past1} a {noun1} and {v_past2} home.",
    "The {nouns1} were {adj1} and {adj2}.",
    "It was a {adj1} day in the {noun1}.",
    "The {noun1} fell {prep1} the {adj1} {noun2}.",
    "A {noun1} and a {noun2} sat {prep1} the {noun3}.",
    "They {v_past1} the {adj1} {noun1} {time1}.",
    "{name1} had a {adj1} {noun1}.",
    "The {adj1} {nouns1} {v_past1} {prep1} the {noun1}.",
    "She liked the {adj1} {noun1} very much.",
    "It was {adj1} and {adj2} outside.",
    "The {noun1} {v_past1} but the {noun2} did not.",
    "He {v_past1} {adv1} {prep1} the {noun1}.",
    "The old {noun1} stood {prep1} the {noun2}.",
    "{name1} {v_past1} the door and {v_past2} inside.",
    "We could hear the {adj1} {noun1} from here.",
    "A {adj1} {noun1} {v_past1} down the {noun2}.",
    "The {noun1} was {adj1} but the {noun2} was {adj2}.",
    "{name1} {v_past1} and then {v_past2}.",
    "She {v_past1} the {noun1} with a {adj1} {noun2}.",
    "He did not {v_base1} the {adj1} {noun1}.",
    "All the {nouns1} were {adj1} that day.",
    "The {noun1} looked {adj1} in the {noun2}.",
    "{name1} always {v_past1} the {nouns1}.",
    "They {v_past1} the {noun1} and {v_past2} the {noun2}.",
    "The {adj1} {noun1} {v_past1} the {adj2} {noun2}.",
    "No one {v_past1} the {adj1} {noun1}.",
    "The {noun1} did not {v_base1}.",
    "I {v_past1} a {adj1} {noun1} on the {noun2}.",
    "{name1} and {name2} {v_past1} together.",
]

MEDIUM_TEMPLATES = [
    # compound sentences, commas, varied structure
    "{name1} {v_past1} the {adj1} {noun1}, and the {noun2} {v_past2} {adv1}.",
    "The {adj1} {noun1} {v_past1} {prep1} the {noun2}, but no one {v_past2}.",
    "After the {noun1} {v_past1}, the {adj1} {noun2} began to {v_base1}.",
    "{time1}, {name1} {v_past1} {prep1} the {adj1} {noun1} and {v_past2}.",
    "The {nouns1} {v_past1} {adv1}, and the {adj1} {noun1} {v_past2} {prep1} the {noun2}.",
    "{name1} {v_past1} the {noun1} that {v_past2} {prep1} the {adj1} {noun2}.",
    "Before the {noun1} could {v_base1}, {name1} {v_past1} the {adj1} {noun2}.",
    "The {noun1} {v_past1} {prep1} the {noun2}; it was {adv1} {adj1}.",
    "{name1} had never {v_past1} such a {adj1} {noun1} before.",
    "With a {adj1} {noun1}, {name1} {v_past1} {prep1} the {noun2}.",
    "She {v_past1} the {adj1} {noun1}, hoping to {v_base1} the {noun2}.",
    "The {adj1} {noun1} and the {adj2} {noun2} {v_past1} together.",
    "He {v_past1} {adv1}, for the {noun1} was {adj1} and {adj2}.",
    "As the {noun1} {v_past1}, the {nouns1} began to {v_base1}.",
    "They {v_past1} the {adj1} {noun1}, which {v_past2} {prep1} the {noun2}.",
    "{name1} {v_past1} that the {noun1} would {v_base1} {time1}.",
    "Despite the {adj1} {noun1}, {name1} {v_past1} to {v_base1}.",
    "Every {noun1} in the {noun2} {v_past1} {adv1} that day.",
    "The {noun1} {v_past1}, and {name1} {v_past2} {prep1} the {adj1} {noun2}.",
    "{name1} {v_past1} {prep1} the {noun1}, {v_ing1} the {adj1} {noun2}.",
    "It seemed that the {adj1} {noun1} had {v_past1} the {noun2} {adv1}.",
    "The {nouns1} could not {v_base1}; they {v_past1} {adv1} instead.",
    "{time1}, the {adj1} {noun1} finally {v_past1}.",
    "While {v_ing1} {prep1} the {noun1}, {name1} {v_past1} a {adj1} {noun2}.",
    "She {v_past1} the {noun1} and {v_past2} it {prep1} the {adj1} {noun2}.",
    "If the {noun1} had {v_past1}, the {noun2} would have {v_past2}.",
    "Somewhere {prep1} the {noun1}, a {adj1} {noun2} was {v_ing1}.",
    "The {adj1} {noun1} {v_past1} without a {noun2} to {v_base1}.",
    "{name1} could hear {nouns1} {v_ing1} {prep1} the {adj1} {noun1}.",
    "{name1} often {v_past1} the {adj1} {nouns1} that {v_past2} {prep1} the {noun1}.",
    "Although the {noun1} was {adj1}, {name1} {v_past1} it {adv1}.",
    "A {adj1} {noun1} {v_past1} the {noun2}, and {name1} {v_past2} {adv1}.",
    "The {noun1} {v_past1} so {adv1} that the {nouns1} {v_past2}.",
    "Nobody could {v_base1} why the {adj1} {noun1} had {v_past1}.",
    "She {v_past1} {prep1} the {noun1} and into the {adj1} {noun2}.",
    "He wanted to {v_base1} the {noun1}, but the {noun2} {v_past1} first.",
    "There was a {adj1} {noun1} {v_ing1} {prep1} the {noun2}.",
    "{name1} believed the {adj1} {noun1} would never {v_base1}.",
    "It was {adj1}; the {nouns1} {v_past1} and the {noun1} grew {adj2}.",
    "The {noun1} slowly {v_past1}, and the {adj1} {noun2} {v_past2}.",
]

HARD_TEMPLATES = [
    # complex clauses, semicolons, parenthetical phrases
    "Although the {adj1} {noun1} had {v_past1} {adv1}, the {noun2} remained {adj2}; no one could {v_base1} it.",
    "The {noun1}, which had been {v_ing1} {prep1} the {adj1} {noun2}, suddenly {v_past1} without {v_ing2}.",
    "{name1} believed that the {adj1} {noun1} would {v_base1}; however, the {noun2} {v_past1} {adv1}.",
    "Having {v_past1} the {adj1} {noun1} {time1}, {name1} {v_past2} the {adj2} {noun2} with {adj3} {noun3}.",
    "The {adj1} {noun1}, {adv1} {v_ing1} {prep1} the {noun2}, {v_past1} the {adj2} {noun3} that {v_past2} {prep2} the {noun4}.",
    "It was neither the {adj1} {noun1} nor the {adj2} {noun2} that {v_past1}; rather, it was the {noun3} itself.",
    "While the {nouns1} {v_past1} {adv1} {prep1} the {noun1}, {name1} {v_past2} the {adj1} {noun2} that {v_past3} {prep2} the {noun3}.",
    "The {noun1} {v_past1} {adv1}, not because the {noun2} was {adj1}, but because the {adj2} {noun3} had {v_past2}.",
    "{name1}, who had {adv1} {v_past1} the {adj1} {noun1}, could not {v_base1} why the {noun2} {v_past2} so {adv2}.",
    "Beneath the {adj1} {noun1} lay a {adj2} {noun2}, {v_ing1} {adv1} as the {nouns1} {v_past1} {prep1} it.",
    "Neither the {adj1} {noun1} nor the {adj2} {noun2} could {v_base1} what {name1} had {v_past1}.",
    "The {adj1} {noun1} {v_past1} {prep1} the {noun2}, {v_ing1} every {noun3} that {v_past2} in its {noun4}.",
    "{time1}, when the {adj1} {noun1} {v_past1} the {noun2}, {name1} {v_past2} that something had {v_past3}.",
    "Despite {v_ing1} the {adj1} {noun1} {adv1}, {name1} {v_past1} that the {noun2} would not {v_base1} without {adj2} {noun3}.",
    "The {noun1} had {v_past1} {adv1}; the {adj1} {noun2}, however, {v_past2} {prep1} the {noun3} as though nothing had {v_past3}.",
    "In the {adj1} {noun1}, where {nouns1} once {v_past1} {adv1}, there now stood a {adj2} {noun2} {v_ing1} in the {noun3}.",
    "{name1} {v_past1} the {adj1} {noun1} and, without {v_ing1}, {v_past2} {prep1} the {adj2} {noun2} that {v_past3} {prep2} the {noun3}.",
    "The {nouns1}, which had been {v_ing1} {prep1} the {noun1} for some time, {adv1} {v_past1} when the {adj1} {noun2} {v_past2}.",
    "What {name1} had {v_past1} was not merely a {adj1} {noun1}; it was the {adj2} {noun2} that {v_past2} the entire {noun3}.",
    "Though the {adj1} {noun1} seemed {adj2}, {name1} {v_past1} {adv1} that the {noun2} was far more {adj3} than it appeared.",
    "By the time the {adj1} {noun1} had {v_past1}, the {nouns1} were already {v_ing1} {prep1} the {adj2} {noun2}.",
    "The {noun1}, once {adj1} and {adj2}, had {v_past1} into something {adv1} {adj3}; {name1} could barely {v_base1} it.",
    "{name1} {v_past1} that the {adj1} {noun1}, despite its {adj2} {noun2}, would eventually {v_base1} the {noun3}.",
    "There existed, {prep1} the {adj1} {noun1}, a {noun2} of such {adj2} {noun3} that even {name1} {v_past1} in {noun4}.",
    "So {adj1} was the {noun1} that the {nouns1} could only {v_base1} and {v_base2}, unable to {v_base3} any further.",
    "It was {time1} that {name1} first {v_past1} the {adj1} {noun1}; since then, the {noun2} had never {v_past2} the same.",
    "Between the {adj1} {noun1} and the {adj2} {noun2}, a {adj3} {noun3} {v_past1}, {v_ing1} {adv1} in the {noun4}.",
    "The {adj1} {noun1} {v_past1} {adv1}, as if it had {v_past2} every {noun2} and {noun3} along the {noun4}.",
    "Had the {noun1} not {v_past1} so {adv1}, the {adj1} {noun2} might have {v_past2} the {noun3} entirely.",
    "At the center of the {adj1} {noun1} stood a {adj2} {noun2}, its {noun3} {v_ing1} {adv1} in the {adj3} {noun4}.",
    "Whether the {adj1} {noun1} had truly {v_past1} or merely {v_past2} remained a {noun2} that {name1} could not {v_base1}.",
    "The {noun1} that {name1} had {v_past1} {time1} was not the same {noun2} that now {v_past2} {prep1} the {adj1} {noun3}.",
    "{name1}, {v_ing1} {prep1} the {adj1} {noun1}, {v_past1} the {adj2} {noun2} and then {v_past2} {adv1} {prep2} the {noun3}.",
    "Even the {adj1} {nouns1} that {v_past1} {prep1} the {noun1} could not {v_base1} the {adj2} {noun2} that {v_past2} {prep2} the {noun3}.",
    "The {adj1} {noun1} {v_past1}, {v_past2}, and {v_past3}; still, the {noun2} refused to {v_base1}.",
    "As {name1} {v_past1} {prep1} the {adj1} {noun1}, the {adj2} {nouns1} {v_past2} {adv1}, {v_ing1} the {noun2} in {adj3} {noun3}.",
    "Not since {time1} had the {adj1} {noun1} {v_past1} so {adv1}; {name1} {v_past2} in {adj2} {noun2}.",
    "{name1} {adv1} {v_past1} the {noun1}, knowing that the {adj1} {noun2} {prep1} the {noun3} would never {v_base1} again.",
    "The {adj1} {noun1} and the {adj2} {noun2} {v_past1} {prep1} one another, neither willing to {v_base1} nor to {v_base2}.",
    "Whatever {name1} had {v_past1} {prep1} the {adj1} {noun1} was {adv1} {v_past2} by the {adj2} {noun2} that followed.",
]

TEMPLATES = {
    "easy": EASY_TEMPLATES,
    "medium": MEDIUM_TEMPLATES,
    "hard": HARD_TEMPLATES,
}


# ── generator ────────────────────────────────────────────────────────────────

def generate(count=80, difficulty="medium"):
    """Generate natural sentences totaling approximately `count` words."""
    pools = get_pools(difficulty)
    templates = TEMPLATES.get(difficulty, MEDIUM_TEMPLATES)
    sentences = []
    total_words = 0

    while total_words < count:
        tmpl = random.choice(templates)
        filler = _Filler(pools)
        sentence = tmpl.format_map(filler)
        sentences.append(sentence)
        total_words += len(sentence.split())

    return " ".join(sentences)
