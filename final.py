import cv2
import time
import os
from ultralytics import YOLO
import paho.mqtt.client as mqtt
from playsound import playsound

# =============================== SETTINGS =================================
# YOLOv8 Model Path
MODEL_PATH = "yolov8n.pt"

# Region of Interest (ROI) coordinates
ROI_X, ROI_Y, ROI_W, ROI_H = 100, 100, 400, 400

# MQTT Settings
BROKER = "mqtt.eclipseprojects.io"
MQTT_TOPIC = "home/surveillance"

# Snapshot Settings
SNAPSHOT_DIR = "C:/surveillance/snapshots"  # Replace with your desired directory
ALERT_COOLDOWN = 30  # Cooldown in seconds to avoid repeated alerts

# Objects of interest (COCO dataset IDs): 0 = person, 2 = car
CLASSES_OF_INTEREST = [0, 2]

# Video Output Settings
OUTPUT_VIDEO_PATH = "annotated_output.avi"
FRAME_WIDTH, FRAME_HEIGHT = 1920, 1080
FPS = 20.0

# Alert Sound File
ALERT_SOUND_PATH = "C:/Users/infan/Music/ReelqAudio-33695.mp3"  # Replace with the path to your audio file
# =========================================================================


def setup_directories():
    """Create required directories for saving snapshots if they don't exist."""
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)


def setup_mqtt_client():
    """Initialize and connect to the MQTT broker."""
    client = mqtt.Client()
    try:
        client.connect(BROKER, 1883, 60)
        print("MQTT client connected successfully.")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        exit()
    return client


def save_snapshot(frame):
    """Save snapshot with a unique name to the specified directory."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    snapshot_path = os.path.join(SNAPSHOT_DIR, f"snapshot_{timestamp}.jpg")
    cv2.imwrite(snapshot_path, frame)
    print(f"Snapshot saved to {snapshot_path}")
    return snapshot_path


def trigger_audio_alert():
    """Play an audio alert sound."""
    try:
        playsound(ALERT_SOUND_PATH)
    except Exception as e:
        print(f"Error playing sound: {e}")


def main():
    # ======================= INITIAL SETUP ================================
    print("Initializing Smart Surveillance System...")
    setup_directories()

    # Load YOLOv8 model
    model = YOLO(MODEL_PATH)

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    # Setup MQTT client
    client = setup_mqtt_client()

    # Video Writer setup
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))

    # Logging file
    log_file = open("detection_log.txt", "a")

    # Alert cooldown settings
    last_alert_time = 0

    print("Starting Smart Surveillance System... Press 'q' to stop.")

    # ====================== MAIN PROGRAM LOOP ============================
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Extract Region of Interest (ROI)
        roi = frame[ROI_Y:ROI_Y+ROI_H, ROI_X:ROI_X+ROI_W]

        # Perform detection on ROI
        results = model(roi)

        # Annotate the ROI with detection results
        annotated_roi = results[0].plot()
        frame[ROI_Y:ROI_Y+ROI_H, ROI_X:ROI_X+ROI_W] = annotated_roi

        # Log detections
        detected_classes = results[0].names
        if detected_classes:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Detected: {detected_classes}\n")
            print(f"Logged detection: {detected_classes}")

        # Check for objects of interest and enforce alert cooldown
        detected_ids = results[0].boxes.cls.tolist()
        if any(cls in CLASSES_OF_INTEREST for cls in detected_ids):
            if time.time() - last_alert_time > ALERT_COOLDOWN:
                print("Alert: Object of interest detected!")
                snapshot_path = save_snapshot(frame)
                client.publish(MQTT_TOPIC, f"Object of interest detected! Snapshot saved at: {snapshot_path}")
                trigger_audio_alert()  # Play the alert sound
                last_alert_time = time.time()

        # Draw ROI rectangle
        cv2.rectangle(frame, (ROI_X, ROI_Y), (ROI_X + ROI_W, ROI_Y + ROI_H), (0, 255, 0), 2)

        # Write annotated frame to output video file
        out.write(frame)

        # Display the frame
        cv2.imshow("Smart Surveillance System", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # ====================== CLEANUP RESOURCES ============================
    cap.release()
    out.release()
    log_file.close()
    client.disconnect()
    cv2.destroyAllWindows()
    print("Surveillance System Stopped.")


if __name__ == "__main__":
    main()
