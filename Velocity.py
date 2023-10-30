import cv2
from ultralytics import YOLO
import time

# Load the YOLOv8 model
model = YOLO(r'Bottle\best.pt')

# Open the video file
cap = cv2.VideoCapture(0)

# Initialize variables to track the previous position and time
prev_bbox = None
prev_time = None

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Initialize speed
        speed = 0.0

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        if results and results[0].boxes.id is not None:
            # Get the bounding box of the first detected object
            bbox = results[0].boxes.xyxy.cpu()[0]

            if prev_bbox is not None:
                # Calculate the distance between the current and previous bounding boxes
                distance = ((bbox[0] - prev_bbox[0])**2 + (bbox[1] - prev_bbox[1])**2)**0.5

                # Calculate the time elapsed between frames
                current_time = time.time()
                time_elapsed = current_time - prev_time

                if time_elapsed > 0:
                    # Calculate speed in pixels per second
                    speed = distance / time_elapsed

            # Update the previous bounding box and time for the next iteration
            prev_bbox = bbox
            prev_time = time.time()

            # Draw the bounding box and display the speed
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Speed: {speed:.2f} pixels/second", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Display the annotated frame with the bounding box and speed
        cv2.imshow("YOLOv8 Tracking", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
