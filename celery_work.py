# -*-encoding:utf-8 -*-
import time

import packaging
from celery import Celery

import uiautomator2
from packaging.version import InvalidVersion

from common.collectionCommon import InitVenv, InitDeviceApp
from collection.we_collection import WeCollectionHandleMain, WeConfigParse


app = Celery(
    'celeryDemo',
)
app.config_from_object('celery_config')


def spider_run(parse_config_value, device_ip, rec=False):
    try:
        elements_value = WeConfigParse.parse_base_config('config/elements.yaml')
        we_run_app = WeCollectionHandleMain(parse_config_value, device_ip, elements_value)
        if rec:
            we_run_app.destroy_current_app()
        time.sleep(3)
        we_run_app.check_spider_status()
    except (uiautomator2.exceptions.GatewayError, InvalidVersion) as e:
        init_env = InitDeviceApp(parse_config_value, device_ip)
        for _ in range(2):
            init_env.check_atx_instrument()

        init_env.start_uiautomator2()
        spider_run(parse_config_value, device_ip)
        print("GatewayError")
        print(e)
    except RecursionError as e:
        print(e)
        spider_run(parse_config_value, device_ip, rec=True)


@app.task()
def main(device):
    parse_config_value = WeConfigParse.parse_base_config('config/config.yaml')
    while True:
        spider_run(parse_config_value, device)
