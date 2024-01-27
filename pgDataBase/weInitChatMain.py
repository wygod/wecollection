# -*- encoding:utf-8 -*-

from pgDataBase import *


class WeCollectionBaseInfo(Base):
    '''
    直播间数据
    '''
    __tablename__ = 'we_collection_store_info'
    id = Column(Integer, comment='we_collection_store_id', primary_key=True, autoincrement=True)
    finder_id = Column(String(length=100), comment='达人id', unique=True, nullable=False)
    video_name = Column(String(length=300), comment='视频号名称', nullable=False)
    store_name = Column(Text, comment='商店名称', nullable=False)
    store_province_city = Column(String(length=100), comment='地址', nullable=True)
    store_point = Column(String(length=100), comment='评分', nullable=True)
    store_look_hot_class = Column(Text, comment='观看人数和热度', nullable=True)
    store_like_class = Column(String(length=20), comment='点赞数', nullable=True)
    store_class = Column(String(length=100), comment='分类', nullable=True)
    store_verify = Column(Text, comment='认证', nullable=True)
    store_photo = Column(Text, comment='頭像', nullable=True)
    store_live_feature = Column(Text, comment='預約時間', nullable=True)
    store_update_date = Column(DATE, comment="更新时间", default=datetime.datetime.now(), nullable=False)


class WeCollectionShopProduct(Base):
    '''
    视频号产品
    '''
    __tablename__ = 'we_collection_shop_info'
    id = Column(Integer, comment='we_collection_store_id', primary_key=True, autoincrement=True)
    we_chat_shop_name = Column(Text, comment='商店名称', nullable=False)
    shop_product_description = Column(Text, comment='商品标题', nullable=False)
    shop_sale_price = Column(Text, comment='商品价格_优惠', nullable=True)
    shop_product_photo = Column(Text, comment='圖片', nullable=True)
    product_update_date = Column(DATE, default=datetime.datetime.now(), comment='商品更新时间', nullable=False)


class CheckCollectionStatus(Base):
    '''
    检查状态表
    '''
    __tablename__ = 'check_we_collection_status'
    id = Column(Integer, comment='we_collection_store_id', primary_key=True, autoincrement=True)
    finder_id = Column(String(length=100), comment='达人id', unique=True, nullable=False)
    finder_store_name = Column(Text, comment='商店名称', nullable=False)
    finder_id_status = Column(Integer, comment='商店检查状态', nullable=False)
    finder_id_update_date = Column(DATE, default=datetime.datetime.now(), comment='商店检查时间', nullable=False)
