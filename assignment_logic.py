def assign_casualties_to_camps(casualties, camps):
    # Sort casualties by priority (high → low)
    casualties_sorted = sorted(
        casualties,
        key=lambda x: x["priority_score"],
        reverse=True
    )

    for casualty in casualties_sorted:
        best_camp = None
        best_score = -1

        for camp in camps:
            if len(camp["assigned"]) >= camp["capacity"]:
                continue

            distance = casualty["distances"][camp["type"]]
            score = casualty["priority_score"] / (distance + 1)

            if score > best_score:
                best_score = score
                best_camp = camp

        if best_camp:
            best_camp["assigned"].append(casualty)
            best_camp["total_priority"] += casualty["priority_score"]

    return camps
