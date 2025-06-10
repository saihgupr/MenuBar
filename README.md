# MQTT MenuBar

A lightweight macOS status bar python script that displays colored indicator dots based on MQTT messages from microwave sensors. Perfect for home automation systems, IoT monitoring, or any MQTT-based status indication needs.

## Features

- **Color-coded status indicators**: Red, Yellow, and Green dots using Mac system colors
- **MQTT integration**: Connects to your MQTT broker with authentication support
- **Background operation**: Runs without showing in Dock
- **Automatic reconnection**: Handles network interruptions gracefully
- **Threaded MQTT handling**: Non-blocking UI operations
- **Native macOS integration**: Uses PyObjC for seamless menu bar integration

## Requirements

- macOS 10.12 or later
- Python 3.6+
- PyObjC framework
- paho-mqtt library

## Installation

1. **Install Dependencies**
   ```bash
   pip install paho-mqtt pyobjc-framework-Cocoa
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/microwave-sensor-statusbar.git
   cd microwave-sensor-statusbar
   ```

3. **Configure MQTT Settings**
   
   Edit the following variables in the script:
   ```python
   self.mqtt_broker = "192.168.1.199"      # Your MQTT broker IP
   self.mqtt_port = 1883                    # MQTT port (default: 1883)
   self.mqtt_username = "XXX"          # MQTT username
   self.mqtt_password = "XXX"          # MQTT password
   self.mqtt_topic = "all/hallway/example/color"  # MQTT topic to subscribe to
   ```

4. **Run the Application**
   ```bash
   python3 microwave_sensor_app.py
   ```

## Usage

The application subscribes to the configured MQTT topic and displays colored dots based on received messages:

- **Red dot**: Send `"red"` to MQTT topic
- **Yellow dot**: Send `"yellow"` to MQTT topic  
- **Green dot**: Send `"green"` to MQTT topic
- **Clear indicator**: Send `"off"` to hide the dot

## Configuration

Key configuration options in the script:

```python
# MQTT Configuration
mqtt_broker = "your.mqtt.broker.ip"
mqtt_port = 1883
mqtt_username = "your_username"
mqtt_password = "your_password"
mqtt_topic = "your/mqtt/topic"

# Visual Configuration
font_size = 14.0                    # Menu bar font size
baseline_offset = -0.75             # Vertical positioning of dots
```

## Colors

The app uses macOS system colors for native integration:

- **Red**: `NSColor.colorWithRed_green_blue_alpha_(1.0, 0.231, 0.188, 1.0)`
- **Yellow**: `NSColor.colorWithRed_green_blue_alpha_(1.0, 0.8, 0.0, 1.0)`
- **Green**: `NSColor.colorWithRed_green_blue_alpha_(0.196, 0.843, 0.294, 1.0)`

### Changing the Indicator Symbol

Replace the `"●"` character with any Unicode symbol you prefer:
- `"◆"` for diamonds
- `"▲"` for triangles  
- `"★"` for stars
- `"■"` for squares

### Auto-Start on Login

To run the app automatically when you log in:

1. Open **System Preferences** → **Users & Groups**
2. Select your user account
3. Click **Login Items** tab
4. Add the Python script or create a wrapper script

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [PyObjC](https://pyobjc.readthedocs.io/) for native macOS integration
- Uses [paho-mqtt](https://pypi.org/project/paho-mqtt/) for reliable MQTT communication
- Inspired by the need for simple IoT status monitoring
