VISUAL_TOPIC_MAP = {

    "karnaugh": [

        "assets/diagrams/kmap1.png",

        "assets/diagrams/kmap2.png",

        "assets/diagrams/kmap3.png"
    ],

    "flip flop": [

        "assets/diagrams/Dflipflop.png",

        "assets/diagrams/JKflipflop.png",

        "assets/diagrams/SRflipflop.png"
    ],

    "fsm": [

        "assets/diagrams/fsm.png"
    ],

    "cmos": [

        "assets/diagrams/cmos.png"
    ],

    "setup hold": [

        "assets/diagrams/setupandholdtime.png"
    ],

    "shift register": [

        "assets/diagrams/shiftregister.png"
    ],

    "sram": [

        "assets/diagrams/sram.png"
    ]
}


def retrieve_visuals(query):

    if not query:

        return []

    query = query.lower()

    matched_visuals = []

    if "karnaugh" in query or "k-map" in query:

        matched_visuals.extend(
            VISUAL_TOPIC_MAP["karnaugh"]
        )

    if "flip flop" in query or "flip-flop" in query:

        matched_visuals.extend(
            VISUAL_TOPIC_MAP["flip flop"]
        )

    if "fsm" in query or "finite state machine" in query:

        matched_visuals.extend(
            VISUAL_TOPIC_MAP["fsm"]
        )

    if "cmos" in query:

        matched_visuals.extend(
            VISUAL_TOPIC_MAP["cmos"]
        )

    if "setup" in query or "hold" in query:

        matched_visuals.extend(
            VISUAL_TOPIC_MAP["setup hold"]
        )

    if "shift register" in query:

        matched_visuals.extend(
            VISUAL_TOPIC_MAP["shift register"]
        )

    if "sram" in query:

        matched_visuals.extend(
            VISUAL_TOPIC_MAP["sram"]
        )

    return matched_visuals