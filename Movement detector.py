import pygame
import sys
import cv2
import numpy as np

# Initialize cv2
motion_detector = cv2.createBackgroundSubtractorMOG2()
cap = cv2.VideoCapture(0)

# Read the first frame for optical flow
ret, prev_frame = cap.read()
if not ret:
    print("Failed to capture video")
    sys.exit()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Initialize Pygame
pygame.init()

# Set up display
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ReMouvement")

# Define cube properties
cube_color = (0, 128, 255)
cube_size = 50
cube_x = (width - cube_size) // 2
cube_y = (height - cube_size) // 2

# Movement threshold
motion_threshold = 10000  # Adjust for sensitivity

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()
    if not ret:
        break

    # Apply the motion detector
    fg_mask = motion_detector.apply(frame)

    # Find contours of moving objects
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    movement_detected = False
    largest_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500 and area > largest_area:
            largest_area = area
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            movement_detected = True

    # Optical flow direction detection (only if movement detected)
    direction = ""
    if movement_detected and largest_area > motion_threshold:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        avg_mag = np.mean(mag)
        avg_flow = flow.mean(axis=(0, 1))
        dx, dy = avg_flow
        if avg_mag > 1:  # Only move if significant motion
            if abs(dx) > abs(dy):
                direction = "Right" if dx > 0 else "Left"
            else:
                direction = "Down" if dy > 0 else "Up"
        prev_gray = gray.copy()
    else:
        direction = ""

    cv2.putText(frame, f"Direction: {direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Frame", frame)

    # Move cube only if movement detected and direction is set
    if direction == "Right":
        cube_x += 10
    elif direction == "Left":
        cube_x -= 10
    elif direction == "Up":
        cube_y -= 10
    elif direction == "Down":
        cube_y += 10

    # Keep cube inside window
    cube_x = max(0, min(width - cube_size, cube_x))
    cube_y = max(0, min(height - cube_size, cube_y))

    screen.fill((255, 255, 255))  # Fill background with white
    pygame.draw.rect(screen, cube_color, (cube_x, cube_y, cube_size, cube_size))
    pygame.display.flip()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




# Initialize cv2
motion_detector = cv2.createBackgroundSubtractorMOG2()
cap = cv2.VideoCapture(0)

# Read the first frame for optical flow
ret, prev_frame = cap.read()
if not ret:
    print("Failed to capture video")
    sys.exit()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Initialize Pygame
pygame.init()

# Set up display
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ReMouvement")

# Define cube properties
cube_color = (0, 128, 255)
cube_size = 50
cube_x = (width - cube_size) // 2
cube_y = (height - cube_size) // 2

# Movement threshold
motion_threshold = 10000  # Adjust for sensitivity

pygame.quit()
sys.exit()