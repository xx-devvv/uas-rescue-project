# 🚁 UAS Rescue Assignment System
Image-Based Casualty Detection, Prioritization & Camp Assignment

------------------------------------------------------------

## 📌 Project Overview
This project implements an automated rescue decision system that analyzes aerial images to:

• Detect objects (casualties & rescue camps)  
• Classify geometric shapes  
• Identify land vs ocean regions  
• Determine emergency severity levels  
• Compute rescue priorities  
• Measure distances to rescue camps  
• Assign casualties based on priority & capacity  
• Generate rescue efficiency metrics  
• Rank images based on rescue performance  

The system simulates how an Unmanned Aerial System (UAS) can assist in rescue mission planning.

------------------------------------------------------------

## 🎯 Objectives
The main objectives of this project are:

1. Segment land and ocean areas from aerial images
2. Detect and classify shapes representing casualties and camps
3. Assign emergency levels based on color detection
4. Compute rescue priority scores
5. Allocate casualties to camps based on:
   • Distance
   • Camp capacity
   • Emergency severity
6. Calculate rescue efficiency metrics
7. Rank images by rescue effectiveness

------------------------------------------------------------

## 🧠 Methodology

### Step 1 — Image Segmentation
• Convert image to HSV color space  
• Apply color thresholds to detect:
  - Land (Green)
  - Ocean (Blue)
• Clean masks using morphological operations  

### Step 2 — Shape Detection
• Edge detection using Canny  
• Contour extraction  
• Shape classification into:
  - Circle (Camp)
  - Triangle
  - Square
  - Star

### Step 3 — Emergency Detection
Emergency level is determined by color:

• Red → Severe  
• Yellow → Mild  
• Green → Safe  

Circles are treated as camps and excluded from emergency scoring.

### Step 4 — Priority Calculation
Priority is calculated based on:
• Shape weight  
• Emergency severity  

### Step 5 — Distance Computation
Euclidean distance is calculated between casualties and camps.

### Step 6 — Camp Assignment
Casualties are assigned:
• Based on highest priority
• To the nearest available camp
• While respecting camp capacity

### Step 7 — Reporting
Metrics calculated:
• Total casualties
• Total rescued
• Rescue ratio
• Total priority rescued

------------------------------------------------------------

## 📊 Rescue Ratio Formula

Rescue Ratio =  
(Total Priority Rescued) ÷ (Total Number of Casualties)

------------------------------------------------------------

## 🗂 Project Structure

uas_rescue_project/
│
├── segmentation.py          → Main pipeline  
├── classification.py        → Shape classification  
├── analysis.py              → Object analysis  
├── camp_logic.py            → Camp detection logic  
├── priority_logic.py        → Priority scoring  
├── distance_logic.py        → Distance calculations  
├── assignment_logic.py      → Camp assignment  
├── reporting_logic.py       → Report generation  
├── task_images/             → Dataset  
└── README.md               → Documentation  

------------------------------------------------------------

## ⚙️ Technologies Used

• Python  
• OpenCV  
• NumPy  

------------------------------------------------------------

## 📈 Output
The system produces:

• Object detection summary  
• Camp assignments  
• Priority scores  
• Distance measurements  
• Rescue ratio  
• Image ranking by efficiency  

------------------------------------------------------------

## 🚀 How to Run

1. Install dependencies:
   pip install opencv-python numpy

2. Place dataset in the folder:
   task_images/

3. Run:
   python segmentation.py

------------------------------------------------------------

## 🏁 Final Results
Images are ranked based on rescue ratio to evaluate mission effectiveness.

------------------------------------------------------------

## 👨‍💻 Author
Dev Pandey, 
Project developed as part of the UAS Rescue Assignment Task.

------------------------------------------------------------



------------------------------------------------------------
