import re

def detect_distortion(text):
    text = text.lower()

    # Enhanced distortion patterns with more sophisticated matching
    distortions = {
        "catastrophizing": [
            "ruined", "disaster", "worst", "everything is over", "completely ruined",
            "terrible", "horrible", "awful", "end of the world", "catastrophe",
            "doomed", "hopeless", "no way out", "will never recover",
            "life is ruined", "can't survive", "going to be terrible"
        ],
        "overgeneralization": [
            "always", "never", "every time", "nothing ever works",
            "everyone", "nobody", "no one", "everything", "nothing",
            "all the time", "constantly", "forever", "every single",
            "without fail", "inevitably"
        ],
        "mind_reading": [
            "everyone thinks", "they think", "people believe", "they must think",
            "i know they", "they probably think", "i'm sure they",
            "they'll think", "everyone will say", "people will judge",
            "they're judging", "i bet they think"
        ],
        "all_or_nothing": [
            "perfect", "failure", "either", "completely", "totally",
            "absolute", "utter", "total failure", "complete success",
            "all or nothing", "black and white", "no middle ground"
        ],
        "personalization": [
            "it's all my fault", "i'm to blame", "my fault",
            "i caused this", "because of me", "i ruined",
            "i'm responsible for", "i should have prevented"
        ],
        "should_statements": [
            "i should", "i must", "i have to", "i need to",
            "i ought to", "supposed to", "should have", "must have"
        ],
        "labeling": [
            "i'm a loser", "i'm stupid", "i'm worthless", "i'm a failure",
            "i'm useless", "i'm pathetic", "i'm incompetent",
            "i'm an idiot", "i'm such a"
        ],
        "emotional_reasoning": [
            "i feel like", "it feels like", "i feel that",
            "because i feel", "my feelings tell me"
        ]
    }

    # Priority order for detection (some patterns overlap)
    priority_order = [
        "labeling", "personalization", "catastrophizing",
        "mind_reading", "should_statements", "all_or_nothing",
        "overgeneralization", "emotional_reasoning"
    ]

    # Check in priority order
    for distortion in priority_order:
        keywords = distortions[distortion]
        for keyword in keywords:
            if keyword in text:
                return distortion

    return None