# -*- encoding:utf-8 -*-

import re
import math
import time
import redis
import base64
import datetime
import uiautomator2
from omegaconf import OmegaConf

from common.collectionLog import CollectionLog
from common.collectionCommon import InitDeviceApp
from pgDataBase.databaseInit import InitDatabaseOperation
from CollectionEnum.collectionEnum import NameCollectionENum
from collectionException.collectionSelfDefineException import AndroidSysNotException
from pgDataBase.weInitChatMain import WeCollectionShopProduct, WeCollectionBaseInfo, CheckCollectionStatus, WeChatLive


