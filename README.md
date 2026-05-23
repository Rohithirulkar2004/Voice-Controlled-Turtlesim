# Voice-Controlled TurtleSim Robot using ROS 2

A ROS 2-based project that controls a TurtleSim robot using real-time voice commands. The system uses the Vosk offline speech recognition library to convert spoken commands into ROS 2 `Twist` velocity messages for robot navigation.

## Features

* Real-time voice-controlled robot movement
* Offline speech recognition using Vosk
* ROS 2 publisher-subscriber communication
* Dynamic speed adjustment using voice commands
* Modular ROS 2 Python package structure
* Compatible with TurtleSim and extendable to real robots

## Technologies Used

* ROS 2 Humble
* Python
* TurtleSim
* Vosk Speech Recognition
* sounddevice
* geometry_msgs/Twist
* rclpy

## Voice Commands

| Command          | Action         |
| ---------------- | -------------- |
| `forward` / `go` | Move forward   |
| `back`           | Move backward  |
| `left`           | Turn left      |
| `right`          | Turn right     |
| `stop`           | Stop movement  |
| `faster`         | Increase speed |
| `slower`         | Decrease speed |

## System Architecture

1. Microphone captures audio input
2. Audio processed using Vosk speech recognition
3. Recognized text mapped to movement commands
4. ROS 2 publishes `Twist` messages on `/turtle1/cmd_vel`
5. TurtleSim receives commands and moves accordingly

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/voice-controlled-turtlesim.git
cd voice-controlled-turtlesim
```

### Build the Workspace

```bash
colcon build
source install/setup.bash
```

### Install Dependencies

```bash
pip install vosk sounddevice
sudo apt install ros-humble-turtlesim
```

### Download Vosk Model

Download the English Vosk model from:

[Vosk Official Website](https://alphacephei.com/vosk/?utm_source=chatgpt.com)

Extract the model and place it in:

```bash
~/vosk_models/
```

## Run the Project

### Start TurtleSim

```bash
ros2 run turtlesim turtlesim_node
```

### Run Voice Control Node

```bash
ros2 run voice_turtlesim voice_control
```

## Project Structure

```bash
voice_turtlesim/
│── voice_turtlesim/
│   ├── voice_control.py
│── package.xml
│── setup.py
│── resource/
│── test/
```

## Results

* Achieved high command recognition accuracy
* Average response latency below 500 ms
* Successfully demonstrated ROS 2 topic-based communication and real-time robot control

## Future Improvements

* Multi-node ROS 2 architecture
* Support for multilingual voice commands
* Integration with physical robots like TurtleBot 3
* Noise filtering and wake-word detection
* Streaming speech recognition for smoother control

Based on the project report: 
