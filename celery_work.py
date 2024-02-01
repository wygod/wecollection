# -*-encoding:utf-8 -*-

from celery import Celery

import uiautomator2.exceptions
from collection.we_collection import *
from common.collectionCommon import InitVenv

broker = 'redis://localhost:6379/1'
backend = 'redis://localhost:6379/2'

app = Celery(
    'celeryDemo',
    broker=broker,
    backend=backend
)


def spider_run(parse_config_value, device_ip):
    try:
        we_run_app = WeCollectionOperator(parse_config_value, device_ip)
        we_run_app.destroy_current_app()
        time.sleep(2)
        we_run_app.start_current_app()
        we_run_app.move_to_button()
        we_run_app.cycle_living_store()
        we_run_app.destroy_current_app()
    except uiautomator2.exceptions.GatewayError as e:
        init_env = InitDeviceApp(parse_config_value, device_ip)
        init_env.check_atx_instrument()
        init_env.start_uiautomator2()
        spider_run(parse_config_value, device_ip)
        print("try restart")
        print(e)


@app.task()
def main(device):
    parse_config_value = WeConfigParse.parse_base_config('config/config.yaml')
    iter_number = 0
    while True:
        try:
            spider_run(parse_config_value, device)
        except uiautomator2.exceptions.UiAutomationNotConnectedError as e:
            init_env = InitVenv(config=parse_config_value, device_serial=device)
            init_env.check_atx_instrument(low=8 if iter_number < 8 else iter_number)
            if init_env.ui_device.uiautomator.running():
                iter_number = 0
                print('restart atx successful')
            print(e)