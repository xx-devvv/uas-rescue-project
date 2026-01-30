import cv2

# -----------------------------
# EMERGENCY COLOR DETECTION (HSV)
# -----------------------------
def detect_emergency_color(img, center):
    import cv2
    cx, cy = center
    h, w, _ = img.shape

    # safety check
    if not (0 <= cy < h and 0 <= cx < w):
        return "Unknown", 0

    # convert to HSV
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_val, s_val, v_val = hsv_img[cy, cx]

    # --- RED (Severe) ---
    if (0 <= h_val <= 10) or (160 <= h_val <= 180):
        return "Severe", 3

    # --- YELLOW (Mild) ---
    elif 20 <= h_val <= 35:
        return "Mild", 2

    # --- GREEN (Safe) ---
    elif 35 < h_val <= 85:
        return "Safe", 1

    return "Unknown", 0


def build_object_data(contours, land_mask, ocean_mask, classify_shape, img):
    detected_objects = []

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # ignore very small noise
        if area < 5:
            continue

        shape = classify_shape(cnt)

        # center of contour
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0
        # -----------------------------
        # EMERGENCY DETECTION (Only for casualties)
        # -----------------------------
        if shape != "Circle":
            emergency_label, emergency_score = detect_emergency_color(img, (cx, cy))
        else:
            emergency_label = None
            emergency_score = None

        # safe boundary check
        h, w = land_mask.shape
        if 0 <= cy < h and 0 <= cx < w:
            if land_mask[cy, cx] == 255:
                region = "Land"
            else:
                region = "Ocean"
        else:
            region = "Unknown"

        detected_objects.append({
            "shape": shape,
            "center": (cx, cy),
            "area": area,
            "region": region,
            "emergency": emergency_label,
            "emergency_score": emergency_score
        })

    return detected_objects


def print_object_summary(detected_objects):
    print(f"\nTotal Objects Detected: {len(detected_objects)}")



