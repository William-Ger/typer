"""Categorized word banks for sentence generation."""

# ── nouns (singular) ─────────────────────────────────────────────────────────

NOUNS_EASY = [
    "cat", "dog", "bird", "fish", "tree", "road", "sun", "moon", "rain",
    "book", "door", "house", "wall", "room", "bed", "chair", "table", "lamp",
    "cup", "hat", "coat", "shoe", "bag", "box", "key", "bell", "boat", "car",
    "bus", "hill", "lake", "farm", "park", "shop", "town", "school", "road",
    "path", "gate", "yard", "roof", "fire", "wind", "snow", "sky", "star",
    "rock", "leaf", "hand", "face", "eye", "song", "game", "ball", "toy",
    "boy", "girl", "man", "child", "baby", "king", "cook", "nurse", "clerk",
    "fox", "bear", "deer", "wolf", "frog", "duck", "goat", "horse", "mouse",
    "ship", "train", "plane", "bridge", "clock", "phone", "light", "flag",
    "gift", "cake", "soup", "bread", "milk", "rose", "seed", "nest", "pond",
    "coin", "rope", "drum", "ring", "map", "pen", "page", "sign", "step",
    "meal", "dream", "smile", "voice", "story", "color", "night", "river",
    "stone", "cloud", "grass", "floor", "plate", "glass", "shirt", "dress",
]

NOUNS_MEDIUM = [
    "garden", "village", "harbor", "mountain", "library", "market", "temple",
    "castle", "forest", "island", "valley", "desert", "meadow", "canyon",
    "palace", "cottage", "chapel", "tavern", "museum", "prison", "tower",
    "fountain", "orchard", "vineyard", "glacier", "volcano", "plateau",
    "captain", "soldier", "merchant", "painter", "scholar", "servant",
    "stranger", "teacher", "farmer", "hunter", "sailor", "doctor",
    "traveler", "prisoner", "guardian", "builder", "driver", "author",
    "journal", "portrait", "lantern", "blanket", "curtain", "pillow",
    "candle", "mirror", "carpet", "ribbon", "basket", "anchor", "compass",
    "trumpet", "violin", "hammer", "shovel", "ladder", "barrel", "wagon",
    "feather", "pebble", "crystal", "shadow", "whisper", "silence",
    "thunder", "breeze", "rainbow", "sunset", "horizon", "twilight",
    "promise", "secret", "memory", "fortune", "mystery", "journey",
    "creature", "phantom", "spirit", "legend", "victory", "treasure",
    "harvest", "shelter", "passage", "kingdom", "empire", "chamber",
    "surface", "pattern", "signal", "method", "reason", "problem",
    "answer", "moment", "feeling", "opinion", "message", "purpose",
    "weather", "season", "morning", "evening", "century", "chapter",
]

NOUNS_HARD = [
    "labyrinth", "silhouette", "archipelago", "chandelier", "protagonist",
    "manuscript", "phenomenon", "hemisphere", "catastrophe", "bureaucracy",
    "surveillance", "renaissance", "melancholy", "philosophy", "controversy",
    "temperament", "consequence", "predicament", "architecture", "atmosphere",
    "equilibrium", "paradox", "metaphor", "hypothesis", "rhetoric",
    "algorithm", "infrastructure", "sovereignty", "aristocracy", "expedition",
    "observatory", "constellation", "jurisdiction", "predecessor", "beneficiary",
    "connoisseur", "entrepreneur", "acquaintance", "correspondent",
    "accomplishment", "circumstance", "reconnaissance", "discrepancy",
    "idiosyncrasy", "kaleidoscope", "paraphernalia", "quintessence",
]

# ── nouns (plural) ───────────────────────────────────────────────────────────

NOUNS_PL_EASY = [
    "cats", "dogs", "birds", "trees", "roads", "books", "doors", "walls",
    "rooms", "cups", "hats", "shoes", "bags", "keys", "bells", "boats",
    "cars", "hills", "lakes", "farms", "shops", "towns", "paths", "gates",
    "stars", "rocks", "songs", "games", "toys", "ships", "trains", "clocks",
    "gifts", "cakes", "roses", "seeds", "coins", "drums", "rings", "maps",
    "pages", "signs", "steps", "meals", "dreams", "voices", "stories",
    "clouds", "stones", "plates", "floors", "children", "horses", "foxes",
    "wolves", "mice", "leaves", "nights", "rivers", "colors", "smiles",
]

