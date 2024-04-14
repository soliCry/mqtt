import paho.mqtt.client as mqtt
from YAMLReader import YAMLReader
from ErrorLogger import ErrorLogger
import time
import random


class MQTTPublisher:
    def __init__(self):
        self.yamlreader = YAMLReader()
        self.error_logger = ErrorLogger()
        self.yamlreader.init_config_file("config/mqtt_config.yml")
        self.brokerURL = self.yamlreader.load_sys_config_value('brokerUrl')
        self.port = self.yamlreader.load_sys_config_value('port')
        self.keepAlive = self.yamlreader.load_sys_config_value('keepAlive')
        self.client = mqtt.Client(f'python-mqtt-{random.randint(0, 10000)}')
        self.publish_thread = None
        self.publishing = False

        # Set callback functions
        self.client.on_connect = self.on_connect

    def on_disconnect(self, client, userdata, rc):
        print("Client Got Disconnected")
        client.connect(self.brokerURL, self.port, self.keepAlive)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            # Subscribe to topics when connected
            self.subscribe_persisted_topics()
        else:
            print(f"Connection failed with result code {rc}")

    def connect(self):
        try:
            self.client.connect(self.brokerURL, port=self.port)
            self.client.loop_start()
        except Exception as e:
            self.error_logger.log_error(f"Error connecting to MQTT broker: {e}")

    def start_publishing(self):
        try:
            self.publishing = True
            self.publish_thread = threading.Thread(target=self.continuous_publish)
            self.publish_thread.start()
        except Exception as e:
            print(f"Error starting publishing thread: {e}")

    def stop_publishing(self):
        try:
            self.publishing = False
            if self.publish_thread:
                self.publish_thread.join()
        except Exception as e:
            print(f"Error stopping publishing thread: {e}")

    def continuous_publish(self):
        while self.publishing:
            try:
                topic_to_publish = "example/topic1"
                message_to_publish = "Continuous Publish"
                self.publish(topic_to_publish, message_to_publish)
                time.sleep(2)
            except Exception as e:
                print(f"Error in continuous publishing: {e}")