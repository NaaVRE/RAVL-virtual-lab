import yaml
import os

class SecretsProvider:        
    def __init__(self, file_path):
        self.file_path = file_path
        self.validate_yaml_file()    
            
    def validate_yaml_file(self) -> bool:
        return self.can_open_file_as_yaml() and self.file_content_parsed_to_dict()
        
    def can_open_file_as_yaml(self) -> bool:
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"File '{self.file_path}' does not exist.")
            return False
        try:
            with open(self.file_path, 'r') as f:
                yaml.safe_load(f)
            return True
        except yaml.YAMLError as exc:
            raise yaml.YAMLError(f"Error parsing YAML file: {exc}")
            return False
        
    def file_content_parsed_to_dict(self) -> bool:
        with open(self.file_path, 'r') as f:
            file_content = yaml.safe_load(f)
        content_parsed_to_dict: bool = isinstance(file_content, dict)
        if not content_parsed_to_dict:
            raise SyntaxError("File yaml content is not parsed to dict")
        return content_parsed_to_dict
        
    def get_secret(self, key: str) -> str:
        with open(self.file_path, 'r') as file:
            secrets = yaml.safe_load(file)
            return secrets[key]