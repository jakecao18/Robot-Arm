# 5-DOF Robotic Arm

### Description

A 5-DOF desktop robotic arm built for that can pick and place objects using coordinates and arrow control.

The arm uses 3D-printed parts, high-torque hobby servos, and an ESP32 for control. Position calculations are ran on a laptop

Part of the **Stardance** project.

Devlogs are avalible on https://stardance.hackclub.com/projects/28283

### Uses

The arm is meant to be able to lift ojects around 1kg.

This robot arm will be controlled through a local web app. It can be controlled using coordinates, joint angles, and arrow keys.

### Why I built this

I built project mainly to learn more about robotics and start my first big project.

I have done smaller projects with arduinos kits before and want to upgrade to something a bit more complicated. I felt like a robotic arm would be educational and fun.

## Wiring

![Wiring Diagram](<Documents/pictures & videos/circuit_image.png>)

## CAD

![CAD Assembly](<Documents/pictures & videos/v2 picture 3.png>)

## Physical Robot

[![Robot Arm Demo](Documents/Pictures/finished build.jpg)](https://www.youtube.com/watch?v=XWoJphzX7BE)

## Hardware

| Component        | Spec / Model            | Qty | Notes                           |
| ---------------- | ----------------------- | --: | ------------------------------- |
| Microcontroller  | ESP32 DevKit V1         |   1 | Main controller                 |
| PWM Driver       | PCA9685 16-Channel      |   1 | I2C servo control               |
| Base Servo       | 150 kg·cm digital servo |   1 | Base rotation                   |
| Shoulder / Elbow | 40 kg·cm digital servos |   2 | Main arm joints                 |
| Wrist / Gripper  | 20 kg·cm digital servos |   2 | Wrist and gripper               |
| Power Supply     | 12V SMPS                |   1 | Stepped down for the servo rail |

The full parts list, prices, and sourcing information are in [`Documents/BOM template for robot arm - Sheet1.csv`](Documents/BOM template for robot arm - Sheet1.csv).

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

## License

MIT License

Designed and built by Jake.
