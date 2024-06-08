from dataclasses import dataclass


@dataclass
class HostConfig:
    port: int = 80

@dataclass
class AppConfig:
    port: int = 5000

@dataclass
class Config:
    host: HostConfig = HostConfig()
    app: AppConfig = AppConfig()

    @classmethod
    def from_dict(cls, config_dict):
        host_config = config_dict.get('host', {})
        app_config = config_dict.get('app', {})
        return cls(host=HostConfig(**host_config), app=AppConfig(**app_config))
