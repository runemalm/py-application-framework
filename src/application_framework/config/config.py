from dataclasses import dataclass

@dataclass
class Host:
    port: int = 80

@dataclass
class App:
    port: int = 5000

@dataclass
class Config:
    host: Host = Host()
    app: App = App()

    @classmethod
    def from_dict(cls, config_dict):
        host_config = config_dict.get('host', {})
        app_config = config_dict.get('app', {})
        return cls(host=Host(**host_config), app=App(**app_config))
