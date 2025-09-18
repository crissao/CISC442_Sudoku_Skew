# cisc442_sudoku.py
import sys
import cv2 as cv
import numpy as np

def subdivide_cells(warped, grid_size=9):
    """Yield each cell as an image."""
    h, w = warped.shape[:2]
    cell_h, cell_w = h // grid_size, w // grid_size # 450 // 9 = 50
    for r in range(grid_size):
        for c in range(grid_size):
            cell = warped[r*cell_h:(r+1)*cell_h, c*cell_w:(c+1)*cell_w]
            yield r, c, cell

def cell_has_digit(cell):
    """Decide if a cell contains a digit or is empty."""

    # Convert to grayscale if not already
    if len(cell.shape) == 3:
        cell = cv.cvtColor(cell, cv.COLOR_BGR2GRAY)

    # Crop to center (optional, to avoid borders)
    h, w = cell.shape[:2]
    scale = 0.8
    new_w = int(w * scale)
    new_h = int(h * scale)
    x1, y1 = (w - new_w)//2, (h - new_h)//2
    x2, y2 = x1 + new_w, y1 + new_h
    cell = cell[y1:y2, x1:x2]

    # Adaptive threshold → binary (0/255)
    blockSize = 7
    C = 8
    binary = cv.adaptiveThreshold(
        cell, 255,
        cv.ADAPTIVE_THRESH_MEAN_C,
        cv.THRESH_BINARY_INV,
        blockSize, C
    )

    # Morphology to clean noise
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2,2))
    cleaned = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)

    # Density check
    ratio = np.sum(cleaned > 0) / cleaned.size
    return 1 if ratio > 0.1 else 0

def draw_output_on_original(canny, occupancy, Minv, size=450, grid_size=9):
    """Draw grid and occupancy markers back on the original color image."""
    out = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)
    cell_h, cell_w = size // grid_size, size // grid_size

    for r in range(grid_size + 1):  # include 0..9
        thickness = 3 if r % 3 == 0 else 2
        y = int(r * cell_h)
        p1 = np.array([[[0, y]]], dtype="float32")
        p2 = np.array([[[size, y]]], dtype="float32")
        pts = np.vstack([p1, p2])
        line_pts = cv.perspectiveTransform(pts, Minv)
        cv.line(out, tuple(line_pts[0, 0].astype(int)),
                    tuple(line_pts[1, 0].astype(int)),
                    (0, 0, 255) if r % 3 == 0 else (255, 255, 0),
                    thickness)

    for c in range(grid_size + 1):  # include 0..9
        thickness = 3 if c % 3 == 0 else 2
        x = int(c * cell_w)
        p1 = np.array([[[x, 0]]], dtype="float32")
        p2 = np.array([[[x, size]]], dtype="float32")
        pts = np.vstack([p1, p2])
        line_pts = cv.perspectiveTransform(pts, Minv)
        cv.line(out, tuple(line_pts[0, 0].astype(int)),
                    tuple(line_pts[1, 0].astype(int)),
                    (0, 0, 255) if c % 3 == 0 else (255, 255, 0),
                    thickness)

    for r in range(grid_size):
        for c in range(grid_size):
            # occupancy markers
            if occupancy[r][c] == 1:
                cx = int((c + 0.5) * cell_w)
                cy = int((r + 0.5) * cell_h)
                pt = np.array([[[cx, cy]]], dtype="float32")  # (1,1,2)
                mapped = cv.perspectiveTransform(pt, Minv)
                mx, my = mapped[0, 0].astype(int)
                cv.circle(out, (mx, my), 8, (0, 255, 0), -1)
    return out



def main():
    if len(sys.argv) != 9 + 1:
        print("Usage: python cisc442_sudoku.py <input_filename>.png x_UL y_UL x_UR y_UR x_LL y_LL x_LR y_LR")
        return

    filename = sys.argv[1]
    pts = [(float(sys.argv[i]), float(sys.argv[i+1])) for i in range(2, 10, 2)]

    img = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    sharp = cv.GaussianBlur(img, (5,5), 0)
    canny = cv.Canny(sharp, 50, 75, None, 3)
    src = np.array(pts, dtype="float32")
    size = 450
    dst = np.array([[0, 0], [size-1, 0], [0, size-1], [size-1, size-1]], dtype="float32")
    M = cv.getPerspectiveTransform(src, dst)
    Minv = cv.getPerspectiveTransform(dst, src)
    warped = cv.warpPerspective(canny, M, (size, size))

    occupancy = np.zeros((9, 9), dtype=int)
    for r, c, cell in subdivide_cells(warped):
        occupancy[r][c] = cell_has_digit(cell)

    # Print 9x9 array
    for r in range(9):
        print("".join(str(x) for x in occupancy[r]))

    # Save visualization
    out = draw_output_on_original(canny, occupancy, Minv, size=size)
    out_filename = filename.replace(".png", "_sudoku.png")
    cv.imwrite(out_filename, out)
    return 0

if __name__ == "__main__":
    main()