NOUNS_PL_MEDIUM = [
    "gardens", "villages", "mountains", "libraries", "markets", "temples",
    "castles", "forests", "islands", "valleys", "deserts", "meadows",
    "palaces", "towers", "fountains", "orchards", "glaciers", "soldiers",
    "merchants", "scholars", "strangers", "travelers", "guardians",
    "journals", "portraits", "lanterns", "curtains", "candles", "mirrors",
    "feathers", "crystals", "shadows", "whispers", "promises", "secrets",
    "memories", "mysteries", "journeys", "creatures", "legends", "treasures",
    "kingdoms", "chambers", "surfaces", "patterns", "signals", "reasons",
    "problems", "answers", "moments", "feelings", "opinions", "messages",
    "seasons", "mornings", "evenings", "centuries", "chapters", "victories",
]

NOUNS_PL_HARD = [
    "labyrinths", "silhouettes", "manuscripts", "catastrophes", "phenomena",
    "hemispheres", "consequences", "predicaments", "atmospheres", "paradoxes",
    "metaphors", "hypotheses", "algorithms", "expeditions", "constellations",
    "accomplishments", "circumstances", "discrepancies", "kaleidoscopes",
]

# ── proper names ─────────────────────────────────────────────────────────────

NAMES = [
    "Alice", "James", "Clara", "Henry", "Elena", "Thomas", "Sarah", "Oliver",
    "Grace", "William", "Emma", "Daniel", "Sophie", "Marcus", "Violet",
    "Arthur", "Helen", "George", "Anna", "Edward", "Maria", "Charles",
    "Rose", "Peter", "Julia", "Samuel", "Lucy", "David", "Margaret",
    "Robert", "Eleanor", "Frank", "Ruth", "Leon", "Ada", "Felix",
    "Iris", "Hugo", "Vera", "Max", "Nora", "Paul", "Lily", "Oscar",
    "June", "Miles", "Ella", "Simon", "Jane", "Victor", "Eve", "Martin",
    "Hazel", "Albert", "Ivy", "Louis", "Alma", "Walter", "Flora", "Leo",
]

# ── verbs (past tense) ──────────────────────────────────────────────────────

VERBS_PAST_EASY = [
    "saw", "ran", "sat", "ate", "had", "got", "put", "let", "cut", "hit",
    "set", "won", "led", "met", "held", "told", "read", "kept", "gave",
    "took", "came", "made", "went", "said", "knew", "felt", "left", "found",
    "lost", "heard", "paid", "sent", "fell", "drew", "grew", "hung", "laid",
    "rode", "rose", "sang", "sank", "shut", "slid", "sold", "wore", "woke",
    "liked", "loved", "hoped", "moved", "used", "lived", "played", "asked",
    "tried", "walked", "looked", "turned", "called", "needed", "worked",
    "pulled", "picked", "pushed", "dropped", "washed", "filled", "saved",
]

VERBS_PAST_MEDIUM = [
    "opened", "closed", "carried", "studied", "noticed", "watched",
    "reached", "crossed", "entered", "climbed", "planted", "painted",
    "gathered", "offered", "promised", "believed", "whispered", "wandered",
    "returned", "followed", "finished", "covered", "searched", "removed",
    "decided", "expected", "answered", "demanded", "explored", "imagined",
    "measured", "observed", "prepared", "repeated", "revealed", "selected",
    "shattered", "balanced", "captured", "defended", "escaped", "fastened",
    "honored", "inspired", "launched", "mastered", "polished", "recalled",
    "rescued", "scattered", "trembled", "troubled", "vanished", "welcomed",
    "arranged", "borrowed", "composed", "discovered", "embraced", "examined",
    "traveled", "delivered", "abandoned", "collected", "destroyed", "survived",
]

VERBS_PAST_HARD = [
    "acknowledged", "accompanied", "administered", "anticipated", "approximated",
    "articulated", "characterized", "commemorated", "comprehended", "concentrated",
    "consolidated", "contemplated", "contributed", "deliberated", "deteriorated",
    "distinguished", "endeavored", "exaggerated", "extinguished", "facilitated",
    "illuminated", "inaugurated", "manipulated", "necessitated", "orchestrated",
    "overwhelmed", "persevered", "proliferated", "rationalized", "reverberated",
    "scrutinized", "surrendered", "sympathized", "transcended", "underestimated",
]

# ── verbs (3rd person present) ───────────────────────────────────────────────

