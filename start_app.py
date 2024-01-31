# -*-encoding:utf-8 -*-
import packaging.version
import uiautomator2.exceptions

from collection.we_collection import *
from common.collectionCommon import InitVenv


def spider_run(parse_config_value, device_ip):
    we_run_app = WeCollectionOperator(parse_config_value, device_ip)
    try:
        we_run_app.destroy_current_app()
        time.sleep(2)
        we_run_app.start_current_app()
        we_run_app.move_to_button()
        we_run_app.cycle_living_store()
        we_run_app.destroy_current_app()
    except uiautomator2.exceptions.GatewayError as e:
        we_run_app.start_uiautomator2()
        we_run_app.check_spider_status()
        print(e)


def main():
    device_ip = 'TPG5T17C20018164'
    parse_config_value = WeConfigParse.parse_base_config('config/config.yaml')
    iter_number = 0
    while True:
        try:
            spider_run(parse_config_value, device_ip)
        except uiautomator2.exceptions.UiAutomationNotConnectedError as e:
            init_env = InitVenv(config=parse_config_value, device_serial=device_ip)
            init_env.check_atx_instrument(low=8 if iter_number < 8 else iter_number)
            if init_env.ui_device.uiautomator.running():
                iter_number = 0
                print('restart atx successful')


if __name__ == "__main__":
    main()
