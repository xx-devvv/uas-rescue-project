import cv2


# -----------------------------
# CAMP COLOR DETECTION (HSV)
# -----------------------------
def detect_camp_color(img, center):
    import cv2
    cx, cy = center
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h, s, v = hsv_img[cy, cx]

    # -----------------------------
    # BLUE CAMP
    # -----------------------------
    if 90 <= h <= 130:
        return "Blue", 4

    # -----------------------------
    # GREY CAMP
    # -----------------------------
    elif s < 30:
        return "Grey", 2

    # -----------------------------
    # EVERYTHING ELSE = PINK
    # -----------------------------
    else:
        return "Pink", 3



# -----------------------------
# SEPARATE CAMPS FROM CASUALTIES
# -----------------------------
def separate_camps_and_casualties(detected_objects, img):
    camps = []
    casualties = []

    for obj in detected_objects:
        if obj["shape"] == "Circle":
            camp_type, capacity = detect_camp_color(img, obj["center"])

            camp_data = {
                "type": camp_type,
                "center": obj["center"],
                "capacity": capacity,
                "assigned": [],
                "total_priority": 0
            }

            camps.append(camp_data)

        else:
            casualties.append(obj)

    return camps, casualties
