> **Note**  
> This project has been replaced by a native macOS app [MQTTMenuBar ↗](https://github.com/saihgupr/MQTTMenuBar)  
> For the best experience on macOS, use the new version.

# MenuBar MQTT

A lightweight macOS status bar Python script that displays status from MQTT messages — either as **colored indicator dots** or **dynamic text**. Perfect for home automation systems, IoT monitoring, or any MQTT-based status indication needs.

## 🚀 Features

- **Color-coded indicators**: Red, Yellow, and Green dots using macOS-native colors  
- **Dynamic text display**: Show short MQTT-published values like `"17°C"`, `"ON"`, or `"75%"` in the menu bar  
- **MQTT integration**: Connects to any MQTT broker with support for authentication  
- **Runs in background**: No Dock icon; menu bar only  
- **Automatic reconnection**: Handles network interruptions  
- **Threaded MQTT handling**: Keeps the UI responsive  
- **Built for macOS**: Uses PyObjC for seamless system integration  

---

## 📦 Modes

### 🟢 MenuBar Dots

Displays a **single colored dot** in the menu bar based on incoming MQTT messages.

**MQTT Commands:**

- `"red"` → shows a red dot  
- `"yellow"` → shows a yellow dot  
- `"green"` → shows a green dot  
- `"off"` → hides the indicator  

**macOS Color Mappings:**

- **Red**: `NSColor.colorWithRed_green_blue_alpha_(1.0, 0.231, 0.188, 1.0)`  
- **Yellow**: `NSColor.colorWithRed_green_blue_alpha_(1.0, 0.8, 0.0, 1.0)`  
- **Green**: `NSColor.colorWithRed_green_blue_alpha_(0.196, 0.843, 0.294, 1.0)`  

**Change the Indicator Symbol:**

You can replace the `"●"` character with any Unicode symbol you prefer:

- `"◆"` for diamonds  
- `"▲"` for triangles  
- `"★"` for stars  
- `"■"` for squares

![Example Screenshot](https://i.imgur.com/QT3iRr9.gif)
  
---

### 🔤 MenuBar Text

Displays a **short dynamic text string** from MQTT messages directly in the menu bar.

**Example MQTT Payloads:**

- `"23°C"` → temperature reading  
- `"ON"` / `"OFF"` → binary state  
- `"75%"` → battery or humidity level  

This variant is ideal for showing real-time sensor values or device states.

![Example Screenshot](https://i.imgur.com/SNXdQzg.png)

---

## ⚙️ Requirements

- macOS 10.12 or later  
- Python 3.6+  
- [`pyobjc-framework-Cocoa`](https://pypi.org/project/pyobjc-framework-Cocoa/)  
- [`paho-mqtt`](https://pypi.org/project/paho-mqtt/)  

---

## 🛠 Installation

1. **Install Dependencies**
   ```bash
   pip install paho-mqtt pyobjc-framework-Cocoa
   ```

2. **Clone Repository**
   ```bash
   git clone git clone https://github.com/saihgupr/MenuBar
   cd MenuBar
   ```

3. **Configure MQTT Settings**
   
   Edit the following variables in the script:
   ```python
   self.mqtt_broker = "192.168.1.199"      # Your MQTT broker IP
   self.mqtt_port = 1883                    # MQTT port (default: 1883)
   self.mqtt_username = "XXX"          # MQTT username
   self.mqtt_password = "XXX"          # MQTT password
   self.mqtt_topic = "menubar/text"  # MQTT topic to subscribe to
   ```

4. **Run the Application**
   ```bash
   python3 menubar_dots.py
   ```
   
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
