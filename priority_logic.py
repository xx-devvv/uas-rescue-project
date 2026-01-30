# -----------------------------
# SHAPE PRIORITY VALUES
# -----------------------------
SHAPE_PRIORITY = {
    "Star": 3,
    "Triangle": 2,
    "Square": 1
}


# -----------------------------
# COMPUTE PRIORITY SCORE
# -----------------------------
def compute_priority(casualties):
    for obj in casualties:

        shape_value = SHAPE_PRIORITY.get(obj["shape"], 0)
        emergency_value = obj.get("emergency_score", 0)

        obj["priority_score"] = shape_value * emergency_value

    return casualties
