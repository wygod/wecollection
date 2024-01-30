# -*-encoding:utf-8 -*-

from pgDataBase import Base
from CollectionEnum.collectionEnum import NameCollectionENum
from collection.we_collection import *


def main():
    device_ip = '192.168.1.101:5555'#4HDVB22531019407'

    we_run_app = WeCollectionOperator(device_ip)
    we_run_app.cycle_living_store()
    we_run_app.destroy_current_app()


if __name__ == "__main__":
    main()
