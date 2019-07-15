import motorAPI
import cv2 as cv
import numpy as np
import math

def canny_edge_detection(frame):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    low = np.array([84,30,184])
    high = np.array([104,50,224])
    mask = cv.inRange(hsv, low,high)
    edges = cv.Canny(mask, 200, 400)
    return edges

def roi(edges):
    height, width = edges.shape
    mask = np.zeros_like(edges)
    polygon = np.array([[(0, height * 1/2), (width, height * 1/2), (width, height), (0, height)]], np.int32)
    cv.fillPoly(mask, polygon, 255)
    cropped_edges = cv.bitwise_and(edges, mask)
    return cropped_edges

def hough_transform(cropped_edges):
    rho = 1  # distance precision in pixel, i.e. 1 pixel
    angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
    min_threshold = 10  # minimal of votes
    line_segments = cv.HoughLinesP(cropped_edges, rho, angle, min_threshold, np.array([]), minLineLength=8, maxLineGap=4)
    return line_segments

def average_line(frame, line_segments):
    if line_segments is None:
        return
    
    height, width, _ = frame.shape
    lane_lines = []
    left_fit = []
    right_fit = []
    left_region_boundary = width * (1 - 1/3)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * 1/3 # right lane line segment should be on left 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2: #vertical line
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))
    return lane_lines

def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def lane_detection_pipeline(frame):
    edges = canny_edge_detection(frame)
    cv.imshow("Caed", edges)
    cropped_edges = roi(edges)
    cv.imshow("Camered", cropped_edges)
    line_segments = hough_transform(cropped_edges)
    lane_lines = average_line(frame, line_segments)
    return lane_lines

def render_lines(frame, lines, steering_angle):
    #lane lines
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    #heading line
    # 0-89 degree: turn left
    # 90 degree: going straight
    # 91-180 degree: turn right 
    height, width, _ = frame.shape
    steering_angle_radian = steering_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian)) #unit circle 
    y2 = int(height / 2)
    cv.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)
    return frame

def steering_angle(frame, lane_lines, angle, num_of_lane_lines):
    if len(lane_lines) == 0:
        return -90

    height, width, _ = frame.shape

    if len(lane_lines) == 1:
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
    else:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        camera_mid_offset_percent = 0.02 # 0.0 means car pointing to center, -0.03: car is centered to left, +0.03 means car pointing to right
        mid = int(width / 2 * (1 + camera_mid_offset_percent))
        x_offset = (left_x2 + right_x2) / 2 - mid
    
    y_offset = int(height / 2)# find the steering angle, which is angle between navigation direction to end of center line
    angle_to_mid_radian = math.atan(x_offset / y_offset)  # angle (in radian) to center vertical line
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  # angle (in degrees) to center vertical line
    new_angle = angle_to_mid_deg + 90  # this is the steering angle needed by car front wheel

	
    if num_of_lane_lines == 2 :
        max_angle_deviation = 5
    else :
        max_angle_deviation = 1
    
    angle_deviation = new_angle - angle
    
    if abs(angle_deviation) > max_angle_deviation:
        stabilized_steering_angle = int(angle + max_angle_deviation * angle_deviation / abs(angle_deviation))
    else:
        stabilized_steering_angle = new_angle
    return stabilized_steering_angle

def drive_robot(angle):
	#print("angle" + str(angle))
	angle = (int(angle/2))
	if(angle) == 45: robot.forward(45)
	elif (angle) < 45: robot.manual_drive(angle, 45)
	else: robot.manual_drive(45 - (angle - 45), 45)

robot = motorAPI.Drivetrain(motorAPI.Motor(4),motorAPI.Motor(1))
stream = cv.VideoCapture(0)
angle = 90
while(stream.isOpened()):
    ret, frame = stream.read()
    if ret == True:
        frame = cv.resize(frame,(320,240))
        lane_lines = lane_detection_pipeline(frame)
        display_image = render_lines(frame, lane_lines, angle)
        cv.imshow("Camera Feed", display_image)
        angle = steering_angle(frame, lane_lines, angle, len(lane_lines))
        drive_robot(angle)
    if (cv.waitKey(1) & 0xFF == ord('q')):
        break

robot.shutdown()
stream.release()
cv.destroyAllWindows()