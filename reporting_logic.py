def generate_image_report(camps, casualties):
    total_casualties = len(casualties)
    total_rescued = sum(len(camp["assigned"]) for camp in camps)

    total_priority_rescued = sum(camp["total_priority"] for camp in camps)

    # rescue ratio formula
    rescue_ratio = round(
        total_priority_rescued / total_casualties, 2
    ) if total_casualties > 0 else 0

    return {
        "total_casualties": total_casualties,
        "total_rescued": total_rescued,
        "rescue_ratio": rescue_ratio,
        "total_priority_rescued": total_priority_rescued
    }
