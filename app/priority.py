
def classify_priority(category: str, description: str) -> str:
    """
    Assign a priority based on the issue category and description.
    """

    text = f"{category} {description}".lower()

    critical_keywords = [
        "fire",
        "gas leak",
        "electrocution",
        "building collapse",
        "exposed live wire",
    ]

    high_keywords = [
        "water leakage",
        "broken window",
        "sewage overflow",
        "power outage",
        "major crack",
        "unsafe",
    ]

    medium_keywords = [
        "leaking tap",
        "broken chair",
        "projector not working",
        "fan not working",
        "damaged desk",
    ]

    if any(keyword in text for keyword in critical_keywords):
        return "Critical"

    if any(keyword in text for keyword in high_keywords):
        return "High"

    if any(keyword in text for keyword in medium_keywords):
        return "Medium"

    return "Low"
