# =========================================================
# SATQUERY-AI
# QUERY UNDERSTANDING MODULE
# English + Hinglish
# =========================================================


def understand_query(query):

    q = query.lower().strip()

    # -----------------------------------------------------
    # VEGETATION
    # -----------------------------------------------------

    vegetation_words = [
        "vegetation",
        "greenery",
        "green area",
        "forest",
        "forests",
        "tree",
        "trees",
        "plant",
        "plants",
        "crop",
        "crops",
        "ndvi",

        # Hinglish / Hindi
        "ped",
        "pedh",
        "ped paudhe",
        "paudha",
        "paudhe",
        "hariyali",
        "kheti",
        "jungle",
        "jangal"
    ]

    # -----------------------------------------------------
    # WATER
    # -----------------------------------------------------

    water_words = [
        "water",
        "waterbody",
        "water body",
        "water area",
        "lake",
        "lakes",
        "river",
        "rivers",
        "pond",
        "ponds",
        "flood",

        # Hinglish / Hindi
        "paani",
        "pani",
        "jal",
        "jheel",
        "talab",
        "nadi"
    ]

    # -----------------------------------------------------
    # CONSTRUCTION
    # -----------------------------------------------------

    construction_words = [
        "construction",
        "building",
        "buildings",
        "built-up",
        "built up",
        "urban",
        "urbanization",
        "urbanisation",
        "development",
        "new building",
        "new buildings",

        # Hinglish / Hindi
        "ghar",
        "ghar bane",
        "ghar bana",
        "makan",
        "makan bane",
        "imarat",
        "imaarat",
        "building bani",
        "building bane",
        "buildings bane",
        "construction hua",
        "construction badha"
    ]

    # -----------------------------------------------------
    # DECREASE WORDS
    # -----------------------------------------------------

    decrease_words = [
        "decrease",
        "decreased",
        "decreasing",
        "loss",
        "lost",
        "reduced",
        "reduce",
        "removed",
        "removal",
        "decline",
        "less",

        # Hinglish / Hindi
        "kam",
        "kam hua",
        "kam hui",
        "kam ho gaya",
        "kam ho gayi",
        "ghata",
        "ghati",
        "ghat",
        "ghat gaya",
        "ghat gayi"
    ]

    # -----------------------------------------------------
    # VEGETATION QUERY
    # -----------------------------------------------------

    if any(
        word in q
        for word in vegetation_words
    ):

        if any(
            word in q
            for word in decrease_words
        ):
            return "vegetation_decrease"

        return "vegetation_increase"

    # -----------------------------------------------------
    # WATER QUERY
    # -----------------------------------------------------

    if any(
        word in q
        for word in water_words
    ):

        if any(
            word in q
            for word in decrease_words
        ):
            return "water_decrease"

        return "water_change"

    # -----------------------------------------------------
    # CONSTRUCTION QUERY
    # -----------------------------------------------------

    if any(
        word in q
        for word in construction_words
    ):

        return "construction_increase"

    # -----------------------------------------------------
    # GENERAL CHANGE
    # -----------------------------------------------------

    return "general_change"


# =========================================================
# DISPLAY NAME
# =========================================================

def get_intent_name(intent):

    names = {

        "vegetation_increase":
            "🌳 Vegetation Increase",

        "vegetation_decrease":
            "🍂 Vegetation Decrease",

        "water_change":
            "💧 Water-body Change",

        "water_decrease":
            "💧 Water-body Decrease",

        "construction_increase":
            "🏗️ New Built-up / Construction",

        "general_change":
            "🔄 General Temporal Change"
    }

    return names.get(
        intent,
        "🔄 General Temporal Change"
    )