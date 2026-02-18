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
        # avoid words already picked in this sentence for the same category
        used = {v for k, v in self._cache.items() if k.rstrip("0123456789") == cat}
        remaining = [w for w in pool if w not in used]
        val = random.choice(remaining if remaining else pool)
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
    "The {noun1} was {adv1} {adj1}.",
    "{name1} {v_past1} a {noun1} for the {noun2}.",
    "Did the {adj1} {noun1} {v_base1} the {noun2}?",
    "The {noun1} and the {noun2} were both {adj1}.",
    "What a {adj1} {noun1} it was!",
    "{name1} {v_past1} every {noun1} in the {noun2}.",
    "There was a {adj1} {noun1} on the {noun2}.",
    "The {noun1} {v_past1} and the {noun2} {v_past2}.",
    "Why did the {noun1} {v_base1} the {adj1} {noun2}?",
    "{name1} found a {adj1} {noun1} by the {noun2}.",
    "The {adj1} {noun1} could not {v_base1} at all.",
    "Every {noun1} in the {noun2} was {adj1}.",
    "She {v_past1} the {noun1}, but he {v_past2} the {noun2}.",
    "How {adj1} the {noun1} looked that day!",
    "{name1} {adv1} {v_past1} a {noun1}.",
    "The {nouns1} {v_past1} while the {noun1} {v_past2}.",
    "A {noun1} {v_past1} over the {adj1} {noun2}.",
    "He gave {name1} a {adj1} {noun1}.",
    # ── expanded ──
    "The {noun1} near the {noun2} was {adj1}.",
    "{name1} never liked the {adj1} {noun1}.",
    "We saw a {adj1} {noun1} on the {noun2}.",
    "The {adj1} {noun1} broke the {noun2}.",
    "{name1} wore a {adj1} {noun1} and a {adj2} {noun2}.",
    "A {noun1} rolled down the {adj1} {noun2}.",
    "The {nouns1} hid {prep1} the {adj1} {noun1}.",
    "She could hear the {noun1} {prep1} the {noun2}.",
    "A {adj1} {noun1} lay {prep1} the {noun2}.",
    "{name1} {v_past1} the {noun1} {adv1}.",
    "The {noun1} grew {adj1} in the {noun2}.",
    "Two {nouns1} {v_past1} the {adj1} {noun1}.",
    "He put the {noun1} {prep1} the {adj1} {noun2}.",
    "There were {adj1} {nouns1} in the {noun1}.",
    "The {noun1} beside the {noun2} was {adj1} and {adj2}.",
    "{name1} gave the {adj1} {noun1} to {name2}.",
    "What {adj1} {nouns1} they were!",
    "She {v_past1} a {noun1} from the {adj1} {noun2}.",
    "They left the {adj1} {noun1} {prep1} the {noun2}.",
    "{name1} set the {noun1} {prep1} the {noun2}.",
    "The {adj1} {noun1} {v_past1} above the {nouns1}.",
    "Only the {adj1} {noun1} was left.",
    "I {v_past1} {name1} a {adj1} {noun1}.",
    "A {adj1} {noun1} and a {adj2} {noun2} were {prep1} the {noun3}.",
    "The {noun1} {v_past1}, and so did the {noun2}.",
    "{name1} {v_past1} past the {adj1} {noun1}.",
    "No {noun1} could {v_base1} the {adj1} {noun2}.",
    "He ran {prep1} the {adj1} {noun1} and the {noun2}.",
    "She thought the {noun1} was {adj1}.",
    "{name1} held a {adj1} {noun1} in each hand.",
    "The {noun1} {v_past1} across the {adj1} {noun2}.",
    "Both {nouns1} were {adj1} that {time1}.",
    "I {v_past1} the {adj1} {noun1} for {name1}.",
    "The {noun1} smelled {adj1} and {adj2}.",
    "Most of the {nouns1} {v_past1} {adv1}.",
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
    "Was it the {adj1} {noun1} that {v_past1}, or had the {noun2} {v_past2} {adv1}?",
    "Neither {name1} nor the {adj1} {noun1} could {v_base1} the {noun2} that {v_past1} {prep1} the {noun3}.",
    "{name1} {v_past1} the {adj1} {noun1}; yet the {noun2} remained {adv1} {adj2}.",
    "How {adv1} the {adj1} {noun1} had {v_past1}, {name1} could not quite {v_base1}.",
    "Once the {noun1} {v_past1}, the {adj1} {nouns1} began {v_ing1} {prep1} the {noun2}.",
    "The {noun1} that {name1} {v_past1} was {adv1} more {adj1} than the {noun2}.",
    "Without the {adj1} {noun1}, {name1} could not have {v_past1} the {noun2}.",
    "Every {noun1} {prep1} the {adj1} {noun2} seemed to {v_base1} {adv1}.",
    "What had {name1} {v_past1} {prep1} the {adj1} {noun1}?",
    "As {name1} {v_past1} the {noun1}, the {adj1} {noun2} {v_past2} {prep1} the {noun3}.",
    "The {adj1} {noun1} {v_past1}, leaving the {nouns1} to {v_base1} {adv1}.",
    "Far {prep1} the {noun1}, {name1} {v_past1} a {adj1} {noun2} {v_ing1} in the {noun3}.",
    "{name1} never {v_past1} why the {adj1} {noun1} {v_past2} so {adv1}.",
    "Until the {noun1} {v_past1}, the {adj1} {nouns1} had been {v_ing1} {prep1} the {noun2}.",
    "So {adj1} was the {noun1} that {name1} {v_past1} {adv1}.",
    "The {noun1} {v_past1} the {adj1} {noun2}, and soon the {nouns1} {v_past2} as well.",
    "{time1}, a {adj1} {noun1} {v_past1} {prep1} the {noun2} and {v_past2} everything.",
    "Would the {adj1} {noun1} ever {v_base1} again, or had it {v_past1} for the last time?",
    # ── expanded ──
    "{name1} {v_past1} the {noun1}, and then the {adj1} {noun2} began to {v_base1}.",
    "The {adj1} {noun1} could barely {v_base1} as the {noun2} {v_past1} {prep1} the {noun3}.",
    "Once inside the {noun1}, {name1} {v_past1} the {adj1} {noun2} {adv1}.",
    "Although the {nouns1} {v_past1}, {name1} still {v_past2} the {adj1} {noun1}.",
    "Somewhere near the {noun1}, a {adj1} {noun2} {v_past1} in the {noun3}.",
    "The {adj1} {noun1} seemed to {v_base1} whenever the {noun2} {v_past1}.",
    "Long before the {noun1} {v_past1}, the {adj1} {nouns1} had begun to {v_base1}.",
    "{name1} could see that the {adj1} {noun1} had {v_past1} the {noun2}.",
    "The {noun1} was {adj1}, yet the {nouns1} {v_past1} {prep1} it {adv1}.",
    "Had {name1} not {v_past1}, the {adj1} {noun1} would have {v_past2}.",
    "It was the {adj1} {noun1} that {v_past1} {name1} the most.",
    "Where the {noun1} once {v_past1}, the {adj1} {noun2} now {v_past2}.",
    "The {nouns1} {v_past1} {adv1}; the {noun1} barely {v_past2} at all.",
    "{name1} wondered whether the {adj1} {noun1} would ever {v_base1} the {noun2}.",
    "Below the {adj1} {noun1}, a {noun2} {v_past1} {prep1} the {noun3}.",
    "Not a single {noun1} {v_past1} when the {adj1} {noun2} {v_past2}.",
    "She often {v_past1} {prep1} the {noun1}, {v_ing1} the {adj1} {nouns1}.",
    "He realized the {adj1} {noun1} was {adv1} more {adj2} than the {noun2}.",
    "After {v_ing1} the {noun1}, {name1} {adv1} {v_past1} toward the {adj1} {noun2}.",
    "{time1}, the {adj1} {noun1} and the {noun2} {v_past1} without a {noun3}.",
    "Perhaps the {adj1} {noun1} had always {v_past1}; perhaps the {noun2} never {v_past2}.",
    "Even {name1} could not {v_base1} the {adj1} {noun1} that {v_past1} {prep1} the {noun2}.",
    "The more the {noun1} {v_past1}, the more {adj1} the {noun2} became.",
    "Between the {noun1} and the {noun2}, a {adj1} {noun3} {v_past1} {adv1}.",
    "{name1} left the {adj1} {noun1} and {v_past1} {prep1} the {noun2}.",
    "For as long as the {noun1} {v_past1}, the {adj1} {nouns1} would {v_base1}.",
    "It was clear that the {noun1} had {adv1} {v_past1} the {adj1} {noun2}.",
    "The {adj1} {noun1} above the {noun2} {v_past1}, {v_ing1} everything below.",
    "{name1} {v_past1} the {noun1} so {adv1} that the {adj1} {noun2} {v_past2}.",
    "All the {nouns1} that {v_past1} were {adj1}, but the {noun1} was not.",
    "What if the {adj1} {noun1} had never {v_past1} the {noun2}?",
    "They {v_past1} the {adj1} {noun1} while the {noun2} {v_past2} {prep1} them.",
    "Until {name1} {v_past1}, no one knew the {noun1} was {adj1}.",
    "As the {adj1} {noun1} {v_past1}, the {nouns1} grew {adj2} and {adj3}.",
    "She wanted to {v_base1} the {noun1}, but the {adj1} {noun2} {v_past1}.",
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
    "Could the {adj1} {noun1}, which had {v_past1} so {adv1} {prep1} the {noun2}, truly {v_base1} what {name1} had {v_past2}?",
    "The {noun1} that {name1} {v_past1} {time1} had since {v_past2}; the {adj1} {noun2} {prep1} the {noun3} was all that {v_past3}.",
    "What {name1} could not {v_base1} was why the {adj1} {noun1}, having {v_past1} the {noun2} {adv1}, would then {v_base2} the {adj2} {noun3}.",
    "In every {noun1} there {v_past1} a {adj1} {noun2}; in every {noun3} there {v_past2} a {adj2} {noun4} waiting to {v_base1}.",
    "The {adj1} {nouns1}, {v_ing1} {adv1} {prep1} the {noun1}, had not {v_past1} that the {adj2} {noun2} would {v_base1} so {adv2}.",
    "How the {adj1} {noun1} had {v_past1} remained unclear; what was certain, however, was that {name1} {v_past2} the {adj2} {noun2} {adv1}.",
    "{name1} {v_past1} {prep1} the {adj1} {noun1}, yet the {noun2}, {adj2} and {adj3}, {v_past2} {adv1} beyond the {noun3}.",
    "Once the {adj1} {noun1} {v_past1}, every {noun2} {prep1} the {noun3} {v_past2}; it was as though the {adj2} {noun4} had never {v_past3}.",
    "Far from {v_ing1} the {adj1} {noun1}, {name1} had {adv1} {v_past1} it; the {noun2}, {adj2} as it was, {v_past2} {prep1} the {noun3}.",
    "The {adj1} {noun1} {v_past1} not because the {nouns1} {v_past2}, but because {name1}, who had {v_past3} the {adj2} {noun2}, could no longer {v_base1}.",
    "If the {adj1} {noun1} had {v_past1} {adv1} {prep1} the {noun2}, then the {noun3} would have {v_past2}; instead, it {v_past3} the {adj2} {noun4}.",
    "Never before had the {adj1} {noun1} {v_past1} so {adv1}, and {name1}, {v_ing1} {prep1} the {adj2} {noun2}, {v_past2} that this was no {adj3} {noun3}.",
    "To {v_base1} the {adj1} {noun1} was one thing; to {v_base2} the {adj2} {noun2} that {v_past1} {prep1} it was something {adv1} different.",
    "The {noun1}, {adj1} though it was, had {v_past1} the {adj2} {noun2}; {name1} {v_past2} that nothing {prep1} the {noun3} would ever {v_base1} again.",
    "Such was the {adj1} {noun1} that {v_past1} {prep1} the {noun2} that even {name1}, who had {adv1} {v_past2}, could not {v_base1} its {adj2} {noun3}.",
    "While the {adj1} {noun1} {v_past1} and the {nouns1} {v_past2} {adv1}, {name1} {v_past3} the {adj2} {noun2}, {v_ing1} that the {noun3} would soon {v_base1}.",
    # ── expanded ──
    "The {adj1} {noun1} that had {v_past1} {prep1} the {noun2} was now {adv1} {v_ing1}; {name1} {v_past2} that the {adj2} {noun3} could no longer {v_base1}.",
    "{name1}, having {adv1} {v_past1} the {adj1} {noun1}, {v_past2} {prep1} the {noun2} and {v_past3} the {adj2} {noun3} that {v_past4} {prep2} the {noun4}.",
    "It was not until the {adj1} {noun1} {v_past1} that {name1} {v_past2} how {adv1} the {noun2} had {v_past3} the {adj2} {noun3}.",
    "The {nouns1}, {adv1} {v_ing1} {prep1} the {adj1} {noun1}, could neither {v_base1} the {noun2} nor {v_base2} the {adj2} {noun3} that {v_past1} {prep2} the {noun4}.",
    "Between the {adj1} {noun1} and the {adj2} {noun2}, {name1} {v_past1} a {noun3} so {adj3} that even the {nouns1} {v_past2} {adv1}.",
    "Had the {adj1} {noun1} not {v_past1} so {adv1}, the {noun2} might never have {v_past2}; instead, the {adj2} {noun3} {v_past3} {prep1} the {noun4}.",
    "What {name1} {v_past1} {prep1} the {adj1} {noun1} was neither {adj2} nor {adj3}; it was the {noun2} itself, {v_ing1} {adv1} {prep2} the {noun3}.",
    "The {noun1}, {adj1} and {adj2}, {v_past1} {adv1} while the {nouns1} {v_past2}; {name1}, meanwhile, {v_past3} the {adj3} {noun2} {prep1} the {noun3}.",
    "Though {name1} had {v_past1} the {adj1} {noun1} many times, never before had the {noun2} {v_past2} so {adv1}, as though the {adj2} {noun3} itself had {v_past3}.",
    "Across the {adj1} {noun1}, where the {nouns1} once {v_past1} {adv1}, there now {v_past2} a {adj2} {noun2}, {v_ing1} the {noun3} with {adj3} {noun4}.",
    "{name1} {v_past1} {adv1} that the {adj1} {noun1}, having {v_past2} the {noun2}, would never again {v_base1} the {adj2} {noun3} that {v_past3} {prep1} the {noun4}.",
    "Within the {adj1} {noun1} there {v_past1} a {noun2} of such {adj2} {noun3} that {name1}, who had {v_past2} many {nouns1}, {v_past3} in {adj3} {noun4}.",
    "The {adj1} {noun1} {v_past1} {prep1} the {noun2}, and the {adj2} {noun3} {v_past2}; yet neither {name1} nor the {nouns1} could {v_base1} what had {v_past3}.",
    "If the {adj1} {noun1} were to {v_base1} the {noun2}, then the {adj2} {nouns1} would {v_base2} {adv1}; this was what {name1} had {v_past1} all along.",
    "Not only had the {adj1} {noun1} {v_past1} the {noun2} {adv1}, but it had also {v_past2} every {adj2} {noun3} {prep1} the {noun4}.",
    "The {noun1} {v_past1} as though it had {v_past2} the {adj1} {noun2}; {name1}, {v_ing1} {prep1} the {noun3}, could barely {v_base1} the {adj2} {noun4}.",
    "Every {noun1} that {v_past1} {prep1} the {adj1} {noun2} seemed to {v_base1} {adv1}, as if the {adj2} {noun3} had {v_past2} them all.",
    "From the {adj1} {noun1} to the {adj2} {noun2}, the {nouns1} {v_past1} {adv1}, {v_ing1} each {noun3} they {v_past2} along the {noun4}.",
    "{name1} could not {v_base1} whether the {adj1} {noun1} had {v_past1} or {v_past2}; either way, the {adj2} {noun2} {v_past3} {adv1} {prep1} the {noun3}.",
    "So {adv1} did the {adj1} {noun1} {v_base1} that the {nouns1}, which had been {v_ing1} {prep1} the {noun2}, {v_past1} without a sound.",
    "Where once the {adj1} {noun1} had {v_past1} {adv1}, there was now only the {adj2} {noun2}, {v_ing1} {prep1} the {adj3} {noun3}.",
    "The {adj1} {noun1}, the {adj2} {noun2}, and the {adj3} {noun3} all {v_past1} {prep1} one another; {name1} could only {v_base1} and {v_base2}.",
    "Whoever had {v_past1} the {adj1} {noun1} must have {v_past2} that the {noun2} would {v_base1}; otherwise, the {adj2} {noun3} would never have {v_past3}.",
    "As the {adj1} {noun1} {v_past1} {prep1} the {noun2}, {name1} {v_past2}, {v_ing1} the {adj2} {nouns1} that {v_past3} {adv1} in the {noun3}.",
    "Long after the {adj1} {noun1} had {v_past1}, the {noun2} continued to {v_base1} {adv1}, as if the {adj2} {noun3} still {v_past2} {prep1} the {noun4}.",
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

    # shuffle templates and cycle through to avoid back-to-back repeats
    deck = list(templates)
    random.shuffle(deck)
    idx = 0

    while total_words < count:
        if idx >= len(deck):
            # reshuffle when exhausted
            random.shuffle(deck)
            idx = 0
        tmpl = deck[idx]
        idx += 1
        filler = _Filler(pools)
        sentence = tmpl.format_map(filler)
        sentences.append(sentence)
        total_words += len(sentence.split())

    return " ".join(sentences)
