# Robot Arm

A 5-DOF desktop robotic arm designed for object manipulation and AI vision. This project focuses on creating a strong, modular, and affordable robot arm using 3D-printed parts, hobby servos, an ESP32 controller, and open-source software.

---

## Overview

The goal of this project is to design and build a fully functional robotic arm capable of precise movement, autonomous control, and AI-assisted operation. The arm is designed to be modular so that components can be upgraded or replaced as the project evolves.

This project is being developed as part of **Stardance**, with development documented through GitHub commits and devlogs.

---


### Current
- 3D CAD designed from scratch
- 5 Degrees of Freedom (DOF)
- ESP32 control system
- Wiring schematic with all components

### Planned
- Inverse kinematics
- AI vision using a camera
- Object detection and tracking
- Pick-and-place automation
- Mobile app control
- Voice commands

---

## Hardware

| Component | Quantity |
|-----------|---------:|
| ESP32 DevKit V1 | 1 |
| PCA9685 Servo Driver | 1 |
| 150kg Servo | 1 |
| 40kg Servo | 2 |
| 20kg Servo | 2 |
| 12V SMPS | 1 |

A complete Board of Materials is available in:

```
Documents/BOM.csv
```

---

## Repository Structure

```
Robot Arm Project/

├── CAD/
│   ├── Assembly
│   └── Individual Parts
│
├── Code/
│
├── Documents/
│   ├── BOM.csv
|   ├── Pictures
│   ├── Wiring_Schematic.svg
│   └── Wiring_Schematic.png
│
│
└── README.md
```

---

## Software

- Arduino IDE
- Python VS Code
- Fusion 360

---

## Progress

- [x] CAD Design
- [x] Wiring Schematic
- [x] Board of Materials
- [x] 3D Printing
- [ ] Assemble robot
- [ ] Inverse Kinematics
- [ ] Web Control
- [ ] AI Vision
- [ ] Autonomous Object Manipulation

---

## Documentation

Development progress is documented through:

- GitHub commits
- Stardance devlogs
- Build photos

---

## Future Goals

- Accurate inverse kinematics
- Autonomous pick-and-place
- AI-powered object recognition
- Object tracking 
- Voice controls

---

## License

This project is licensed under the MIT License.

---

## Author

Jake

Built as a personal robotics project for learning mechanical design, embedded systems, and computer vision.