import cv2

def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def save_video(output_video_frames, output_video_path):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (output_video_frames[0].shape[1], output_video_frames[0].shape[0]))
    for frame in output_video_frames:
        out.write(frame)
    out.release()



import cv2

def display_video(output_video_frames, window_name="Video", fps=70, width=640, height=480):
    """
    Display video frames using OpenCV, with optional resizing to fit a desired window size.

    Args:
        output_video_frames (list): List of frames (numpy arrays).
        window_name (str): Name of the display window.
        fps (int): Frames per second for playback.
        width (int): Desired width of the displayed video.
        height (int): Desired height of the displayed video.

    Returns:
        None
    """
    if not output_video_frames:
        print("Error: No video frames to display.")
        return

    delay = int(1000 / fps)  # Calculate delay in milliseconds for given FPS

    for frame in output_video_frames:
        if frame is None:
            print("Warning: Encountered a None frame, skipping...")
            continue
        
        # Resize the frame to the desired size
        resized_frame = cv2.resize(frame, (width, height))

        cv2.imshow(window_name, resized_frame)  # Display the resized frame in a window

        # Wait for the delay (and check for 'q' key to exit)
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
