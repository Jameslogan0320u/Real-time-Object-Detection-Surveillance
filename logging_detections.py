import time

def log_detection(detections, log_file="detection_log.txt"):
    with open(log_file, "a") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - Detected: {detections}\n")
