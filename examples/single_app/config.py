from dataclasses import dataclass, field


@dataclass
class HostConfig:
    port: int = 80

@dataclass
class AppConfig:
    port: int = 5000
    greeting: str = "Hello World"

@dataclass
class Config:
    host: HostConfig = field(default_factory=HostConfig)
    app: AppConfig = field(default_factory=AppConfig)

    @classmethod
    def from_dict(cls, config_dict):
        host_config = config_dict.get('host', {})
        app_config = config_dict.get('app', {})
        return cls(host=HostConfig(**host_config), app=AppConfig(**app_config))
