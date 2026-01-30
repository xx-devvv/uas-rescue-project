import cv2
import numpy as np
import os
from classification import classify_shape
from analysis import build_object_data, print_object_summary
from camp_logic import separate_camps_and_casualties
from priority_logic import compute_priority
from distance_logic import compute_distances
from assignment_logic import assign_casualties_to_camps
from reporting_logic import generate_image_report

# -----------------------------
# STEP 1 — LOOP THROUGH FOLDER
# -----------------------------
folder_path = "task_images"

all_detected_objects = []
image_reports = []  # store per-image reports for ranking

for file in os.listdir(folder_path):

    if file.endswith(".png") or file.endswith(".jpg"):
        print(f"\nProcessing: {file}")

        # -----------------------------
        # LOAD IMAGE
        # -----------------------------
        img = cv2.imread(os.path.join(folder_path, file))

        # -----------------------------
        # CONVERT TO HSV
        # -----------------------------
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # -----------------------------
        # LAND MASK
        # -----------------------------
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        land_mask = cv2.inRange(hsv, lower_green, upper_green)

        # -----------------------------
        # OCEAN MASK
        # -----------------------------
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([140, 255, 255])
        ocean_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # -----------------------------
        # CLEAN MASKS
        # -----------------------------
        kernel = np.ones((5,5), np.uint8)
        land_mask = cv2.morphologyEx(land_mask, cv2.MORPH_CLOSE, kernel)
        ocean_mask = cv2.morphologyEx(ocean_mask, cv2.MORPH_CLOSE, kernel)

        # -----------------------------
        # SEGMENTED OUTPUT
        # -----------------------------
        output = img.copy()
        output[land_mask == 255] = [0, 255, 0]
        output[ocean_mask == 255] = [255, 0, 0]

        # -----------------------------
        # SHAPE DETECTION
        # -----------------------------
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        edges = cv2.Canny(blur, 50, 150)
        edges = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=1)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour_img = img.copy()

        for cnt in contours:
            area = cv2.contourArea(cnt)

            if 2 < area < 8000:
                shape_name = classify_shape(cnt)

                cv2.drawContours(contour_img, [cnt], -1, (0, 0, 255), 2)

                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    cv2.putText(contour_img, shape_name, (cx - 20, cy),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # -----------------------------
        # BUILD OBJECT DATA
        # -----------------------------
        detected_objects = build_object_data(
            contours, land_mask, ocean_mask, classify_shape, img
        )

        print_object_summary(detected_objects)
        all_detected_objects.extend(detected_objects)

        # -----------------------------
        # CAMP & CASUALTY PROCESSING
        # -----------------------------
        camps, casualties = separate_camps_and_casualties(detected_objects, img)
        casualties = compute_priority(casualties)
        casualties = compute_distances(casualties, camps)
        camps = assign_casualties_to_camps(casualties, camps)

        # -----------------------------
        # RESCUE RATIO
        # -----------------------------
        total_priority_rescued = sum(camp["total_priority"] for camp in camps)
        total_casualties = len(casualties)

        rescue_ratio = round(
            total_priority_rescued / total_casualties, 2
        ) if total_casualties > 0 else 0

        print("\nRescue Ratio:", rescue_ratio)

        # -----------------------------
        # CAMP ASSIGNMENT PRINT
        # -----------------------------
        print("\nCamp Assignments:")
        for camp in camps:
            print(f"\nCamp Type: {camp['type']}")
            print(f"Capacity Used: {len(camp['assigned'])}/{camp['capacity']}")
            print(f"Total Priority: {camp['total_priority']}")
            print("Assigned Casualties:")

            for c in camp["assigned"]:
                print({
                    "shape": c["shape"],
                    "center": c["center"],
                    "emergency": c["emergency"],
                    "priority_score": c["priority_score"]
                })

        # -----------------------------
        # IMAGE REPORT
        # -----------------------------
        report = generate_image_report(camps, casualties)

        print("\nImage Report:")
        print(report)

        image_reports.append({
            "image": file,
            "rescue_ratio": report["rescue_ratio"],
            "priority": report["total_priority_rescued"]
        })

        # -----------------------------
        # FINAL CASUALTY DATA
        # -----------------------------
        print("\nFinal Casuality Data:")
        for c in casualties:
            print(c)

        # -----------------------------
        # SHOW RESULTS
        # -----------------------------
        cv2.imshow("Segmented Output", output)
        cv2.imshow("Detected Shapes", contour_img)
        cv2.waitKey(0)

# -----------------------------
# IMAGE RANKINGS
# -----------------------------
print("\n========== IMAGE RANKINGS ==========")

sorted_reports = sorted(
    image_reports,
    key=lambda x: x["rescue_ratio"],
    reverse=True
)

for rank, report in enumerate(sorted_reports, start=1):
    print(f"{rank}. {report['image']} → Rescue Ratio: {report['rescue_ratio']} | Priority: {report['priority']}")

# -----------------------------
# FINAL SUMMARY
# -----------------------------
print("\n========== OVERALL DATASET SUMMARY ==========")
print_object_summary(all_detected_objects)

cv2.destroyAllWindows()
