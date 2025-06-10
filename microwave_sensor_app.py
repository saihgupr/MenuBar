#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import threading
import time
from Foundation import NSObject
from objc import super
from AppKit import (
    NSApplication, NSStatusBar, NSVariableStatusItemLength,
    NSMenuItem, NSMenu, NSColor, NSAttributedString,
    NSFontAttributeName, NSFont, NSForegroundColorAttributeName,
    NSBaselineOffsetAttributeName,
    NSApplicationActivationPolicyAccessory # <-- Added import for NSApplicationActivationPolicyAccessory
)

class MicrowaveSensorApp(NSObject):
    def init(self):
        self = super().init()
        if self is None: return None

        # Create status bar item
        self.statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)

        # Create dots with different colors
        font = NSFont.menuBarFontOfSize_(14.0)
        base_attrs = {
            NSFontAttributeName: font,
            NSBaselineOffsetAttributeName: -0.75  # Moved significantly higher
        }
        
        # Create colored dots with Mac-like colors
        self.dots = {
            'red': NSAttributedString.alloc().initWithString_attributes_(
                "●", {**base_attrs, NSForegroundColorAttributeName: NSColor.colorWithRed_green_blue_alpha_(1.0, 0.231, 0.188, 1.0)}),  # Mac system red
            'yellow': NSAttributedString.alloc().initWithString_attributes_(
                "●", {**base_attrs, NSForegroundColorAttributeName: NSColor.colorWithRed_green_blue_alpha_(1.0, 0.8, 0.0, 1.0)}),  # Mac system yellow
            'green': NSAttributedString.alloc().initWithString_attributes_(
                "●", {**base_attrs, NSForegroundColorAttributeName: NSColor.colorWithRed_green_blue_alpha_(0.196, 0.843, 0.294, 1.0)})   # Mac system green
        }
        # Set initial state
        self.statusitem.setAttributedTitle_(NSAttributedString.alloc().initWithString_attributes_(" ", {}))

        # MQTT Settings
        self.mqtt_broker = "192.168.1.199"
        self.mqtt_port = 1883  # Default MQTT port
        self.mqtt_username = "XXX"
        self.mqtt_password = "XXX"
        self.mqtt_topic = "all/hallway/microwave_sensor/color"

        # Initialize MQTT client
        self.client = mqtt.Client()
        self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        # Start MQTT in a separate thread
        self.mqtt_thread = threading.Thread(target=self.mqtt_loop)
        self.mqtt_thread.daemon = True
        self.mqtt_thread.start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            self.client.subscribe(self.mqtt_topic)
            print(f"Subscribed to topic: {self.mqtt_topic}")
        else:
            print(f"Failed to connect to MQTT broker with code: {rc}")

    def on_message(self, client, userdata, message):
        payload = message.payload.decode()
        print(f"Received message: {payload} on topic: {message.topic}")
        
        if payload == "off":
            print("Clearing dot")
            self.statusitem.setAttributedTitle_(NSAttributedString.alloc().initWithString_attributes_(" ", {}))
        elif payload.lower() in self.dots:
            print(f"Setting {payload} dot")
            self.statusitem.setAttributedTitle_(self.dots[payload.lower()])
        else:
            print(f"Unknown state: {payload}")

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT broker")
        if rc != 0:
            print("Unexpected disconnection. Attempting to reconnect...")
            self.reconnect_mqtt()

    def reconnect_mqtt(self):
        while True:
            try:
                self.client.connect(self.mqtt_broker, self.mqtt_port)
                break
            except Exception as e:
                print(f"Reconnection failed: {e}")
                time.sleep(5)

    def mqtt_loop(self):
        while True:
            try:
                print(f"Attempting to connect to MQTT broker at {self.mqtt_broker}:{self.mqtt_port}")
                self.client.connect(self.mqtt_broker, self.mqtt_port)
                self.client.loop_forever()
            except Exception as e:
                print(f"MQTT Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyAccessory) # <-- Added line to prevent Dock icon
    sensor_app = MicrowaveSensorApp.alloc().init()
    app.run()