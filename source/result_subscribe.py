from MQTTConnector import MQTTConnector
from YAMLReader import YAMLReader
import pandas as pd


def process_message(topic, message):
    print(f"Processing message from topic: {topic}")
    # Example processing: appending to a DataFrame
    global message_df
    message_df = message_df.append({'Topic': topic, 'Message': message}, ignore_index=True)
    # You can add more complex processing logic here


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # mqtt_connector.connect()

    yamlreader = YAMLReader()
    yamlreader.init_config_file("config/mqtt_config.yml")
    topic = yamlreader.load_sys_config_value('result_topic')
    mqtt_connector = MQTTConnector()
    mqtt_connector.set_message_callback(process_message)
    mqtt_connector.connect()
    mqtt_connector.subscribe(topic)

    # Listen for messages for 10 seconds
    mqtt_connector.listen()

    # Publish a message
    # topic_to_publish = "/python/cry"
    # message_to_publish = "1"
    # mqtt_connector.publish(topic_to_publish, message_to_publish)
