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
    "{pron1} {v_past1} a {adj1} {noun1}.",
    "The {adj1} {noun1} was very {adj2}.",
    "I {v_past1} the {noun1} {prep1} the {noun2}.",
    "{pron1} {v_past1} {adv1} and {v_past2} away.",
    "The {noun1} {v_past1} {prep1} the {adj1} {noun2}.",
    "A {adj1} {noun1} sat {prep1} the {noun2}.",
    "{pron1} could see the {adj1} {noun1}.",
    "The {adj1} {noun1} {v_past1} {adv1}.",
    "We {v_past1} the {noun1} and the {noun2}.",
    "She {v_past1} the {adj1} {noun1} {prep1} the {noun2}.",
    "He {v_past1} a {noun1} and {v_past2} home.",
    "The {nouns1} were {adj1} and {adj2}.",
    "It was a {adj1} day in the {noun1}.",
    "The {noun1} fell {prep1} the {adj1} {noun2}.",
    "A {noun1} and a {noun2} sat {prep1} the {noun3}.",
    "They {v_past1} the {adj1} {noun1} {time1}.",
    "Every {noun1} had a {adj1} {noun2}.",
    "The {adj1} {nouns1} {v_past1} {prep1} the {noun1}.",
    "She liked the {adj1} {noun1} very much.",
    "It was {adj1} and {adj2} outside.",
    "The {noun1} {v_past1} but the {noun2} did not.",
    "He {v_past1} {adv1} {prep1} the {noun1}.",
    "The old {noun1} stood {prep1} the {noun2}.",
    "{pron1} {v_past1} the door and {v_past2} inside.",
    "We could hear the {adj1} {noun1} from here.",
    "A {adj1} {noun1} {v_past1} down the {noun2}.",
    "The {noun1} was {adj1} but the {noun2} was {adj2}.",
    "{pron1} {v_past1} and then {v_past2}.",
    "She {v_past1} the {noun1} with a {adj1} {noun2}.",
    "He did not {v_base1} the {adj1} {noun1}.",
    "All the {nouns1} were {adj1} that day.",
    "The {noun1} looked {adj1} in the {noun2}.",
    "{pron1} always {v_past1} the {nouns1}.",
    "They {v_past1} the {noun1} and {v_past2} the {noun2}.",
    "The {adj1} {noun1} {v_past1} the {adj2} {noun2}.",
    "No one {v_past1} the {adj1} {noun1}.",
    "The {noun1} did not {v_base1}.",
    "I {v_past1} a {adj1} {noun1} on the {noun2}.",
    "The {noun1} and the {noun2} {v_past1} together.",
    "The {noun1} was {adv1} {adj1}.",
    "{pron1} {v_past1} a {noun1} for the {noun2}.",
    "Did the {adj1} {noun1} {v_base1} the {noun2}?",
    "The {noun1} and the {noun2} were both {adj1}.",
    "What a {adj1} {noun1} it was!",
    "{pron1} {v_past1} every {noun1} in the {noun2}.",
    "There was a {adj1} {noun1} on the {noun2}.",
    "The {noun1} {v_past1} and the {noun2} {v_past2}.",
    "Why did the {noun1} {v_base1} the {adj1} {noun2}?",
    "{pron1} found a {adj1} {noun1} by the {noun2}.",
    "The {adj1} {noun1} could not {v_base1} at all.",
    "Every {noun1} in the {noun2} was {adj1}.",
    "She {v_past1} the {noun1}, but he {v_past2} the {noun2}.",
    "How {adj1} the {noun1} looked that day!",
    "{pron1} {adv1} {v_past1} a {noun1}.",
    "The {nouns1} {v_past1} while the {noun1} {v_past2}.",
    "A {noun1} {v_past1} over the {adj1} {noun2}.",
    "He gave the {noun1} a {adj1} {noun2}.",
    # present tense
    "The {noun1} {v_pres1} the {adj1} {noun2} every day.",
    "A {adj1} {noun1} {v_pres1} {prep1} the {noun2}.",
    "She {v_pres1} the {noun1} and he {v_pres2} the {noun2}.",
    "The {adj1} {noun1} {v_pres1} {adv1}.",
    "Every {noun1} {v_pres1} the {adj1} {noun2}.",
    "He {v_pres1} the {nouns1} {prep1} the {noun1}.",
    "They {v_base1} the {noun1} and {v_base2} the {noun2}.",
    "We {v_base1} {adj1} {nouns1} {prep1} the {noun1}.",
    "The {noun1} does not {v_base1} the {adj1} {noun2}.",
    # passive voice
    "The {noun1} was {v_past1} by the {adj1} {noun2}.",
    "The {adj1} {nouns1} were {v_past1} {prep1} the {noun1}.",
    "A {adj1} {noun1} was {v_past1} {prep1} the {noun2}.",
    # questions and exclamations
    "Where did the {adj1} {noun1} {v_base1}?",
    "How did the {noun1} {v_base1} the {adj1} {noun2}?",
    "What {adj1} {noun1} could {v_base1} so {adv1}?",
    "Is the {noun1} still {v_ing1} {prep1} the {noun2}?",
    "Who {v_past1} the {adj1} {noun1} {prep1} the {noun2}?",
    # gerund-led
    "{v_ing1} the {noun1}, the {noun2} {v_past1} {adv1}.",
    "{v_ing1} {adv1}, the {adj1} {noun1} {v_past1}.",
    # lists, comparisons
    "The {noun1} was more {adj1} than the {noun2}.",
    "The {noun1} {v_past1} {adv1}, like a {adj1} {noun2}.",
    "Both the {noun1} and the {noun2} {v_past1} {adv1}.",
    "The {noun1}, the {noun2}, and the {noun3} were all {adj1}.",
    "Neither the {noun1} nor the {noun2} {v_past1}.",
    # conditionals
    "If the {noun1} {v_past1}, the {noun2} would {v_base1}.",
    # more simple variety
    "The {adj1} {noun1} {v_past1} the {noun2} {time1}.",
    "{pron1} {v_past1} the {adj1} {noun1} and left.",
    "I could see the {nouns1} {prep1} the {adj1} {noun1}.",
    "There were {adj1} {nouns1} all {prep1} the {noun1}.",
    "The {noun1} had a {adj1} {noun2} {prep1} its {noun3}.",
    "It grew {adj1} and the {nouns1} {v_past1}.",
    "We {v_past1} the {adj1} {noun1} with {adj2} {nouns1}.",
    "The {noun1} was too {adj1} to {v_base1}.",
    "She {v_past1} it {prep1} the {adj1} {noun1}.",
    "He {v_past1} the {noun1}, and it was {adj1}.",
    "A {noun1} {v_past1} and a {noun2} {v_past2}.",
    "The {adj1} {noun1} {v_past1} right {prep1} the {noun2}.",
    "{pron1} never {v_past1} the {adj1} {noun1}.",
    "The {nouns1} and the {nouns2} were {adj1}.",
    "Something {v_past1} {prep1} the {adj1} {noun1}.",
    "The {noun1} {v_past1} as the {noun2} {v_past2}.",
    "I {v_past1} the {noun1} before the {noun2} could {v_base1}.",
]

