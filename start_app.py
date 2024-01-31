# -*-encoding:utf-8 -*-

from celery_work import main, spider_run
from collection.we_collection import WeConfigParse

if __name__ == "__main__":

    parse_config_value = WeConfigParse.parse_base_config('device.yaml')
    parse_config_value_conf = WeConfigParse.parse_base_config('config/config.yaml')
    device = parse_config_value.device
    spider_run(parse_config_value_conf, device[0])
    # for itask in device:
    #     main(itask)