VERBS_PRES_EASY = [
    "sees", "runs", "sits", "eats", "gets", "puts", "lets", "cuts", "hits",
    "sets", "wins", "leads", "meets", "holds", "tells", "reads", "keeps",
    "gives", "takes", "comes", "makes", "goes", "says", "knows", "feels",
    "finds", "hears", "pays", "sends", "falls", "draws", "grows", "rides",
    "sings", "shuts", "sells", "wears", "likes", "loves", "hopes", "moves",
    "uses", "lives", "plays", "asks", "tries", "walks", "looks", "turns",
    "calls", "needs", "works", "pulls", "picks", "drops", "fills", "saves",
]

VERBS_PRES_MEDIUM = [
    "opens", "closes", "carries", "studies", "notices", "watches",
    "reaches", "crosses", "enters", "climbs", "gathers", "offers",
    "promises", "believes", "whispers", "wanders", "returns", "follows",
    "finishes", "covers", "searches", "removes", "decides", "expects",
    "answers", "demands", "explores", "imagines", "measures", "observes",
    "prepares", "repeats", "reveals", "selects", "captures", "defends",
    "escapes", "inspires", "launches", "polishes", "recalls", "rescues",
    "scatters", "trembles", "vanishes", "welcomes", "arranges", "composes",
    "discovers", "examines", "embraces", "delivers", "collects", "survives",
]

# ── verbs (base/infinitive) ─────────────────────────────────────────────────

VERBS_BASE_EASY = [
    "see", "run", "sit", "eat", "get", "put", "let", "cut", "hit", "set",
    "win", "lead", "meet", "hold", "tell", "read", "keep", "give", "take",
    "come", "make", "go", "say", "know", "feel", "find", "hear", "pay",
    "send", "fall", "draw", "grow", "ride", "sing", "shut", "sell", "wear",
    "like", "love", "hope", "move", "use", "live", "play", "ask", "try",
    "walk", "look", "turn", "call", "need", "work", "pull", "pick", "drop",
    "fill", "save", "rest", "wait", "help", "pass", "stay", "hide", "swim",
]

VERBS_BASE_MEDIUM = [
    "open", "close", "carry", "study", "notice", "watch", "reach", "cross",
    "enter", "climb", "gather", "offer", "promise", "believe", "whisper",
    "wander", "return", "follow", "finish", "cover", "search", "remove",
    "decide", "expect", "answer", "demand", "explore", "imagine", "measure",
    "observe", "prepare", "repeat", "reveal", "select", "capture", "defend",
    "escape", "inspire", "launch", "polish", "recall", "rescue", "scatter",
    "tremble", "vanish", "welcome", "arrange", "compose", "discover",
    "examine", "embrace", "deliver", "collect", "survive", "approach",
    "consider", "establish", "maintain", "remember", "understand", "continue",
]

# ── verbs (gerund / -ing) ───────────────────────────────────────────────────

VERBS_ING_EASY = [
    "running", "sitting", "eating", "getting", "cutting", "hitting",
    "winning", "reading", "keeping", "making", "going", "saying",
    "looking", "walking", "turning", "calling", "working", "playing",
    "trying", "living", "moving", "using", "hoping", "loving",
    "pulling", "picking", "dropping", "filling", "saving", "hiding",
    "waiting", "resting", "helping", "singing", "riding", "drawing",
]

VERBS_ING_MEDIUM = [
    "opening", "closing", "carrying", "studying", "watching", "climbing",
    "reaching", "crossing", "entering", "gathering", "offering", "believing",
    "whispering", "wandering", "returning", "following", "finishing",
    "covering", "searching", "removing", "deciding", "expecting",
    "answering", "demanding", "exploring", "imagining", "measuring",
    "observing", "preparing", "repeating", "revealing", "selecting",
    "capturing", "defending", "escaping", "inspiring", "polishing",
    "recalling", "rescuing", "trembling", "vanishing", "arranging",
    "composing", "discovering", "examining", "embracing", "delivering",
]

# ── adjectives ───────────────────────────────────────────────────────────────

ADJ_EASY = [
    "big", "small", "old", "new", "long", "short", "tall", "wide", "thin",
    "fast", "slow", "hot", "cold", "warm", "cool", "soft", "hard", "dark",
    "bright", "clean", "dry", "wet", "flat", "deep", "high", "low", "full",
    "empty", "rich", "poor", "kind", "fair", "safe", "wild", "calm", "bold",
    "glad", "sad", "lost", "free", "real", "true", "good", "bad", "nice",
    "fine", "red", "blue", "green", "white", "black", "gray", "brown",
    "pale", "round", "sharp", "plain", "fresh", "clear", "sweet", "young",
    "quiet", "loud", "strong", "weak", "quick", "rare", "late", "early",
]

