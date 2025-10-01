Otoplasty Detection Project

This project contains two Python scripts for detecting ear protrusion using either real-time video capture or manual image point selection.
It combines OpenCV, dlib, and matplotlib to measure distances and estimate ear prominence relative to the head.

⸻

Project Structure

OTOPLASTIKA/
│
├── .venv/                          # Virtual environment (optional)
├── Drugo/                          # Additional files (optional)
├── venv/                           # Alternative virtual environment (optional)
│
├── DA3.webp                        # Example image for manual point selection
├── detekcija1.py                   # Real-time ear protrusion detection using webcam
├── detekcija2.py                   # Manual detection using image and grid
├── shape_predictor_68_face_landmarks.dat  # dlib facial landmark model

⸻

Requirements

Make sure you have Python 3.8+ installed.
Install the required libraries with:

pip install opencv-python dlib matplotlib numpy

Important:
	•	You must download the shape_predictor_68_face_landmarks.dat file (if not already included).
	•	This file is necessary for facial landmark detection and can be obtained from:
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

⸻

Script 1: Real-Time Detection (detekcija1.py)

This script uses your webcam to:
	•	Detect a face and facial landmarks.
	•	Estimate the position of ears relative to the head.
	•	Calculate ear–head distances.
	•	Determine whether the ears are protruding (klempave) based on distance thresholds.
	•	Estimate the distance of the face from the camera.

Run

python detekcija1.py

Press q to exit the camera window.

⸻

Script 2: Manual Image Analysis (detekcija2.py)

This script allows you to manually click on 4 reference points on a photo to measure distances.
It uses a simple grid interface to:
	•	Select points around the ears and nose.
	•	Calculate the distances between selected points.
	•	Determine whether the patient has protruding ears based on a custom ratio.

Run
	1.	Replace the putanja_do_slike variable in the script with the path to your image.
	2.	Run the script:

python detekcija2.py

	3.	Click the following 4 points in order on the displayed image:
	•	A → Left ear edge
	•	B → Left face point near the ear
	•	C → Nose or midline reference
	•	D → Right ear edge

The terminal will print calculated distances and a protrusion coefficient.

⸻

Notes
	•	The detection methods are simplified and not meant for medical diagnosis.
	•	Lighting and camera calibration can affect accuracy.
	•	Adjust focal_length and real_face_height in detekcija1.py to match your camera setup
