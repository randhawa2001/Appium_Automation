# Spotify Panel Project

## Overview
The Spotify Panel project is a web-based application that automates and controls Spotify playback on multiple iOS devices. The project leverages Flask, Appium, Selenium, and MongoDB to manage device activities and playlists through an interactive web interface.

## Contents
- **`spot.html`**: UI for managing device settings such as IP, time values, and clones list.
- **`spotify-panel.py`**: Main backend script that serves the web interface, interacts with devices, and manages task execution.
- **`setup.py`**: Automation script for installing dependencies like Node.js, Appium, and Python packages.
- **`sp.py`**: Automation script controlling Spotify playback using Appium.

## System Requirements
- **Operating System**: macOS
- **Dependencies**:
  - **Python 3.x**
  - **Node.js**
  - **Appium Server**
  - **MongoDB**

### Required Python Packages
- Flask
- Appium-Python-Client (v2.7.1)
- Requests
- Selenium (v4.7.2)
- PyMongo

## Installation
### 1. Install System Dependencies
```sh
brew install node
npm install -g appium
npm install wd
brew install carthage
npm i -g webpack
brew install libimobiledevice
npm install -g authorize-ios
brew install ios-deploy
sudo xcode-select -r
brew install ideviceinstaller
```

### 2. Install Appium and Drivers
```sh
appium driver install xcuitest@4.32.10
npm install -g appium
```

### 3. Install Python Packages
Create a `requirements.txt` file with the following content:
```
Flask
Appium-Python-Client==2.7.1
requests
selenium==4.7.2
pymongo
```

Install the packages:
```sh
pip3 install -r requirements.txt
```

## Usage
### Run the Flask Server
```sh
python3 spotify-panel.py
```
Access the application at `http://0.0.0.0:1200` in a web browser.

### Control Devices
Navigate to the `/panel` endpoint to manage devices. Use the provided interface to start or stop tasks and check device status.

## Features
### 1. **Device Management**
- Automatically detects connected devices using `ios-deploy`.
- Maintains device-specific settings in MongoDB.
- Manages task execution through the web interface.

### 2. **Task Automation**
- Automates Spotify playback on iOS devices.
- Supports IP rotation, playback control, and playlist management.

### 3. **Persistent Settings**
- Device-specific settings such as IP, time values, and clones list are saved to MongoDB.
- Users can edit settings using the `/settings-form` endpoint.

### 4. **Enhanced UI and Logs**
- **`spot.html`**: Provides a modern web interface.
- **Logs Filtering**: Fetch logs per device for easier monitoring.

## Recent Improvements
- **Device-Specific Settings**: Added device-specific settings storage in MongoDB.
- **Enhanced Panel Links**: Linked each device to its settings page using query parameters.
- **Log Management**: Integrated individual log retrieval for each device.

## File Descriptions
- **`spot.html`**: Contains the web interface for managing input values.
- **`spotify-panel.py`**: Flask backend managing device statuses and task execution.
- **`setup.py`**: Automates dependency installation.
- **`sp.py`**: Controls Spotify playback on devices.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

## Acknowledgments
- [Appium](https://appium.io/): Used for iOS automation.
- [Flask](https://flask.palletsprojects.com/): Web framework.
- [MongoDB](https://www.mongodb.com/): Database for storing device configurations.

---
**Contributors:** Please feel free to submit issues and pull requests!

