import math


def compute_distances(casualties, camps):
    for casualty in casualties:
        cx, cy = casualty["center"]
        casualty["distances"] = {}

        for camp in camps:
            camp_x, camp_y = camp["center"]

            distance = math.sqrt(
                (camp_x - cx) ** 2 +
                (camp_y - cy) ** 2
            )

            casualty["distances"][camp["type"]] = round(distance, 2)

    return casualties
