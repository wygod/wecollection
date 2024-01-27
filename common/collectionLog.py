# -*- encoding:utf-8 -*-
import os
import logging
from logging import config


class CollectionLog:
    def __init__(self, log_conf):
        self.path = log_conf
        self.rotating_logger = self._log_conf()

    def _log_conf(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding='utf-8') as f:
                logging.config.fileConfig(f)

        rotating_logger = logging.getLogger(name="rotatingFileLogger")
        return rotating_logger
