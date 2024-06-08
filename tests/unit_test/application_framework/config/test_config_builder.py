import os
from dataclasses import dataclass
from unittest.mock import patch, mock_open
from unit_test.unit_test_case import UnitTestCase
from application_framework.config.builder import ConfigBuilder
from application_framework.utils import str_to_bool


@dataclass
class Config:
    port: int = None
    debug: bool = False
    version: float = 1.0
    app_name: str = None
    database: dict = None

    @classmethod
    def from_dict(cls, config_dict):
        return cls(**config_dict)


class TestConfigBuilder(UnitTestCase):

    def setUp(self):
        self.builder = ConfigBuilder()

    def test_load_yaml_file(self):
        with patch("builtins.open", mock_open(read_data="port: 8080")):
            self.builder.add_yaml_file("config.test.yaml")
            config = self.builder.build()
            # Assert
            self.assertEqual(config['port'], 8080)

    def test_load_environment_variables(self):
        env_vars = {
            'CFG_port': '9090',
        }
        with patch.dict(os.environ, env_vars, clear=True):
            self.builder.add_prefixed_env_vars(prefix="CFG_", section_separator=".")
            config = self.builder.build()
            # Assert
            self.assertEqual(config['port'], '9090')

    def test_load_ini_file(self):
        ini_content = """
        [section]
        key=value
        port=8080
        """
        with patch("builtins.open", mock_open(read_data=ini_content)):
            self.builder.add_ini_file("config.test.ini")
            config = self.builder.build()
            # Assert
            self.assertEqual(config['section']['key'], 'value')
            self.assertEqual(config['section']['port'], '8080')

    def test_load_env_file(self):
        env_content = """
        key=value
        port=8080
        """
        with patch("builtins.open", mock_open(read_data=env_content)):
            self.builder.add_env_file("config.test.env")
            config = self.builder.build()
            # Assert
            self.assertEqual(config['key'], 'value')
            self.assertEqual(config['port'], '8080')

    def test_profiled_file_loading(self):
        yaml_content = """
        port: 8080
        """
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            self.builder.set_environment_profile("test")
            self.builder.add_profiled_file("config.{profile}.yaml")
            config = self.builder.build()
            # Assert
            self.assertEqual(config['port'], 8080)

    def test_convert_int_and_float_strings(self):
        env_vars = {
            'CFG_port': '9090',
            'CFG_version': '1.0',
        }
        with patch.dict(os.environ, env_vars, clear=True):
            self.builder.add_prefixed_env_vars(prefix="CFG_", section_separator=".")
            self.builder.set_type_conversion('port', int)
            self.builder.set_type_conversion('version', float)
            config = self.builder.build()
            # Assert
            self.assertEqual(config['port'], 9090)
            self.assertEqual(config['version'], 1.0)

    def test_convert_boolean_strings(self):
        test_cases = {
            'True': True,
            'true': True,
            '1': True,
            'yes': True,
            'y': True,
            'False': False,
            'false': False,
            '0': False,
            'no': False,
            'n': False,
        }
        for str_value, expected_bool in test_cases.items():
            with self.subTest(str_value=str_value):
                env_vars = {
                    'CFG_debug': str_value,
                }
                with patch.dict(os.environ, env_vars, clear=True):
                    self.builder.add_prefixed_env_vars(prefix="CFG_", section_separator=".")
                    self.builder.set_type_conversion('debug', str_to_bool)
                    config = self.builder.build()
                    # Assert
                    self.assertEqual(config['debug'], expected_bool, f"Failed for value: '{str_value}'")

    def test_type_conversion_error(self):
        yaml_content = """
        port: not_an_int
        """
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            self.builder.add_yaml_file("config.test.yaml")
            self.builder.set_type_conversion('port', int)
            # Assert
            with self.assertRaises(ValueError):
                self.builder.build()

    def test_unsupported_profiled_file_type(self):
        with self.assertRaises(ValueError) as context:
            self.builder._load_profiled_file("config.test.unsupported")
        self.assertEqual(str(context.exception),"Unsupported file type for profiled configuration")

    def test_overrides(self):
        yaml_content = """
            port: 8080
        """
        env_vars = {
            'CFG_port': '9090',
        }
        with patch.dict(os.environ, env_vars, clear=True):
            with patch("builtins.open", mock_open(read_data=yaml_content)):
                self.builder.add_yaml_file("config.test.yaml")
                self.builder.add_prefixed_env_vars(prefix="CFG_", section_separator=".")
                config = self.builder.build()
                # Assert
                self.assertEqual(config['port'], '9090')

    def test_environment_variable_sections(self):
        env_vars_with_sections = {
            'CFG_database.host': 'localhost',
            'CFG_database.port': '5432',
            'CFG_database.user': 'admin',
            'CFG_database.password': 'pass'
        }
        with patch.dict(os.environ, env_vars_with_sections, clear=True):
            self.builder.add_prefixed_env_vars(prefix="CFG_", section_separator=".")
            config = self.builder.build()
            # Assert
            expected_database = {
                'host': 'localhost',
                'port': '5432',
                'user': 'admin',
                'password': 'pass'
            }
            self.assertDictEqual(config['database'], expected_database)

    def test_preserves_types(self):
        yaml_content = """
            port: 8080
            debug: True
            version: 1.0
            app_name: TestApp
            database:
                host: localhost
                port: 5432
                user: user
                password: pass
        """
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            self.builder.add_yaml_file("config.test.yaml")
            config = self.builder.build()
            # Assert
            self.assertEqual(config['port'], 8080)
            self.assertEqual(config['debug'], True)
            self.assertEqual(config['version'], 1.0)
            self.assertEqual(config['app_name'], "TestApp")
            expected_database = {
                'host': 'localhost',
                'port': 5432,
                'user': 'user',
                'password': 'pass'
            }
            self.assertDictEqual(config['database'], expected_database)

    def test_binding_to_config_class(self):
        yaml_content = """
            port: 8080
            debug: True
        """
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            self.builder.add_yaml_file("config.test.yaml")
            self.builder.bind(Config)
            config = self.builder.build()
            # Assert
            self.assertIsInstance(config, Config)
            self.assertEqual(config.port, 8080)
            self.assertTrue(config.debug)

    def test_complex_nested_config(self):
        yaml_content = """
            database:
                host: localhost
                port: 5432
                credentials:
                    user: admin
                    password: pass
        """
        env_vars = {
            'CFG_database.credentials.user': 'new_admin'
        }
        with patch.dict(os.environ, env_vars, clear=True):
            with patch("builtins.open", mock_open(read_data=yaml_content)):
                self.builder.add_yaml_file("config.test.yaml")
                self.builder.add_prefixed_env_vars(prefix="CFG_", section_separator=".")
                config = self.builder.build()
                expected_database = {
                    'host': 'localhost',
                    'port': 5432,
                    'credentials': {
                        'user': 'new_admin',
                        'password': 'pass'
                    }
                }
                self.assertDictEqual(config['database'], expected_database)
