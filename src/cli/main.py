import argparse
import configparser
import os
import shutil

LOCAL_CONFIG_FILE = os.path.join('.application_framework', 'config')
GLOBAL_CONFIG_FILE = os.path.expanduser('~/.application_framework/config')
SYSTEM_CONFIG_FILE = '/etc/application_framework/config'
DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default_config_cli.ini')

def read_config_file(file_path):
    config = configparser.ConfigParser()
    if os.path.exists(file_path):
        config.read(file_path)
    return config

def create_global_config_if_not_exists():
    if not os.path.exists(os.path.dirname(GLOBAL_CONFIG_FILE)):
        os.makedirs(os.path.dirname(GLOBAL_CONFIG_FILE))
    if not os.path.exists(GLOBAL_CONFIG_FILE):
        shutil.copy(DEFAULT_CONFIG_FILE, GLOBAL_CONFIG_FILE)

def merge_configs(system_config, global_config, local_config):
    merged_config = configparser.ConfigParser()
    for config_parser in (system_config, global_config, local_config):
        for section in config_parser.sections():
            if not merged_config.has_section(section):
                merged_config.add_section(section)
            for option, value in config_parser.items(section):
                merged_config.set(section, option, value)
    return merged_config

def get_merged_config():
    system_config = read_config_file(SYSTEM_CONFIG_FILE)
    global_config = read_config_file(GLOBAL_CONFIG_FILE)
    local_config = read_config_file(LOCAL_CONFIG_FILE)

    merged_config = merge_configs(system_config, global_config, local_config)

    return merged_config

def cloud_command(args):
    print("Administering Cloud Platform")

def vcs_command(args):
    print("Administering Version Control Systems")

def project_command(args):
    print("Creating a New Project")

def get_configuration(args):
    merged_config = get_merged_config()
    if args.local:
        config = read_config_file(LOCAL_CONFIG_FILE)
    elif args.global_:
        config = read_config_file(GLOBAL_CONFIG_FILE)
    elif args.system:
        config = read_config_file(SYSTEM_CONFIG_FILE)
    else:
        config = merged_config

    if args.key:
        section, key = args.key.split('.')
        if config.has_section(section) and config.has_option(section, key):
            print(config.get(section, key))
        else:
            print(f"Configuration key '{args.key}' not found.")
    else:
        print("Please provide a configuration key using the format 'section.key'.")

def set_configuration(args):
    if args.local:
        config_file = LOCAL_CONFIG_FILE
    elif args.global_:
        config_file = GLOBAL_CONFIG_FILE
    elif args.system:
        config_file = SYSTEM_CONFIG_FILE
    else:
        print("Please specify a configuration source using '--local', '--global', or '--system'.")
        return

    config = read_config_file(config_file)

    if args.key:
        section, key = args.key.split('.')
        if config.has_section(section):
            config.set(section, key, args.value)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
            print(f"Configuration key '{args.key}' set to '{args.value}'.")
        else:
            print(f"Configuration section '{section}' not found.")
    else:
        print("Please provide a configuration key using the format 'section.key'.")

def list_config(args):
    if args.local:
        config = read_config_file(LOCAL_CONFIG_FILE)
    elif args.global_:
        config = read_config_file(GLOBAL_CONFIG_FILE)
    elif args.system:
        config = read_config_file(SYSTEM_CONFIG_FILE)
    else:
        config = get_merged_config()

    for section in config.sections():
        print(f"\n[{section}]")
        for key, value in config.items(section):
            print(f"{key} = {value}")

def main():
    create_global_config_if_not_exists()

    parser = argparse.ArgumentParser(description="py-application-framework command-line tool")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand", help="Available subcommands")

    cloud_parser = subparsers.add_parser("cloud", help="Administer the cloud platform")
    cloud_parser.set_defaults(func=cloud_command)

    vcs_parser = subparsers.add_parser("vcs", help="Administer version control systems")
    vcs_parser.set_defaults(func=vcs_command)

    project_parser = subparsers.add_parser("project", help="Create a new project")
    project_parser.set_defaults(func=project_command)

    config_parser = subparsers.add_parser("configuration", help="Get or set configuration values")
    config_subparsers = config_parser.add_subparsers(title="config_commands", dest="config_command", help="Available config commands")

    get_parser = config_subparsers.add_parser("get", help="Get a configuration value")
    get_parser.add_argument("--local", action="store_true", help="Use local configuration")
    get_parser.add_argument("--global", dest="global_", action="store_true", help="Use global configuration")
    get_parser.add_argument("--system", action="store_true", help="Use system configuration")
    get_parser.add_argument("key", help="Configuration key in the format 'section.key'")
    get_parser.set_defaults(func=get_configuration)

    set_parser = config_subparsers.add_parser("set", help="Set a configuration value")
    set_parser.add_argument("--local", action="store_true", help="Use local configuration")
    set_parser.add_argument("--global", dest="global_", action="store_true", help="Use global configuration")
    set_parser.add_argument("--system", action="store_true", help="Use system configuration")
    set_parser.add_argument("key", help="Configuration key in the format 'section.key'")
    set_parser.add_argument("value", help="New value for the configuration key")
    set_parser.set_defaults(func=set_configuration)

    list_parser = config_subparsers.add_parser("list", help="List configurations")
    list_parser.add_argument("--local", action="store_true", help="List local configurations")
    list_parser.add_argument("--global", dest="global_", action="store_true", help="List global configurations")
    list_parser.add_argument("--system", action="store_true", help="List system configurations")
    list_parser.set_defaults(func=list_config)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
