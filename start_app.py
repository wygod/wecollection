# -*-encoding:utf-8 -*-

from celery_work import main
from collection.we_collection import WeConfigParse

if __name__ == "__main__":

    parse_config_value = WeConfigParse.parse_base_config('device.yaml.yaml')
    device = parse_config_value.device
    for itask in device:
        main(itask)
