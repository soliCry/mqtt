import json
import yaml

from ErrorLogger import ErrorLogger


class YAMLReader:
    def __init__(self):
        self.config_data = None
        self.error_logger = ErrorLogger()

    def init_config_file(self, config_path):
        """
        This function is designed to facilitate the loading of YAML file.
        Args:
            config_path: file path of the YAML file

        Returns: NA

        """
        try:
            with open(config_path, 'r') as stream:
                self.config_data = json.loads(json.dumps(yaml.safe_load(stream)))
        except (yaml.YAMLError, json.JSONDecodeError) as exc:
            stream.close()
            self.error_logger.log_error(f"Error loading config file {config_path}: {exc}")
        finally:
            stream.close()

    def load_sys_config_value(self, key):
        """
        This function is to extract the value associated with a specified key from a loaded YAML file
        Args:
            key: The key string to retrie targeted information.

        Returns: Value (Targeted Information)

        """
        if self.config_data is not None and key in self.config_data:
            return self.config_data[key]
        else:
            self.error_logger.log_error(f"Key '{key}' not found in the system configuration.")
            return None