5-DOF Robotic Arm
A 5-DOF desktop robotic arm built for computer vision experiments and automated pick-and-place tasks. Designed around 3D-printed structural components, high-torque hobby servos, and an ESP32 microcontroller driven over I2C.
Part of the Stardance project.
Hardware Overview
Component
Spec / Model
Qty
Notes
Microcontroller
ESP32 DevKit V1
1
Main controller
PWM Driver
PCA9685 (16-Channel)
1
I2C servo control
Base Servo
150 kg·cm digital servo
1
High-load base rotation
Shoulder / Elbow
40 kg·cm digital servos
2
Primary arm joints
Wrist / Gripper
20 kg·cm digital servos
2
End-effector orientation & grip
Power Supply
12V SMPS
1
Stepped down to servo rail

A complete parts breakdown and sourcing links are tracked in Documents/BOM.csv.
Project Status
[x] Full CAD assembly in Fusion 360
[x] Wiring schematic & power distribution design
[x] Bill of Materials finalized
[x] Structural component 3D printing
[x] Mechanical assembly & dry-fit
[x] Servo calibration & zero-point alignment
[x] Forward & inverse kinematics solver
[x] ESP32 firmware (PWM signal mapping via PCA9685)
[ ] OpenCV / camera integration for object detection
[ ] Autonomous pick-and-place routines
Repository Layout
├── CAD/
│   ├── Assembly/              # Complete Fusion 360 models
│   └── Individual Parts/      # Printable STL/STEP files
├── Code/                      # ESP32 firmware & control scripts
├── Documents/
│   ├── BOM.csv                # Component list, pricing, and specs
│   ├── Pictures/              # Build logs and progress photos
│   └── Wiring_Schematic.*     # System schematics (SVG / PNG)
└── README.md


Tech Stack & Tools
CAD / Modeling: Autodesk Fusion 360
Embedded Firmware: ESP-IDF / C++ via Arduino IDE
Kinematics & Vision: Python (OpenCV, NumPy) in VS Code
License
Distributed under the MIT License. Designed and built by Jake.
