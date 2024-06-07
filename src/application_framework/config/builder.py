class ConfigBuilder:
    def __init__(self):
        self.environment_profile = 'development'
        self.config_sources = []
        self.configuration = {}
        self.config_class = None
        self.type_map = {}

    def set_environment_profile(self, env):
        self.environment_profile = env
        return self

    def add_config_source(self, source_type, data):
        self.config_sources.append((source_type, data))
        return self

    def add_profiled_file(self, template):
        self.add_config_source("profiled", template)
        return self

    def add_yaml_file(self, path):
        self.add_config_source("yaml", path)
        return self

    def add_json_file(self, path):
        self.add_config_source("json", path)
        return self

    def add_ini_file(self, path):
        self.add_config_source("ini", path)
        return self

    def add_env_file(self, path):
        self.add_config_source("env", path)
        return self

    def add_prefixed_env_vars(self, prefix="CFG_", section_separator="."):
        self.add_config_source("env_vars", (prefix, section_separator))
        return self

    def set_type_conversion(self, key, type_func):
        self.type_map[key] = type_func
        return self

    def _apply_type_conversion(self, key, value):
        if key in self.type_map:
            try:
                return self.type_map[key](value)
            except ValueError as e:
                raise ValueError(f"Error converting {key}: {e}")
        return value

    def bind(self, config_class):
        self.config_class = config_class
        return self

    def build(self):
        self._process_sources()
        if self.config_class:
            self.configuration = self.config_class.from_dict(self.configuration)
        return self.configuration

    def _process_sources(self):
        for source_type, data in self.config_sources:
            if source_type == "yaml":
                self.configuration.update(self._load_yaml_file(data))
            elif source_type == "json":
                self.configuration.update(self._load_json_file(data))
            elif source_type == "ini":
                self.configuration.update(self._load_ini_file(data))
            elif source_type == "env":
                self.configuration.update(self._load_env_file(data))
            elif source_type == "env_vars":
                prefix, section_separator = data
                self._load_environment_variables(prefix, section_separator)
            elif source_type == "profiled":
                self.configuration.update(self._load_profiled_file(data))

    def _load_profiled_file(self, template):
        profiled_path = template.replace("{profile}", self.environment_profile)
        if profiled_path.endswith(".yaml"):
            return self._load_yaml_file(profiled_path)
        elif profiled_path.endswith(".json"):
            return self._load_json_file(profiled_path)
        elif profiled_path.endswith(".ini"):
            return self._load_ini_file(profiled_path)
        else:
            raise ValueError("Unsupported file type for profiled configuration")

    def _load_environment_variables(self, prefix, section_separator='.'):
        import os
        for key, value in os.environ.items():
            if prefix and key.startswith(prefix):
                path = key[len(prefix):].split(section_separator)
                nested_key = '.'.join(path)
                converted_value = self._apply_type_conversion(nested_key, value)
                self._set_nested_config(self.configuration, path, converted_value)

    def _set_nested_config(self, config, path, value):
        for key in path[:-1]:
            config = config.setdefault(key, {})
        config[path[-1]] = value

    def _load_yaml_file(self, path):
        import yaml
        with open(path, 'r') as f:
            raw_config = yaml.safe_load(f) or {}
        return {k: self._apply_type_conversion(k, v) for k, v in raw_config.items()}

    def _load_json_file(self, path):
        import json
        with open(path, 'r') as f:
            raw_config = json.load(f)
        return {k: self._apply_type_conversion(k, v) for k, v in raw_config.items()}

    def _load_ini_file(self, path):
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read(path)
        converted_config = {}
        for section in parser.sections():
            section_dict = {}
            for key, value in parser.items(section):
                full_key = f"{section}.{key}"
                section_dict[key] = self._apply_type_conversion(full_key, value)
            converted_config[section] = section_dict
        return converted_config

    def _load_env_file(self, path):
        env_config = {}
        with open(path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_config[key.strip()] = self._apply_type_conversion(key.strip(),
                                                                          value.strip())
        return env_config
