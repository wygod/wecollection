# -*-encoding:utf-8 -*-
import time

import packaging
from celery import Celery

import uiautomator2
from packaging.version import InvalidVersion

from common.collectionCommon import InitVenv, InitDeviceApp
from collection.we_collection import WeCollectionHandleMain, WeConfigParse


broker = 'redis://localhost:6379/1'
backend = 'redis://localhost:6379/2'

app = Celery(
    'celeryDemo',
    broker=broker,
    backend=backend
)


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
    iter_number = 0
    while True:
        try:
            spider_run(parse_config_value, device)
        except uiautomator2.UiAutomationNotConnectedError as e:
            init_env = InitVenv(config=parse_config_value, device_serial=device)
            init_env.check_atx_instrument(low=8 if iter_number < 8 else iter_number)
            if init_env.ui_device.uiautomator.running():
                iter_number = 0
                print('restart atx successful')
            print(e)