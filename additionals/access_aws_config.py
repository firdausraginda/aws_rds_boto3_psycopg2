import argparse
import sys
import json


def access_config():
    """access the config items in aws_config.json"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    args = parser.parse_args()

    if args.config:
        with open(args.config) as config_input:
            config = json.load(config_input)
    else:
        raise
        sys.exit(1)

    return config

def get_config_item(item):
    """retrieve certain config item from aws_config.json"""

    config_items = access_config()

    return config_items[item]