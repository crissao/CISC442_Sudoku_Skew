# cisc442_skew.py
import sys
import math
import cv2 as cv
import numpy as np
def main(argv):
    
    default_file = 'rotation/bricks.png'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1
    
    dst = cv.Canny(src, 50, 200, None, 3)
    
    # Copy edges to the images that will display the results in BGR
    cdstP = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    src_with_skew = cv.cvtColor(src, cv.COLOR_GRAY2BGR)
    
    
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 150, 12)
    
    if linesP is None:
        print("No lines were found")
        return -1
    
    angles = []
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)
        angle = -math.degrees(math.atan2(l[3]-l[1], l[2]-l[0]))
        angles.append(angle)
    # Compute the median angle for skew correction
    median_angle = np.median(angles)
    print("Median angle: ", median_angle)
    # Correct the angle to be within [-45, 45] degrees
    if median_angle < -90:
        corrected_angle = median_angle + 180
    elif median_angle > 90:
        corrected_angle = median_angle - 180
    else:
        corrected_angle = median_angle
    print("Corrected Angle: ", corrected_angle)
    (h, w) = src.shape[:2]
    center = (w // 2, h // 2)
    # Calculate endpoint from center to edge at skew angle (starting from top)
    length = max(h, w)
    angle_rad = math.radians(corrected_angle)
    # Start from center, go in direction of angle from vertical (top)
    end_x = int(center[0] + length * math.sin(-angle_rad))
    end_y = int(center[1] - length * math.cos(-angle_rad))
    cv.line(src_with_skew, center, (end_x, end_y), (255, 0, 255), 2)
    out_filename = filename.replace(".png", "_sudoku.png")
    cv.imwrite(out_filename, src_with_skew)
    return 0
    
if __name__ == "__main__":
    main(sys.argv[1:])