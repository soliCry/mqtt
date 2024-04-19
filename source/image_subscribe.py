from MQTTimageconnector import MQTTConnector
from YAMLReader import YAMLReader
import pandas as pd


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # mqtt_connector.connect()

    yamlreader = YAMLReader()
    yamlreader.init_config_file("config/mqtt_config.yml")
    topic = yamlreader.load_sys_config_value('image_topic')
    mqtt_connector = MQTTConnector()
    mqtt_connector.connect()
    mqtt_connector.subscribe(topic)

    # Listen for messages for 10 seconds
    mqtt_connector.listen()