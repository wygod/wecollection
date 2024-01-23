# -*- encoding:utf-8 -*-
import datetime
import time
import base64
from omegaconf import OmegaConf

from common.collectionCommon import InitDeviceApp
from pgDataBase.databaseInit import InitDatabaseOperation
from CollectionEnum.collectionEnum import NameCollectionENum
from pgDataBase.weInitChatMain import WeCollectionShopProduct, WeCollectionBaseInfo, CheckCollectionStatus
from collectionException.collectionSelfDefineException import CollectionElementNotFoundException


class WeCollectionHandleMain(InitDeviceApp, InitDatabaseOperation):

    def __init__(self, config, device_ip):
        InitDeviceApp.__init__(self, config, device_ip)
        InitDatabaseOperation.__init__(self, config)
        self.screen = InitDeviceApp.screen_size(self)

    def check_now_activity_status(self):
        activity_content = InitDeviceApp.adb_client(self).shell('dumpsys activity top | grep ACTIVITY')

    def search_key_word_page(self, text):

        if self.ui_device(resourceId=NameCollectionENum.b1i.value).exists:
            self.ui_device(resourceId=NameCollectionENum.b1i.value).click()
            self.ui_device.xpath("//android.widget.EditText").set_text(text)
            self.ui_device.xpath('//*[@content-desc="搜索"]').click()
            self.ui_device.xpath('//*[@content-desc="{}"]'.format(text)).click()
            # 可以添加獲取數據
            # 退
            self.ui_device(resourceId=NameCollectionENum.aa4.value).click()

            self.ui_device.swipe(int(self.screen[0] * 0.1), int(self.screen[1] * 0.5),
                              int(self.screen[0]), int(self.screen[1] * 0.5),
                              duration=0.5)

    def move_to_main_page(self, text, sub_text, sub_text_is_use=True):
        if self.ui_device(resourceId=NameCollectionENum.nuw.value, text='{}'.format(text)).exists:
            self.ui_device(resourceId=NameCollectionENum.nuw.value, text='{}'.format(text)).click()
            if sub_text_is_use:
                if self.ui_device(resourceId=NameCollectionENum.nqn.value, text='{}'.format(sub_text)).exists:
                    self.ui_device(resourceId=NameCollectionENum.nqn.value, text="{}".format(sub_text)).click()
                    time.sleep(1)
                    if self.ui_device(resourceId=NameCollectionENum.fs4.value).exists:
                        self.ui_device(resourceId=NameCollectionENum.fs4.value).click()
                        self.click_enter_live_page(sub_text)
                        self.ui_device(resourceId=NameCollectionENum.igx.value).click_exists()
                    else:
                        raise CollectionElementNotFoundException('fs4')
                else:
                    raise CollectionElementNotFoundException('nqn')
            else:
                if self.ui_device(resourceId=NameCollectionENum.fs4.value).exists:
                    self.ui_device(resourceId=NameCollectionENum.fs4.value).click()
                    self.click_enter_live_page(text)
                    self.ui_device(resourceId=NameCollectionENum.igx.value).click_exists()
                else:
                    raise CollectionElementNotFoundException('fs4')
        else:
            raise CollectionElementNotFoundException('Num')

    def click_enter_live_page(self, store_class):

        store_name = ""

        while True:
            sub_store_name = self.get_sub_title(NameCollectionENum.ify.value)

            if sub_store_name == "" or sub_store_name == store_name:
                break
            else:
                if self.updated_store_data(sub_store_name):
                    store_live_active_information = self.handler_live_active_level_info()
                    store_base_information = self.handle_live_store_base_info()
                    store_live_product_information, store_info_base = self.handler_live_product_info()
                    self.handle_we_collection_store_database(store_class,
                                                             store_base_information,
                                                             store_info_base,
                                                             store_live_active_information)

                    self.handle_we_collection_status_database(store_base_information)

                store_name = sub_store_name

                self.ui_device.swipe(int(self.screen[0] * 0.5), int(self.screen[1] * 0.6),
                                  int(self.screen[0] * 0.5), int(self.screen[1] * 0.4),
                                  duration=0.5)

    def updated_store_data(self, store_name):

        update_data = self.session.query(CheckCollectionStatus).filter_by(
            finder_store_name='{}'.format(store_name)).first()
        if update_data:
            delta = update_data.finder_id_update_date - datetime.datetime.now()
            return True if delta.day >= 1 else False
        else:
            return True

    def handle_live_store_verify_info(self):
        data = '沒有發現認證信息'
        if self.ui_device(resourceId=NameCollectionENum.ifz.value).exists:
            p = self.ui_device(resourceId=NameCollectionENum.ifz.value).screenshot()
            p.save('tmp.jpg')
            with open('tmp.jpg', "rb") as b:
                data = base64.b64encode(b.read())
        return data

    def check_close_live(self):
        pass

    def get_sub_title(self, text):
        return self.ui_device(resourceId=text).get_text() if self.ui_device(resourceId=text).exists else ""

    def handle_live_store_base_info(self):
        self.ui_device(resourceId=NameCollectionENum.k3o.value).click()

        time.sleep(2)

        if self.ui_device(resourceId=NameCollectionENum.mm_alert_cancel_btn.value).exists:
            self.ui_device(resourceId=NameCollectionENum.mm_alert_cancel_btn.value).click()

        store_base_info = {'store_name': self.get_sub_title(NameCollectionENum.fzn.value),
                           'store_addr': self.get_sub_title(NameCollectionENum.ov9.value),
                           'store_small_name': self.get_sub_title(NameCollectionENum.g06.value),
                           'store_verify': self.handle_live_store_verify_info()}

        if self.ui_device(resourceId=NameCollectionENum.jqi.value).exists:
            self.ui_device(resourceId=NameCollectionENum.jqi.value).click()
            time.sleep(1)
            if self.ui_device(resourceId=NameCollectionENum.obc.value, text="更多信息").exists:
                self.ui_device(resourceId=NameCollectionENum.obc.value, text="更多信息").click()
                time.sleep(1)
                if self.ui_device(resourceId=NameCollectionENum.cu2.value).exists:
                    store_base_info['store_id'] = self.get_sub_title(NameCollectionENum.cu2.value)
            time.sleep(1)
            self.ui_device.swipe(0, int(self.screen[1] * 0.5), int(self.screen[0] * 0.7), int(self.screen[1] * 0.5),
                              duration=0.5)

        self.ui_device.swipe(0, int(self.screen[1] * 0.5), int(self.screen[1] * 0.7), int(self.screen[1] * 0.5),
                          duration=0.1)

        return store_base_info

    def handler_live_active_level_info(self):
        store_active = {'active_number': self.get_sub_title(NameCollectionENum.i94.value),
                        'like_number': self.get_sub_title(NameCollectionENum.f6i.value)}
        return store_active

    def handler_receive_verify_info(self):
        for element in self.ui_device.xpath('//*[@resource-id="com.tencent.mm:id/l77"]').all():
            ch = element.elem.getchildren()
            price = []
            for j in ch:
                price.append(j.get('text'))
            print(price)
        pass

    def handler_live_product_info(self):
        last_product = ""
        store_status = True
        store_info_base = {}
        collection_result = []
        stop_cycle_condition = True
        self.ui_device(resourceId=NameCollectionENum.fl9.value).click()

        while stop_cycle_condition:

            # sub_content = self.ui_device(resourceId=NameCollectionENum.flh.value)
            # for i_content in sub_content:

            store_product = self.get_sub_title(NameCollectionENum.l6m.value)

            if last_product == store_product:
                stop_cycle_condition = False

            last_product = store_product

            dio = self.get_sub_title(NameCollectionENum.dio.value)

            store_product_content = {"store_preferential": dio if dio != "" else "原价",
                                     "store_product": store_product,
                                     "store_price": self.get_sub_title(NameCollectionENum.l7g.value),
                                     "store_real_price": self.get_sub_title(NameCollectionENum.mug.value)
                                     }
            if store_status:
                store_info_base["store_id"] = self.get_sub_title(NameCollectionENum.mui.value)
                store_info_base["store_point"] = self.get_sub_title(NameCollectionENum.mug.value)
                store_status = False

            collection_result.append(store_product_content)

            self.ui_device.swipe(int(self.screen[0] * 0.5), int(self.screen[1] * 0.9), int(self.screen[0] * 0.5),
                              int(self.screen[1] * 0.5), duration=0.5)

        return collection_result, store_info_base

    def handle_we_collection_store_database(self, store_class, store_base_information,
                                            store_info_base, store_live_active_information):

        we_collection_store_product = WeCollectionBaseInfo()
        we_collection_store_product.finder_id = store_base_information['store_id']
        we_collection_store_product.store_name = store_base_information['store_name']
        we_collection_store_product.store_province_city = store_base_information['store_addr']
        we_collection_store_product.store_point = store_info_base['store_point']
        we_collection_store_product.store_look_hot_class = store_live_active_information['active_number']
        we_collection_store_product.store_like_class = store_live_active_information['like_number']
        we_collection_store_product.store_class = store_class
        we_collection_store_product.store_verify = store_base_information['store_verify']
        we_collection_store_product.store_update_date = datetime.datetime.now()
        self.insert_data_to_database(we_collection_store_product)

    def handle_we_collection_shop_database(self, store_base_information, store_live_product_information):

        we_collection_shop_product = WeCollectionShopProduct()
        we_collection_shop_product.we_chat_shop_name = store_base_information['store_name']
        we_collection_shop_product.shop_product_description = store_live_product_information['store_product']
        we_collection_shop_product.shop_sale_price = store_live_product_information['store_price']
        we_collection_shop_product.shop_preferential = store_live_product_information['shop_preferential']
        we_collection_shop_product.product_update_date = datetime.datetime.now()
        self.insert_data_to_database(we_collection_shop_product)

    def handle_we_collection_status_database(self, store_base_information):

        we_collection_status = CheckCollectionStatus()
        we_collection_status.finder_id = store_base_information["store_di"]
        we_collection_status.finder_store_name = store_base_information["store_name"]
        we_collection_status.finder_id_status = 1
        we_collection_status.finder_id_update_date = datetime.datetime.now()
        self.insert_data_to_database(we_collection_status)


class WeConfigParse:
    def __init__(self):
        pass

    @staticmethod
    def parse_base_config(config_path):
        return OmegaConf.load(config_path)


class WeCollectionOperator(WeCollectionHandleMain):
    def __init__(self, device_ip):
        self.parse_config_value = WeConfigParse.parse_base_config('config/config.yaml')
        self.elements_value = WeConfigParse.parse_base_config('config/elements.yaml')
        WeCollectionHandleMain.__init__(self, self.parse_config_value, device_ip)
        self.start_current_app()
        self.move_to_button()

    def cycle_living_store(self):
        for per_nuw_key, per_nuw_value in self.elements_value.items():
            for per_value in per_nuw_value:
                if per_nuw_key != per_value:
                    self.move_to_main_page(per_nuw_key, per_value)
                else:
                    self.move_to_main_page(per_nuw_key, None, False)
