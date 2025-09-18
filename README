# CISC442 Project – Skew Detection and Sudoku Digit Detection

## Overview

This project contains two scripts:

* **`cisc442_skew.py`** – detects and visualizes the skew of an image using Hough line detection.
* **`cisc442_sudoku.py`** – detects digits in a Sudoku puzzle image by preprocessing, warping, and subdividing into cells.

---

## Approaches

### Skew Detection (`cisc442_skew.py`)

Functions:

* `main()` – handles I/O, runs skew detection, and draws visualization.

Approach:

* Based on the **Hough Line Transform example from OpenCV’s documentation**.
* The script applies Canny edges before Hough transform, then computes the **median line angle** for stability.
* For visualization, a line is drawn starting at the image center (`cx, cy`) toward calculated end coordinates (`end_x, end_y`) to illustrate skew direction.

---

### Sudoku Digit Detection (`cisc442_sudoku.py`)

Functions:

* `subdivide_cells(warped)` – yields each of the 81 cells.
* `cell_has_digit(cell)` – checks if a cell contains a digit via thresholding, morphology, and density ratio.
* `draw_output_on_original(canny, occupancy, Minv, ...)` – overlays Sudoku grid lines and occupancy markers back onto the original image.
* `main()` – runs pipeline.

Approach:

* Inspired by **OpenCV examples** for perspective transforms, adaptive thresholding, and morphology.
* Workflow:

  1. **Perspective correction** with `cv.getPerspectiveTransform` and `cv.warpPerspective`.
  2. **Subdivision** into 9×9 cells.
  3. **Adaptive thresholding and morphology** to isolate digits and suppress noise.
  4. **Occupancy detection** using pixel density ratio.
  5. **Visualization** using the inverse transform (`Minv`) to place grid lines and digit markers back onto the original image.

---

## What Worked

* **`cisc442_skew.py` – main()**

  * Computing the **median angle** of detected Hough lines provided stable skew detection, avoiding outliers from noisy lines.
  * Drawing the skew line from the **center of the image** with calculated end coordinates (`end_x`, `end_y`) successfully visualized the skew.

* **`cisc442_sudoku.py` – cell_has_digit()**

  * Adaptive thresholding combined with **morphological opening** effectively removed grid artifacts and isolated digits.
  * Using a **pixel density ratio threshold** gave a reliable digit/no-digit classification.

* **`cisc442_sudoku.py` – draw_output_on_original()**

  * Using `cv.perspectiveTransform` on grid line endpoints allowed accurate overlays when mapping back to the original image.
  * The color/thickness scheme (red for 3×3 boxes, blue for single-cell divisions) clearly distinguished major and minor grid lines.

---

## What Didn’t Work / Required Adjustments

* **`cisc442_sudoku.py` – main()**

  * Initially, I attempted Sudoku occupancy detection without using Canny edge detection. While it produced partial results, they were inconsistent. After reviewing example outputs, I added the Canny step and saw much more accurate results.

* **`cisc442_sudoku.py` – cell_has_digit()**

  * Early thresholding parameters (`blockSize`, `C`) produced either too much noise or missed digits. I had to experiment to find a balanced setting.
  * Without cropping the center of each cell, the grid borders interfered with digit detection. Adding a crop-to-center step (80% of the cell) significantly improved accuracy.

* **`cisc442_sudoku.py` – draw_output_on_original()**

  * Drawing grid lines on the warped image directly didn’t map back correctly. Using transformed endpoints solved that.

---

## AI Usage

I used AI tools throughout the project, mainly for math help, debugging, and organizing code. All usage is cited below:

* **`cisc442_skew.py`**

  * GPT-5 clarified the **math for visualization**: how to compute the image center (`cx, cy`) and calculate `end_x` and `end_y` for the skew angle line.
  * GPT-5 also explained how to **normalize the median angle** to stay within `[-45, 45]` degrees.

* **`cisc442_sudoku.py`**

  * GPT-5 helped refine the **`cell_has_digit` function**:

    * Suggested cropping the center region before thresholding.
    * Recommended adaptive thresholding with tuned parameters and morphology to clean noise.
    * Proposed using a **pixel density ratio** for digit detection.
  * GPT-5 contributed to the structure of **`draw_output_on_original`**:
    * Recommended how to loop through grid lines.
    * Ensured line/circle coordinates were properly handled with `float32` before passing into `cv.perspectiveTransform`.
  * GPT-5 also helped debug **array type issues** when constructing `src`, `dst`, and point arrays.

* **General AI Support**

  * GitHub Copilot provided **auto-generated comments** and occasional autocomplete for repetitive OpenCV code.
  * GPT-5 helped polish and organize this README into a structured format with clearer language.

---

## Files

* `cisc442_skew.py` – skew detection via Hough Transform.
* `cisc442_sudoku.py` – Sudoku digit detection and visualization.
* `README.md` – this file.