MEDIUM_TEMPLATES = [
    # compound sentences, commas, varied structure
    "{pron1} {v_past1} the {adj1} {noun1}, and the {noun2} {v_past2} {adv1}.",
    "The {adj1} {noun1} {v_past1} {prep1} the {noun2}, but no one {v_past2}.",
    "After the {noun1} {v_past1}, the {adj1} {noun2} began to {v_base1}.",
    "{time1}, {pron1} {v_past1} {prep1} the {adj1} {noun1} and {v_past2}.",
    "The {nouns1} {v_past1} {adv1}, and the {adj1} {noun1} {v_past2} {prep1} the {noun2}.",
    "{pron1} {v_past1} the {noun1} that {v_past2} {prep1} the {adj1} {noun2}.",
    "Before the {noun1} could {v_base1}, {pron1} {v_past1} the {adj1} {noun2}.",
    "The {noun1} {v_past1} {prep1} the {noun2}; it was {adv1} {adj1}.",
    "{pron1} had never {v_past1} such a {adj1} {noun1} before.",
    "With a {adj1} {noun1}, {pron1} {v_past1} {prep1} the {noun2}.",
    "She {v_past1} the {adj1} {noun1}, hoping to {v_base1} the {noun2}.",
    "The {adj1} {noun1} and the {adj2} {noun2} {v_past1} together.",
    "He {v_past1} {adv1}, for the {noun1} was {adj1} and {adj2}.",
    "As the {noun1} {v_past1}, the {nouns1} began to {v_base1}.",
    "They {v_past1} the {adj1} {noun1}, which {v_past2} {prep1} the {noun2}.",
    "{pron1} {v_past1} that the {noun1} would {v_base1} {time1}.",
    "Despite the {adj1} {noun1}, {pron1} {v_past1} to {v_base1}.",
    "Every {noun1} in the {noun2} {v_past1} {adv1} that day.",
    "The {noun1} {v_past1}, and the {adj1} {noun2} {v_past2} {prep1} the {noun3}.",
    "{pron1} {v_past1} {prep1} the {noun1}, {v_ing1} the {adj1} {noun2}.",
    "It seemed that the {adj1} {noun1} had {v_past1} the {noun2} {adv1}.",
    "The {nouns1} could not {v_base1}; they {v_past1} {adv1} instead.",
    "{time1}, the {adj1} {noun1} finally {v_past1}.",
    "While {v_ing1} {prep1} the {noun1}, {pron1} {v_past1} a {adj1} {noun2}.",
    "She {v_past1} the {noun1} and {v_past2} it {prep1} the {adj1} {noun2}.",
    "If the {noun1} had {v_past1}, the {noun2} would have {v_past2}.",
    "Somewhere {prep1} the {noun1}, a {adj1} {noun2} was {v_ing1}.",
    "The {adj1} {noun1} {v_past1} without a {noun2} to {v_base1}.",
    "{pron1} could hear {nouns1} {v_ing1} {prep1} the {adj1} {noun1}.",
    "{pron1} often {v_past1} the {adj1} {nouns1} that {v_past2} {prep1} the {noun1}.",
    "Although the {noun1} was {adj1}, the {noun2} {v_past1} it {adv1}.",
    "A {adj1} {noun1} {v_past1} the {noun2}, and {pron1} {v_past2} {adv1}.",
    "The {noun1} {v_past1} so {adv1} that the {nouns1} {v_past2}.",
    "Nobody could {v_base1} why the {adj1} {noun1} had {v_past1}.",
    "She {v_past1} {prep1} the {noun1} and into the {adj1} {noun2}.",
    "He wanted to {v_base1} the {noun1}, but the {noun2} {v_past1} first.",
    "There was a {adj1} {noun1} {v_ing1} {prep1} the {noun2}.",
    "{pron1} believed the {adj1} {noun1} would never {v_base1}.",
    "It was {adj1}; the {nouns1} {v_past1} and the {noun1} grew {adj2}.",
    "The {noun1} slowly {v_past1}, and the {adj1} {noun2} {v_past2}.",
    "Was it the {adj1} {noun1} that {v_past1}, or had the {noun2} {v_past2} {adv1}?",
    "Neither the {noun1} nor the {adj1} {noun2} could {v_base1} the {noun3} that {v_past1} {prep1} the {noun4}.",
    "{pron1} {v_past1} the {adj1} {noun1}; yet the {noun2} remained {adv1} {adj2}.",
    "How {adv1} the {adj1} {noun1} had {v_past1}, {pron1} could not quite {v_base1}.",
    "Once the {noun1} {v_past1}, the {adj1} {nouns1} began {v_ing1} {prep1} the {noun2}.",
    "The {noun1} that {pron1} {v_past1} was {adv1} more {adj1} than the {noun2}.",
    "Without the {adj1} {noun1}, the {noun2} could not have {v_past1} the {noun3}.",
    "Every {noun1} {prep1} the {adj1} {noun2} seemed to {v_base1} {adv1}.",
    "What had {pron1} {v_past1} {prep1} the {adj1} {noun1}?",
    "As the {noun1} {v_past1} the {noun2}, the {adj1} {noun3} {v_past2} {prep1} the {noun4}.",
    "The {adj1} {noun1} {v_past1}, leaving the {nouns1} to {v_base1} {adv1}.",
    "Far {prep1} the {noun1}, a {adj1} {noun2} was {v_ing1} in the {noun3}.",
    "The {noun1} never {v_past1} why the {adj1} {noun2} {v_past2} so {adv1}.",
    "Until the {noun1} {v_past1}, the {adj1} {nouns1} had been {v_ing1} {prep1} the {noun2}.",
    "So {adj1} was the {noun1} that {pron1} {v_past1} {adv1}.",
    "The {noun1} {v_past1} the {adj1} {noun2}, and soon the {nouns1} {v_past2} as well.",
    "{time1}, a {adj1} {noun1} {v_past1} {prep1} the {noun2} and {v_past2} everything.",
    "Would the {adj1} {noun1} ever {v_base1} again, or had it {v_past1} for the last time?",
    # present tense
    "The {adj1} {noun1} {v_pres1} the {noun2} whenever the {noun3} {v_pres2}.",
    "Every {noun1} {v_pres1} {adv1}, but the {adj1} {noun2} {v_pres2} {adv2}.",
    "{pron1} {v_pres1} the {adj1} {nouns1} that {v_base1} {prep1} the {noun1}.",
    "The {noun1} {v_pres1} {prep1} the {noun2}, {v_ing1} the {adj1} {noun3}.",
    "She {v_pres1} the {noun1} while he {v_pres2} the {adj1} {noun2}.",
    "Whenever the {noun1} {v_pres1}, the {adj1} {nouns1} {v_base1} {adv1}.",
    # passive voice
    "The {adj1} {noun1} was {v_past1} by a {noun2} that had {v_past2} {prep1} the {noun3}.",
    "The {nouns1} were {v_past1} {adv1}, and the {adj1} {noun1} was {v_past2} as well.",
    "The {noun1} had been {v_past1} {prep1} the {adj1} {noun2} for a long time.",
    # questions
    "Why had the {adj1} {noun1} {v_past1} when the {noun2} was still {v_ing1}?",
    "Could the {noun1} {v_base1} the {adj1} {noun2} before the {noun3} {v_past1}?",
    "Had the {adj1} {noun1} truly {v_past1}, or was the {noun2} still {v_ing1}?",
    # gerund-led
    "{v_ing1} the {adj1} {noun1}, {pron1} {v_past1} the {noun2} {adv1}.",
    "{v_ing1} {prep1} the {noun1}, the {adj1} {noun2} {v_past1} {prep2} the {noun3}.",
    "After {v_ing1} the {noun1}, the {adj1} {noun2} {v_past1} {adv1}.",
    # comparisons and lists
    "The {noun1} was more {adj1} than the {noun2}, and the {noun3} was the most {adj2} of all.",
    "The {adj1} {noun1} {v_past1} the {noun2}, the {noun3}, and the {noun4}.",
    "Neither the {adj1} {noun1} nor the {adj2} {noun2} could {v_base1} the {noun3}.",
    # conditionals
    "If the {noun1} {v_past1} the {adj1} {noun2}, then the {nouns1} would {v_base1}.",
    "Unless the {adj1} {noun1} {v_past1}, the {noun2} could not {v_base1}.",
    # more compound variety
    "The {noun1} {v_past1} the {adj1} {noun2}; the {noun3}, however, {v_past2} {adv1}.",
    "She {v_past1} {adv1} and he {v_past2} {adv2}; the {noun1} {v_past3} {prep1} them.",
    "A {adj1} {noun1} and a {adj2} {noun2} {v_past1} {prep1} the {noun3} {time1}.",
    "{pron1} {v_past1} the {noun1} that the {adj1} {noun2} had {v_past2}.",
    "The {adj1} {noun1} {v_past1}, but the {nouns1} {v_past2} {adv1} {prep1} the {noun2}.",
    "They could not {v_base1} the {adj1} {noun1}; it was too {adj2} to {v_base2}.",
    "When the {noun1} {v_past1}, the {adj1} {noun2} began {v_ing1} {adv1}.",
    "The {adj1} {noun1} {v_past1} {prep1} the {noun2} as the {nouns1} {v_past2}.",
    "Across the {adj1} {noun1}, the {nouns1} {v_past1} {adv1} toward the {noun2}.",
    "{time1}, the {nouns1} {v_past1} and the {adj1} {noun1} {v_past2} {prep1} the {noun2}.",
    "The {noun1} {v_past1} the {noun2}, which {v_past2} the {adj1} {noun3} {adv1}.",
    "He {v_past1} every {noun1} he could {v_base1}, yet the {adj1} {noun2} remained.",
    "What the {noun1} {v_past1} was {adj1}; what the {noun2} {v_past2} was {adj2}.",
    "She had {v_past1} the {adj1} {noun1} long before the {noun2} {v_past2}.",
    "The {noun1} {v_past1} {adv1}, and not a single {noun2} {v_past2}.",
    "Between the {adj1} {noun1} and the {noun2}, {pron1} {v_past1} a {adj2} {noun3}.",
    "It was not the {noun1} but the {adj1} {noun2} that {v_past1} {adv1}.",
    "The {adj1} {noun1}, though {adj2}, {v_past1} the {noun2} without {v_ing1}.",
    "Once, the {nouns1} had {v_past1} {adv1}; now, they {v_past2} in {adj1} {noun1}.",
    "The {adj1} {noun1} {v_past1} {prep1} the {noun2}, and the {adj2} {nouns1} {v_past2}.",
    "He {v_past1} the {noun1} while she {v_past2} the {adj1} {noun2} {prep1} the {noun3}.",
    "{pron1} {v_past1} that the {adj1} {noun1} had been {v_ing1} {prep1} the {noun2}.",
]

