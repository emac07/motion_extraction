import cv2
import sys
import numpy as np

def motion_extraction(input_file, output_file):
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print(f"Error: cannot open video file {input_file}")
        sys.exit(1)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    ret, prev_frame = cap.read()
    if not ret:
        print("Error: cannot read the first frame from the video.")
        cap.release()
        out.release()
        sys.exit(1)
    
    while True:
        ret, current_frame = cap.read()
        if not ret:
            break
        
        inverted_prev = 255 - prev_frame
        
        blended = cv2.addWeighted(current_frame, 0.5, inverted_prev, 0.5, 0)
        
        out.write(blended)
        
        prev_frame = current_frame
    
    cap.release()
    out.release()
    print("Finished: Outputted at:", output_file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python motion_extraction.py <input_video> <output_video>")
        sys.exit(1)
    
    input_video = sys.argv[1]
    output_video = sys.argv[2]
    
    motion_extraction(input_video, output_video)
