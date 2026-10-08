# 5-DOF Robotic Arm

A 5-DOF desktop robotic arm built for computer vision experiments and automated pick-and-place tasks.

The arm uses 3D-printed parts, high-torque hobby servos, and an ESP32 for control. Servo control is handled through a PCA9685 over I2C.

Part of the **Stardance** project.

## Hardware

| Component        | Spec / Model            | Qty | Notes                           |
| ---------------- | ----------------------- | --: | ------------------------------- |
| Microcontroller  | ESP32 DevKit V1         |   1 | Main controller                 |
| PWM Driver       | PCA9685 16-Channel      |   1 | I2C servo control               |
| Base Servo       | 150 kg·cm digital servo |   1 | Base rotation                   |
| Shoulder / Elbow | 40 kg·cm digital servos |   2 | Main arm joints                 |
| Wrist / Gripper  | 20 kg·cm digital servos |   2 | Wrist and gripper               |
| Power Supply     | 12V SMPS                |   1 | Stepped down for the servo rail |

The full parts list, prices, and sourcing information are in [`Documents/BOM.csv`](Documents/BOM.csv).

## Project Status

* [x] Full CAD assembly in Fusion 360
* [x] Wiring schematic and power distribution
* [x] Bill of Materials
* [x] Structural parts 3D printed
* [x] Mechanical assembly and dry-fit
* [x] Servo calibration and zero-point alignment
* [x] Forward and inverse kinematics
* [x] ESP32 firmware and PCA9685 control
* [ ] OpenCV camera integration
* [ ] Object detection
* [ ] Autonomous pick-and-place

## Repository

```text
├── CAD/
│   ├── Assembly/              # Complete Fusion 360 models
│   └── Individual Parts/      # Printable STL/STEP files
│
├── Code/                      # ESP32 firmware and control scripts
│
├── Documents/
│   ├── BOM.csv                # Parts, pricing, and specifications
│   ├── Pictures/              # Build photos and progress
│   └── Wiring_Schematic.*     # System schematics
│
└── README.md
```

## Software

* **CAD:** Autodesk Fusion 360
* **Firmware:** C++ / Arduino IDE
* **Microcontroller:** ESP32
* **Servo Control:** PCA9685 over I2C
* **Kinematics:** Python, NumPy
* **Computer Vision:** OpenCV
* **Development:** VS Code

## License

MIT License

Designed and built by Jake.
