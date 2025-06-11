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
    NSApplicationActivationPolicyAccessory,
    # --- ADDED: New imports for bold font handling ---
    NSFontManager, NSFontBoldTrait
)

class MenubarDisplayApp(NSObject):
    def init(self):
        self = super().init()
        if self is None: return None

        # Create status bar item
        self.statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)

        # --- MODIFIED: Font creation logic to get a bold version ---

        # 1. Get the standard system font used in the menu bar.
        base_font_size = 14.0
        base_font = NSFont.menuBarFontOfSize_(base_font_size)

        # 2. Use the font manager to find the bold version of that font.
        font_manager = NSFontManager.sharedFontManager()
        bold_font = font_manager.convertFont_toHaveTrait_(base_font, NSFontBoldTrait)
        
        # 3. Fallback to the base font if a bold version isn't available
        if bold_font is None:
            print("Warning: Could not find a bold variant of the menu bar font. Using the standard font.")
            bold_font = base_font

        # 4. Define the text attributes using our new bold font.
        self.text_attributes = {
            NSForegroundColorAttributeName: NSColor.textColor(),
            NSBaselineOffsetAttributeName: -1.0
        }
        
        # --- End of font modification ---

        # Set an initial state to show the app is running
        initial_text = NSAttributedString.alloc().initWithString_attributes_("...", self.text_attributes)
        self.statusitem.setAttributedTitle_(initial_text)


        # MQTT Settings
        self.mqtt_broker = "192.168.1.199" # Fill in with your IP MQTT Broker Address
        self.mqtt_port = 1883  # Default MQTT port
        self.mqtt_username = "XXX" # Fill in with your username if you have one
        self.mqtt_password = "XXX" # Fill in with your password if you have one
        self.mqtt_topic = "menubar/text" # Change topic if you like

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
        print(f"Received message: '{payload}' on topic: '{message.topic}'")

        if payload.lower() == "off" or payload == "":
            print("Clearing menubar text")
            self.statusitem.setTitle_("")
        else:
            print(f"Updating menubar with: '{payload}'")
            display_text = NSAttributedString.alloc().initWithString_attributes_(
                payload, self.text_attributes
            )
            self.statusitem.setAttributedTitle_(display_text)

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
    app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
    display_app = MenubarDisplayApp.alloc().init()
    app.run()
