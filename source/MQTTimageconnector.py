import paho.mqtt.client as mqtt
from YAMLReader import YAMLReader
from ErrorLogger import ErrorLogger
import time
import base64


class MQTTConnector:
    def __init__(self):
        self.yamlreader = YAMLReader()
        self.error_logger = ErrorLogger()
        self.yamlreader.init_config_file("config/mqtt_config.yml")
        self.brokerURL = self.yamlreader.load_sys_config_value('brokerUrl')
        self.port = self.yamlreader.load_sys_config_value('port')
        self.keepAlive = self.yamlreader.load_sys_config_value('keepAlive')
        self.client = mqtt.Client(self.yamlreader.load_sys_config_value('client_id'))
        self.subscribed_topics = []
        self.messages = []
        self.message_callback = None

        # Set callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

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

    def on_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            # 将接收到的消息转换为 base64 编码的字符串
            image_base64 = msg.payload.decode('utf-8')

            # 将 base64 编码的字符串转换为图片
            image_data = base64.b64decode(image_base64)

            # 保存图片
            with open('received_image.jpg', 'wb') as f:
                f.write(image_data)

            # Update the DataFrame with the received message and topic
            # self.message_df = self.message_df.append({'Topic': topic, 'Message': message}, ignore_index=True)
            # If a callback function is set, call it with the received message and topic
        except Exception as e:
            self.error_logger.log_error(f"Error processing message: {e}")

    def set_message_callback(self, callback):
        self.message_callback = callback

    def connect(self):
        """
        This function will use to connect with MQTT broker. Before using it, the brokerURL, port ,keepAlive,
        client_id must have to declare in config/mqtt_config.yml first.

        Returns: NA

        """
        try:
            self.client.connect(self.brokerURL, port=self.port)
            self.client.loop_start()
        except Exception as e:
            self.error_logger.log_error(f"Error connecting to MQTT broker: {e}")

    def publish(self, topic, message, qos=0):
        """
        This function is to publish the message through MQTT broker. Before using it, the brokerURL, port ,keepAlive,
        client_id must have to declare in config/mqtt_config.yml first.
        Args:
            topic: The topic name that you want to publish the message.
            message: The information that you want to publish.

        Returns: A successful message.

        """
        try:
            self.client.publish(topic, message, qos=qos)
            print(f"Published message: {message} on topic {topic}")
        except Exception as e:
            self.error_logger.log_error(f"Error publishing message: {e}")

    def continuous_publish(self, topic, message, interval=2, qos=0):
        """
        This function will continuously publish the message through MQTT broker. Before using it, the brokerURL,
        port ,keepAlive, client_id must have to declare in config/mqtt_config.yml first.

        Args:
            topic: The topic name that you want to publish the message.
            message: The information that you want to publish.
            interval: The interval to publish the message. The default value is 2.

        Returns: NA
        """
        try:
            while True:
                self.publish(topic, message, qos=qos)
                time.sleep(interval)
        except KeyboardInterrupt:
            self.error_logger.log_error("Continuous publishing interrupted")

    def subscribe(self, topic, qos=0):
        try:
            self.client.subscribe(topic, qos=qos)
            print(f"Subscribed to topic: {topic} with QoS {qos}")
            # Add the topic to the list of subscribed topics
            self.subscribed_topics.append(topic)
        except Exception as e:
            self.error_logger.log_error(f"Error subscribing to topic: {e}")

    def subscribe_many(self, topic_qos_dict):
        """
        This function is to subscribe list of the topics.
        Args:
            topic_qos_dict: key-value pairs of topic and qos.

        Returns:NA

        """
        try:
            for topic, qos in topic_qos_dict.items():
                self.subscribe(topic, qos=qos)
        except Exception as e:
            self.error_logger.log_error(f"Error subscribing to topics: {e}")

    def subscribe_persisted_topics(self):
        try:
            if self.subscribed_topics:
                # Assuming all topics have the same QoS for simplicity
                qos_level = 0 if not isinstance(self.subscribed_topics, dict) else self.subscribed_topics[0][1]
                self.client.subscribe([(topic, qos_level) for topic in self.subscribed_topics])
                print(f"Subscribed to topics: {self.subscribed_topics} with QoS {qos_level}")
        except Exception as e:
            self.error_logger.log_error(f"Error subscribing to persisted topics: {e}")

    def listen(self):
        """
        This function is to keep listening the topics that you subscribed.
        Returns: It will work with on_message function.

        """
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.error_logger.log_error("KeyboardInterrupting & Disconnecting from MQTT broker")
            self.client.disconnect()