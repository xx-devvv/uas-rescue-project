import cv2
import numpy as np

def classify_shape(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.03 * peri, True)
    vertices = len(approx)

    area = cv2.contourArea(contour)
    if area == 0:
        return "Unknown"

    # Circularity check
    circularity = (4 * np.pi * area) / (peri * peri)

    # Bounding box ratio
    x, y, w, h = cv2.boundingRect(approx)
    aspect_ratio = float(w) / h

    # --- Shape Rules ---
    if vertices == 3:
        return "Triangle"

    elif vertices == 4:
        # AREA-based separation
        if area < 500:
            return "Triangle"
        else:
            return "Square"

    elif circularity > 0.75:
        return "Circle"

    elif vertices >= 5:
        return "Star"

    else:
        return "Unknown"
