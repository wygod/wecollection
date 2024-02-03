# -*-encoding:utf-8 -*-

import argparse

from ppadb.client import Client as adbClient

from celery_work import spider_run
from collection.we_collection import WeConfigParse


def read_device(host, port):
    adb_shell = adbClient(host=host, port=port)
    return [i.serial for i in adb_shell.devices()]


if __name__ == "__main__":

    collection_arg = argparse.ArgumentParser()
    collection_arg.add_argument(
        "--host",
        type=str,
        help="主机 ip",
    )
    collection_arg.add_argument(
        "--port",
        type=int,
        help="adb port",
    )
    collection_arg_parse = collection_arg.parse_args()
    device = read_device(collection_arg_parse.host, collection_arg_parse.port)
    parse_config_value = WeConfigParse.parse_base_config('config/config.yaml')
    spider_run(parse_config_value, device[0])
