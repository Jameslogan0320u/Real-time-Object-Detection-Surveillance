
import cv2

def setup_video_writer(output_file="annotated_output.avi", frame_size=(640, 480), fps=20.0):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(output_file, fourcc, fps, frame_size)

def write_frame_to_video(video_writer, frame):
    video_writer.write(frame)

# Example usage
if __name__ == "__main__":
    # Initialize video writer
    video_writer = setup_video_writer()

    # Capture video from the default camera
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Write the frame to the video file
        write_frame_to_video(video_writer, frame)

        # Display the frame
        cv2.imshow('Frame', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and writer objects
    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()
