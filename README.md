# Argus Sense: Intelligent Gesture & Sensor Fusion System

![Project Status](https://img.shields.io/badge/status-in%20development-yellow)
![Arduino](https://img.shields.io/badge/hardware-Arduino-00979D?logo=arduino)
![Python](https://img.shields.io/badge/code-Python%203.8+-3776AB?logo=python)
![Azure](https://img.shields.io/badge/cloud-Azure%20ML-0078D4?logo=microsoftazure)

## 🎯 Project Overview

Argus Sense is an advanced gesture-controlled system that combines hardware sensors, computer vision, and machine learning to enable intuitive human-computer interaction. The system uses sensor fusion to merge ultrasonic distance detection, ambient light sensing, and real-time hand tracking to recognize gestures and control system actions.

## 🏗️ System Architecture

```
Hardware Layer (Arduino)
    ↓
Serial Communication
    ↓
Python Processing Layer
    ↓
Sensor Fusion Engine → Computer Vision (MediaPipe)
    ↓
Gesture Recognition (ML Model)
    ↓
Action Layer (Mouse Control, LED Feedback)
    ↓
Azure ML (Training, Deployment, Logging)
```

## 🔧 Hardware Components

- **Arduino Uno**: Microcontroller for sensor interfacing
- **HC-SR04 Ultrasonic Sensor**: Distance measurement (2-400cm range)
- **2x Light Sensors (LDR)**: Ambient light detection
- **4-Pin RGB LED**: Visual feedback system

## 💻 Technology Stack

### Hardware Interface

- Arduino C++ (sensor data acquisition)
- PySerial (Arduino ↔ Python communication)

### Computer Vision

- OpenCV (camera input, preprocessing)
- MediaPipe (hand tracking, landmark detection)

### Machine Learning

- TensorFlow/PyTorch (gesture classification)
- Azure Machine Learning (experiment tracking, model deployment)

### Backend

- Flask/FastAPI (API endpoints)
- Azure Functions (serverless deployment)

## 📁 Project Structure

```
argus-sense/
├── arduino/
│   └── sensor_reader.ino          # Arduino sensor code
├── python/
│   ├── main.py                     # Application entry point
│   ├── hardware/
│   │   └── arduino_interface.py   # Serial communication
│   ├── vision/
│   │   ├── camera.py              # OpenCV camera interface
│   │   └── hand_tracker.py        # MediaPipe integration
│   ├── fusion/
│   │   └── sensor_fusion.py       # Multi-modal data fusion
│   ├── models/
│   │   └── gesture_classifier.py  # ML model
│   └── utils/
│       ├── logger.py              # Data logging
│       └── config.py              # Configuration management
├── data/
│   ├── raw/                       # Raw sensor logs
│   ├── processed/                 # Preprocessed data
│   └── samples/                   # Sample datasets
├── models/
│   ├── trained/                   # Trained model files
│   └── experiments/               # Experiment tracking
├── tests/
│   └── (unit tests)
├── docs/
│   └── (documentation)
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Development Stages

- [x] **Stage 1**: Arduino sensor validation & serial communication
- [ ] **Stage 2**: Python ↔ Arduino real-time data flow
- [ ] **Stage 3**: Computer vision setup (OpenCV + MediaPipe)
- [ ] **Stage 4**: Gesture recognition (rule-based)
- [ ] **Stage 5**: Sensor fusion engine
- [ ] **Stage 6**: Mouse control integration
- [ ] **Stage 7**: Data collection pipeline
- [ ] **Stage 8**: ML model training & evaluation
- [ ] **Stage 9**: Azure ML integration
- [ ] **Stage 10**: Production deployment

## 📊 Current Development Status

**Completed**: Arduino sensor interface with validated data output

**In Progress**: Python serial communication layer

**Next**: Computer vision pipeline setup

## 🎓 Learning Objectives

This project demonstrates:

- ✅ Hardware-software integration
- ✅ Real-time sensor data processing
- ✅ Computer vision & hand tracking
- ✅ Sensor fusion techniques
- ✅ Machine learning model development
- ✅ Cloud deployment (Azure)
- ✅ Professional software engineering practices

## 📝 Setup Instructions

### Prerequisites

- Arduino IDE
- Python 3.8+
- Git
- VS Code (recommended)

### Installation

```bash
# Clone repository
git clone https://github.com/Russell-Mazambara/Argus-Sense-Intelligent-Gesture-Sensor-Fusion-System.git

#cd into main file

# Install Python dependencies
pip install -r requirements.txt

# Upload Arduino code
# Open arduino/sensor_reader.ino in Arduino IDE and upload
```

### Running the System

```bash
# Start the application
python python/main.py
```

## 🤝 Contributing

This is a personal learning project. Feedback and suggestions are welcome!

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author


- GitHub: (https://github.com/RussellMazambara)

---


