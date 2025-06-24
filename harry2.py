import cv2
import numpy as np
import time

def create_background(cap, num_frames=30, interval=0.1):
    """Capture median background more efficiently with progress feedback."""
    print(f"Capturing {num_frames} frames for background. Please move out of frame.")
    backgrounds = []
    start_time = time.time()
    
    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: Could not read frame {i+1}/{num_frames}")
            continue
            
        backgrounds.append(frame)
        
        # Calculate estimated time remaining
        elapsed = time.time() - start_time
        remaining = (num_frames - i - 1) * interval
        print(f"\rProgress: {i+1}/{num_frames} | Elapsed: {elapsed:.1f}s | Remaining: {remaining:.1f}s", end="")
        
        time.sleep(interval)
    
    print()  # New line after progress
    if not backgrounds:
        raise ValueError("Could not capture any frames for background")
    
    return np.median(backgrounds, axis=0).astype(np.uint8)
    
def create_mask(frame, lower_color, upper_color):
    """Create a refined mask with optimized morphological operations."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Use a single kernel for all morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    
    # Combine opening and dilation in one step
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    return mask

def apply_cloak_effect(frame, mask, background):
    """Apply the cloak effect more efficiently using numpy operations."""
    # Use numpy where instead of bitwise operations for better readability
    return np.where(mask[..., None], background, frame)

def main():
    print("OpenCV version:", cv2.__version__)

    # Initialize video capture with error handling
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Set camera resolution for better performance (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    try:
        background = create_background(cap)
    except ValueError as e:
        print(f"Error: {e}")
        cap.release()
        return

    # Define color range for cloak (HSV format)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    print("Starting main loop. Press 'q' to quit or 'r' to recapture background.")
    
    prev_time = time.time()
    frame_count = 0
    fps = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            time.sleep(0.5)
            continue

        # Calculate FPS
        frame_count += 1
        if time.time() - prev_time >= 1.0:
            fps = frame_count
            frame_count = 0
            prev_time = time.time()
        
        mask = create_mask(frame, lower_blue, upper_blue)
        result = apply_cloak_effect(frame, mask, background)
        
        # Display FPS on screen
        cv2.putText(result, f"FPS: {fps}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Invisible Cloak', result)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            try:
                background = create_background(cap)
                print("Background recaptured!")
            except ValueError as e:
                print(f"Error recapturing background: {e}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()