ADJ_MEDIUM = [
    "gentle", "bitter", "golden", "silver", "hollow", "narrow", "frozen",
    "hidden", "broken", "silent", "ancient", "modern", "distant", "curious",
    "careful", "fearful", "grateful", "honest", "humble", "clever", "proper",
    "sudden", "formal", "simple", "steady", "subtle", "elegant", "fragile",
    "massive", "patient", "private", "sacred", "strange", "typical", "urgent",
    "useful", "violent", "visible", "willing", "worried", "familiar",
    "peaceful", "powerful", "pleasant", "splendid", "terrible", "fortunate",
    "important", "beautiful", "dangerous", "difficult", "delicate", "graceful",
    "brilliant", "charming", "dreadful", "faithful", "generous", "innocent",
    "restless", "tireless", "watchful", "colorful", "cheerful", "doubtful",
]

ADJ_HARD = [
    "meticulous", "exquisite", "formidable", "ubiquitous", "treacherous",
    "magnificent", "spontaneous", "inconspicuous", "unprecedented",
    "extraordinary", "incomprehensible", "sophisticated", "conscientious",
    "idiosyncratic", "quintessential", "unequivocal", "ostentatious",
    "surreptitious", "contemptible", "indefatigable", "imperceptible",
    "irreconcilable", "magnanimous", "perspicacious", "phantasmagorical",
]

# ── adverbs ──────────────────────────────────────────────────────────────────

ADV_EASY = [
    "very", "just", "well", "also", "here", "then", "soon", "still", "never",
    "always", "often", "once", "again", "away", "down", "up", "now", "fast",
    "hard", "far", "near", "back", "even", "only", "almost", "quite",
]

ADV_MEDIUM = [
    "quickly", "slowly", "gently", "quietly", "softly", "loudly", "calmly",
    "boldly", "gladly", "sadly", "deeply", "firmly", "purely", "rarely",
    "simply", "merely", "nearly", "barely", "hardly", "clearly", "closely",
    "finally", "greatly", "largely", "neatly", "partly", "safely", "surely",
    "wholly", "widely", "eagerly", "swiftly", "bravely", "proudly",
    "sharply", "brightly", "carefully", "silently", "suddenly", "properly",
    "steadily", "patiently", "honestly", "entirely", "politely", "precisely",
    "gracefully", "endlessly", "restlessly", "faithfully", "peacefully",
]

ADV_HARD = [
    "meticulously", "spontaneously", "simultaneously", "unquestionably",
    "conscientiously", "indiscriminately", "inconspicuously", "magnanimously",
    "surreptitiously", "extraordinarily", "incomprehensibly", "unequivocally",
    "disproportionately", "incontrovertibly", "characteristically",
]

# ── prepositions ─────────────────────────────────────────────────────────────

PREPOSITIONS = [
    "in", "on", "at", "by", "to", "for", "from", "with", "near", "past",
    "through", "across", "around", "along", "above", "below", "under",
    "beside", "behind", "beyond", "between", "toward", "against", "among",
    "beneath", "inside", "outside", "within", "without", "before", "after",
]

# ── time phrases ─────────────────────────────────────────────────────────────

TIME_PHRASES = [
    "that morning", "that evening", "that night", "that afternoon",
    "last summer", "last winter", "last spring", "every morning",
    "every evening", "every winter", "for many years", "for a long time",
    "at dawn", "at dusk", "at midnight", "at noon", "on that day",
    "in those days", "long ago", "years later", "the next morning",
    "the following day", "one quiet evening", "on a cold night",
    "during the storm", "before sunrise", "after sunset", "by then",
    "at that moment", "without warning", "all at once", "once again",
]

# ── pool builder ─────────────────────────────────────────────────────────────

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
        "name": NAMES,
        "v_past": _pool(VERBS_PAST_EASY, VERBS_PAST_MEDIUM, VERBS_PAST_HARD, difficulty),
        "v_pres": _pool(VERBS_PRES_EASY, VERBS_PRES_MEDIUM, difficulty=difficulty),
        "v_base": _pool(VERBS_BASE_EASY, VERBS_BASE_MEDIUM, difficulty=difficulty),
        "v_ing": _pool(VERBS_ING_EASY, VERBS_ING_MEDIUM, difficulty=difficulty),
        "adj": _pool(ADJ_EASY, ADJ_MEDIUM, ADJ_HARD, difficulty),
        "adv": _pool(ADV_EASY, ADV_MEDIUM, ADV_HARD, difficulty),
        "prep": PREPOSITIONS,
        "time": TIME_PHRASES,
    }
