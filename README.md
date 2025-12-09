# Tennis Ball Tracking & Trajectory Prediction System
Real-time detection, tracking, physics prediction, and TUI-based source selection.

## Overview

This project implements a real-time tennis ball tracking and future trajectory prediction system using:
- A custom-trained YOLOv8 model (trained_best.pt)
- A Kalman filter for smooth state estimation
- A physics-based predictor for long-horizon motion simulation
- Homography correction for warped or slanted camera views
- A full terminal UI (TUI) for selecting video sources or webcams
- Real-time visualization with OpenCV

The system is designed to handle:
1. fast-moving balls
2. out-of-frame entry
3. motion blur
4. warped ground planes
5. cluttered backgrounds with floor markings

## Features
1. Accurate Tennis Ball Detection
    The project uses a YOLOv8 model trained exclusively on tennis ball images, ensuring:
    - No false positives on digits, lines, shadows, or other objects
    - Robust detection even under motion blur
    - Seamless tracking across frames


    Implemented in:
        src/model.py

2. Terminal UI (TUI) Source Selector
    A full-screen terminal application lets you:
    - Browse all webcams
    - Browse folders and select video files (.mp4, .mov, etc.)
    - View live ASCII preview of each selected source
    - Use fuzzy search
    - Navigate directories with scrolling
    
    Implemented in:
    - src/source_selector.py
    - src/file_picker.py
    - src/ascii_preview.py

3. Kalman Filter Tracking
    A 2D constant-velocity Kalman filter maintains a stable estimate of:
    
    - Ball position
    - Ball velocity
    
    It continues predicting when the ball is:
    - Temporarily lost
    - Occluded
    - Outside the frame
    
    Implemented in:
        src/kalman.py

4. Physics-Based Trajectory Prediction

    In addition to Kalman prediction, a physics module simulates:
    - Parabolic motion
    - Gravity
    - Bounce behavior
    - Energy loss
    - Estimated landing points

    This provides a forward prediction arc even when future motion is complex.
    
    Implemented in:
        src/physics_predictor.py

5. Homography & Planar Correction

    The optional homography utility allows:
    - Ground plane correction
    - Transforming warped/slanted camera perspectives
    - Mapping between pixel space and world coordinates

    Implemented in:
        src/homography_utils.py

6. Real-Time Visualization

    The main loop:
    - Draws YOLO detections
    - Draws Kalman predictions
    - Draws future predicted trajectory points
    - Optional landing point markers

    Implemented in:
        src/main.py

## Project Structure
src/
    
    main.py                 ← Main real-time loop
    model.py                ← YOLO detector wrapper
    kalman.py               ← 2D Kalman state estimator
    physics_predictor.py    ← Physics-based trajectory engine
    homography_utils.py     ← Ground transformation utilities
    camcorder.py            ← Simple camera wrapper
    source_selector.py      ← TUI interface for selecting sources
    file_picker.py          ← Fuzzy-search TUI file browser
    ascii_preview.py        ← Live ASCII video preview

assets/
    
    trained_best.pt         ← Custom YOLO tennis-ball-only model

## Installation
Requirements: 
    
    pip install ultralytics opencv-python numpy

Optional for TUI:
    
    pip install curses

(Linux/macOS usually include it by default)

▶️ Usage
1. Run the application
    python3 src/main.py

2. Select a source in the TUI

    #### You can:

- Choose a webcam
- Choose a video file
- Preview sources in ASCII
- Use fuzzy search to find files

3. Watch real-time tracking

    The OpenCV window displays:    
    - Green box → YOLO detection
    - Yellow dot → Detected center
    - Red dot → Kalman next-state prediction
    - Blue dots → Future predicted trajectory

## How It Works
Detection → Tracking → Prediction Pipeline

1. YOLOv8 detects the ball
     - Returns bounding box + center.

2. Kalman filter updates its state
    - Smooths noise and estimates velocity.

3. Physics predictor estimates the future path
    - Simulates gravity and bouncing.

4. Trajectory is rendered on-screen
    - Showing where the ball is likely to go.

### Model Performance

The custom model achieved:
    
- Precision: ~1.00
- Recall: ~0.999
- mAP50: 0.995
- mAP50–95: 0.921

## Dataset Generation (Optional)

This project includes a helper script (make_tennis_dataset.py) that:
    
    - Extracts frames from a video
    - Auto-labels tennis balls using YOLOv8x
    - Produces a training-ready YOLO dataset

#### Creates tennis.yaml for training

## Future Improvements
    
- Multi-camera 3D triangulation
- GPU-accelerated inference
- Real-world unit calibration
- Surface friction modeling
- Automatic bounce detection
- Rest-point prediction