HARD_TEMPLATES = [
    # complex clauses, semicolons, parenthetical phrases
    "Although the {adj1} {noun1} had {v_past1} {adv1}, the {noun2} remained {adj2}; no one could {v_base1} it.",
    "The {noun1}, which had been {v_ing1} {prep1} the {adj1} {noun2}, suddenly {v_past1} without {v_ing2}.",
    "{pron1} believed that the {adj1} {noun1} would {v_base1}; however, the {noun2} {v_past1} {adv1}.",
    "Having {v_past1} the {adj1} {noun1} {time1}, {pron1} {v_past2} the {adj2} {noun2} with {adj3} {noun3}.",
    "The {adj1} {noun1}, {adv1} {v_ing1} {prep1} the {noun2}, {v_past1} the {adj2} {noun3} that {v_past2} {prep2} the {noun4}.",
    "It was neither the {adj1} {noun1} nor the {adj2} {noun2} that {v_past1}; rather, it was the {noun3} itself.",
    "While the {nouns1} {v_past1} {adv1} {prep1} the {noun1}, the {adj1} {noun2} {v_past2} the {noun3} that {v_past3} {prep2} the {noun4}.",
    "The {noun1} {v_past1} {adv1}, not because the {noun2} was {adj1}, but because the {adj2} {noun3} had {v_past2}.",
    "{pron1}, who had {adv1} {v_past1} the {adj1} {noun1}, could not {v_base1} why the {noun2} {v_past2} so {adv2}.",
    "Beneath the {adj1} {noun1} lay a {adj2} {noun2}, {v_ing1} {adv1} as the {nouns1} {v_past1} {prep1} it.",
    "Neither the {adj1} {noun1} nor the {adj2} {noun2} could {v_base1} what the {noun3} had {v_past1}.",
    "The {adj1} {noun1} {v_past1} {prep1} the {noun2}, {v_ing1} every {noun3} that {v_past2} in its {noun4}.",
    "{time1}, when the {adj1} {noun1} {v_past1} the {noun2}, {pron1} {v_past2} that something had {v_past3}.",
    "Despite {v_ing1} the {adj1} {noun1} {adv1}, {pron1} {v_past1} that the {noun2} would not {v_base1} without {adj2} {noun3}.",
    "The {noun1} had {v_past1} {adv1}; the {adj1} {noun2}, however, {v_past2} {prep1} the {noun3} as though nothing had {v_past3}.",
    "In the {adj1} {noun1}, where {nouns1} once {v_past1} {adv1}, there now stood a {adj2} {noun2} {v_ing1} in the {noun3}.",
    "{pron1} {v_past1} the {adj1} {noun1} and, without {v_ing1}, {v_past2} {prep1} the {adj2} {noun2} that {v_past3} {prep2} the {noun3}.",
    "The {nouns1}, which had been {v_ing1} {prep1} the {noun1} for some time, {adv1} {v_past1} when the {adj1} {noun2} {v_past2}.",
    "What the {noun1} had {v_past1} was not merely a {adj1} {noun2}; it was the {adj2} {noun3} that {v_past2} the entire {noun4}.",
    "Though the {adj1} {noun1} seemed {adj2}, {pron1} {v_past1} {adv1} that the {noun2} was far more {adj3} than it appeared.",
    "By the time the {adj1} {noun1} had {v_past1}, the {nouns1} were already {v_ing1} {prep1} the {adj2} {noun2}.",
    "The {noun1}, once {adj1} and {adj2}, had {v_past1} into something {adv1} {adj3}; {pron1} could barely {v_base1} it.",
    "{pron1} {v_past1} that the {adj1} {noun1}, despite its {adj2} {noun2}, would eventually {v_base1} the {noun3}.",
    "There existed, {prep1} the {adj1} {noun1}, a {noun2} of such {adj2} {noun3} that even the {noun4} {v_past1}.",
    "So {adj1} was the {noun1} that the {nouns1} could only {v_base1} and {v_base2}, unable to {v_base3} any further.",
    "It was {time1} that {pron1} first {v_past1} the {adj1} {noun1}; since then, the {noun2} had never {v_past2} the same.",
    "Between the {adj1} {noun1} and the {adj2} {noun2}, a {adj3} {noun3} {v_past1}, {v_ing1} {adv1} in the {noun4}.",
    "The {adj1} {noun1} {v_past1} {adv1}, as if it had {v_past2} every {noun2} and {noun3} along the {noun4}.",
    "Had the {noun1} not {v_past1} so {adv1}, the {adj1} {noun2} might have {v_past2} the {noun3} entirely.",
    "At the center of the {adj1} {noun1} stood a {adj2} {noun2}, its {noun3} {v_ing1} {adv1} in the {adj3} {noun4}.",
    "Whether the {adj1} {noun1} had truly {v_past1} or merely {v_past2} remained a {noun2} that no one could {v_base1}.",
    "The {noun1} that {pron1} had {v_past1} {time1} was not the same {noun2} that now {v_past2} {prep1} the {adj1} {noun3}.",
    "{pron1}, {v_ing1} {prep1} the {adj1} {noun1}, {v_past1} the {adj2} {noun2} and then {v_past2} {adv1} {prep2} the {noun3}.",
    "Even the {adj1} {nouns1} that {v_past1} {prep1} the {noun1} could not {v_base1} the {adj2} {noun2} that {v_past2} {prep2} the {noun3}.",
    "The {adj1} {noun1} {v_past1}, {v_past2}, and {v_past3}; still, the {noun2} refused to {v_base1}.",
    "As {pron1} {v_past1} {prep1} the {adj1} {noun1}, the {adj2} {nouns1} {v_past2} {adv1}, {v_ing1} the {noun2} in {adj3} {noun3}.",
    "Not since {time1} had the {adj1} {noun1} {v_past1} so {adv1}; the {noun2} {v_past2} in {adj2} {noun3}.",
    "{pron1} {adv1} {v_past1} the {noun1}, knowing that the {adj1} {noun2} {prep1} the {noun3} would never {v_base1} again.",
    "The {adj1} {noun1} and the {adj2} {noun2} {v_past1} {prep1} one another, neither willing to {v_base1} nor to {v_base2}.",
    "Whatever the {noun1} had {v_past1} {prep1} the {adj1} {noun2} was {adv1} {v_past2} by the {adj2} {noun3} that followed.",
    "Could the {adj1} {noun1}, which had {v_past1} so {adv1} {prep1} the {noun2}, truly {v_base1} what {pron1} had {v_past2}?",
    "The {noun1} that {pron1} {v_past1} {time1} had since {v_past2}; the {adj1} {noun2} {prep1} the {noun3} was all that {v_past3}.",
    "What {pron1} could not {v_base1} was why the {adj1} {noun1}, having {v_past1} the {noun2} {adv1}, would then {v_base2} the {adj2} {noun3}.",
    "In every {noun1} there {v_past1} a {adj1} {noun2}; in every {noun3} there {v_past2} a {adj2} {noun4} waiting to {v_base1}.",
    "The {adj1} {nouns1}, {v_ing1} {adv1} {prep1} the {noun1}, had not {v_past1} that the {adj2} {noun2} would {v_base1} so {adv2}.",
    "How the {adj1} {noun1} had {v_past1} remained unclear; what was certain was that the {noun2} {v_past2} the {adj2} {noun3} {adv1}.",
    "{pron1} {v_past1} {prep1} the {adj1} {noun1}, yet the {noun2}, {adj2} and {adj3}, {v_past2} {adv1} beyond the {noun3}.",
    "Once the {adj1} {noun1} {v_past1}, every {noun2} {prep1} the {noun3} {v_past2}; it was as though the {adj2} {noun4} had never {v_past3}.",
    "Far from {v_ing1} the {adj1} {noun1}, the {noun2} had {adv1} {v_past1} it; the {noun3}, {adj2} as it was, {v_past2} {prep1} the {noun4}.",
    "The {adj1} {noun1} {v_past1} not because the {nouns1} {v_past2}, but because {pron1}, who had {v_past3} the {adj2} {noun2}, could no longer {v_base1}.",
    "If the {adj1} {noun1} had {v_past1} {adv1} {prep1} the {noun2}, then the {noun3} would have {v_past2}; instead, it {v_past3} the {adj2} {noun4}.",
    "Never before had the {adj1} {noun1} {v_past1} so {adv1}, and {pron1}, {v_ing1} {prep1} the {adj2} {noun2}, {v_past2} that this was no {adj3} {noun3}.",
    "To {v_base1} the {adj1} {noun1} was one thing; to {v_base2} the {adj2} {noun2} that {v_past1} {prep1} it was something {adv1} different.",
    "The {noun1}, {adj1} though it was, had {v_past1} the {adj2} {noun2}; the {noun3} {v_past2} that nothing {prep1} the {noun4} would ever {v_base1} again.",
    "Such was the {adj1} {noun1} that {v_past1} {prep1} the {noun2} that even {pron1}, who had {adv1} {v_past2}, could not {v_base1} its {adj2} {noun3}.",
    "While the {adj1} {noun1} {v_past1} and the {nouns1} {v_past2} {adv1}, {pron1} {v_past3} the {adj2} {noun2}, {v_ing1} that the {noun3} would soon {v_base1}.",
    # present tense complex
    "The {adj1} {noun1} {v_pres1} the {noun2} {adv1}, yet the {adj2} {noun3} {v_pres2} as though the {noun4} does not {v_base1}.",
    "Every {noun1} that {v_pres1} {prep1} the {adj1} {noun2} also {v_pres2} the {adj2} {noun3}; such is the {noun4} of the {noun5}.",
    "The {noun1} {v_pres1} what the {adj1} {noun2} cannot {v_base1}; the {adj2} {noun3}, however, {v_pres2} neither.",
    # passive voice complex
    "The {adj1} {noun1} was {v_past1} by the {noun2} that had been {v_ing1} {prep1} the {adj2} {noun3} since {time1}.",
    "The {nouns1}, once {v_past1} {adv1} by the {adj1} {noun1}, were now {v_past2} {prep1} the {adj2} {noun2}.",
    "Having been {v_past1} by the {adj1} {noun1}, the {noun2} was {adv1} {v_past2} {prep1} the {adj2} {noun3}.",
    # questions complex
    "Had the {adj1} {noun1} not {v_past1} the {noun2} so {adv1}, would the {adj2} {noun3} have {v_past2} at all?",
    "What could the {adj1} {noun1} have {v_past1} that the {noun2} and the {noun3} had not already {v_past2}?",
    "Why, then, had the {adj1} {noun1} {v_past1} {adv1}, when every {noun2} {prep1} the {noun3} {v_past2} the opposite?",
    # gerund-led complex
    "{v_ing1} {adv1} {prep1} the {adj1} {noun1}, the {noun2} {v_past1} the {adj2} {noun3} that had {v_past2} {prep2} the {noun4}.",
    "After {v_ing1} the {adj1} {noun1} and {v_ing2} the {noun2}, {pron1} {v_past1} {adv1} {prep1} the {adj2} {noun3}.",
    "By {v_ing1} the {noun1} {adv1}, the {adj1} {noun2} managed to {v_base1} the {adj2} {noun3} that {v_past1} {prep1} the {noun4}.",
    # conditionals complex
    "If the {adj1} {noun1} had not {v_past1} the {noun2}, the {adj2} {nouns1} would never have {v_past2} {prep1} the {noun3}.",
    "Were it not for the {adj1} {noun1} that {v_past1} {prep1} the {noun2}, the {adj2} {noun3} might still be {v_ing1} {adv1}.",
    # more variety
    "The {noun1} {v_past1} {adv1}, {v_ing1} each {noun2} and {noun3} with {adj1} {noun4}; the {adj2} {noun5} alone {v_past2}.",
    "Across the {adj1} {noun1}, where the {nouns1} {v_past1} and the {nouns2} {v_past2}, a {adj2} {noun2} {v_past3} {adv1}.",
    "The {adj1} {noun1} that had {v_past1} the {noun2} {time1} now {v_past2} {adv1}; the {adj2} {noun3} could only {v_base1}.",
    "So {adv1} did the {adj1} {noun1} {v_base1} that the {nouns1} {v_past1}, and the {adj2} {noun2} {v_past2} {prep1} the {noun3}.",
    "The {adj1} {noun1} {v_past1} the {noun2}; the {adj2} {noun3} {v_past2} the {noun4}; and the {adj3} {noun5} {v_past3} them all.",
    "What the {adj1} {noun1} {v_past1} {prep1} the {noun2} was {adv1} less {adj2} than what the {noun3} {v_past2} {prep2} the {noun4}.",
    "Somewhere {prep1} the {adj1} {noun1} and the {adj2} {noun2}, a {noun3} had been {v_ing1}, {adv1} {v_ing2} the {adj3} {noun4}.",
    "The {noun1} {v_past1}, the {noun2} {v_past2}, and the {adj1} {noun3} {v_past3}; none of the {nouns1} could {v_base1} what had {v_past4}.",
    "Although the {nouns1} {v_past1} and the {adj1} {noun1} {v_past2}, the {adj2} {noun2} {v_past3} {adv1} as if nothing had {v_past4}.",
    "It was the {adj1} {noun1}, {adv1} {v_ing1} {prep1} the {noun2}, that {v_past1} the {adj2} {noun3}; the {noun4} merely {v_past2}.",
    "With the {adj1} {noun1} {v_ing1} {prep1} the {noun2} and the {adj2} {noun3} {v_ing2} {prep2} the {noun4}, the {adj3} {noun5} finally {v_past1}.",
    "The {nouns1}, {adj1} and {adj2}, {v_past1} the {noun1} that {pron1} had {adv1} {v_past2}; no {noun2} could {v_base1} the {adj3} {noun3} now.",
    "Long before the {adj1} {noun1} {v_past1} the {noun2}, the {adj2} {noun3} had already {v_past2}; {pron1} {v_past3} too late.",
    "The {adj1} {noun1} {v_past1} {adv1}, as the {nouns1}, {v_ing1} {prep1} the {adj2} {noun2}, refused to {v_base1} the {noun3}.",
    "It was not merely the {adj1} {noun1} that had {v_past1}; it was the {adj2} {noun2} and the {adj3} {noun3} that {v_past2} {adv1} as well.",
    "Through the {adj1} {noun1}, past the {adj2} {noun2}, and beyond the {adj3} {noun3}, the {noun4} {v_past1} {adv1}, {v_ing1} everything in its {noun5}.",
    "Whether the {adj1} {noun1} {v_past1} or the {adj2} {noun2} {v_past2} made little difference; the {noun3} had already {v_past3} {adv1}.",
    "The {noun1} {v_past1}, and with it {v_past2} the {adj1} {noun2} that every {noun3} {prep1} the {adj2} {noun4} had once {v_past3}.",
    "No sooner had the {adj1} {noun1} {v_past1} than the {noun2}, {adj2} and {adj3}, {v_past2} {adv1} {prep1} the {noun3}.",
    "The {noun1} that {v_past1} {prep1} the {adj1} {noun2} was the very same {noun3} that had {v_past2} the {adj2} {noun4} {time1}.",
    "Whichever {noun1} {v_past1} the {adj1} {noun2} first would also {v_base1} the {adj2} {noun3}; this the {nouns1} {v_past2} {adv1}.",
    "Not only did the {adj1} {noun1} {v_base1} the {noun2}, but it also {v_past1} the {adj2} {noun3} that {v_past2} {prep1} the {noun4}.",
    "The {adj1} {noun1} and the {adj2} {noun2} had {v_past1} the same {noun3}; yet only the {noun4} {v_past2} when the {adj3} {noun5} {v_past3}.",
    "As the {adj1} {noun1} {v_past1} {adv1} and the {noun2} {v_past2}, the {nouns1} realized that no {noun3} could {v_base1} the {adj2} {noun4}.",
    "{pron1} had {adv1} {v_past1} the {adj1} {noun1} before the {noun2} {v_past2}; now the {adj2} {noun3} {v_past3} {prep1} the {noun4} alone.",
    "From the {adj1} {noun1} to the {adj2} {noun2}, every {noun3} had {v_past1}; even the {adj3} {nouns1} {v_past2} {adv1}.",
    "The {adj1} {noun1} {v_past1} where the {noun2} had once {v_past2}, and in its {noun3} {v_past3} a {adj2} {noun4} that would {v_base1} the {noun5}.",
    "Scarcely had the {noun1} {v_past1} when the {adj1} {noun2}, {v_ing1} {adv1}, {v_past2} the {adj2} {noun3} {prep1} the {noun4}.",
    "Whereas the {adj1} {noun1} had {v_past1} the {noun2} {adv1}, the {adj2} {noun3} {v_past2} {prep1} it with {adj3} {noun4}.",
    "The {adj1} {noun1}, having {v_past1} both the {noun2} and the {noun3}, {v_past2} {adv1} {prep1} the {adj2} {noun4} that {v_past3} them.",
]

TEMPLATES = {
    "easy": EASY_TEMPLATES,
    "medium": MEDIUM_TEMPLATES,
    "hard": HARD_TEMPLATES,
}


# ── shuffle-bag generator ───────────────────────────────────────────────────

_bags = {}


def generate(count=80, difficulty="medium"):
    """Generate natural sentences totaling approximately `count` words.

    Uses a shuffle-bag so every template is used once before any repeats.
    """
    pools = get_pools(difficulty)
    templates = TEMPLATES.get(difficulty, MEDIUM_TEMPLATES)
    sentences = []
    total_words = 0

    # get or create the shuffle bag for this difficulty
    bag, idx = _bags.get(difficulty, ([], 0))
    if not bag or idx >= len(bag):
        bag = list(templates)
        random.shuffle(bag)
        idx = 0

    while total_words < count:
        if idx >= len(bag):
            bag = list(templates)
            random.shuffle(bag)
            idx = 0
        tmpl = bag[idx]
        idx += 1
        filler = _Filler(pools)
        sentence = tmpl.format_map(filler)
        sentence = sentence[0].upper() + sentence[1:]
        sentences.append(sentence)
        total_words += len(sentence.split())

    _bags[difficulty] = (bag, idx)
    return " ".join(sentences)
