# -*-encoding:utf-8 -*-

import argparse
import celery_work
from collection.we_collection import WeConfigParse

if __name__ == "__main__":

    collection_arg = argparse.ArgumentParser()
    collection_arg.add_argument()
    collection_arg.add_argument(
        "--conf",
        type=str,
        help="adb 相關環境配置文件",
    )
    collection_arg_parse = collection_arg.parse_args()

    parse_config_value_conf = WeConfigParse.parse_base_config(collection_arg_parse.conf)
    device = parse_config_value_conf.device
    for i_device in device:
        celery_work.main.delay(parse_config_value_conf, i_device)
