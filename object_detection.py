from ultralytics import YOLO
import cv2


def load_yolo_model():
    return YOLO("yolov8n.pt")


def detect_objects(model, frame):
    results = model(frame)
    return results[0].plot()


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    model = load_yolo_model()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        annotated_frame = detect_objects(model, frame)
        cv2.imshow("Object Detection", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
