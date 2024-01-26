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
            # 可以添加獲取數據退
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

    def handle_live_store_photo_info(self, element):
        data = '沒有發現認證信息'
        if self.ui_device(resourceId=element).exists:  # NameCollectionENum.ifz.value
            p = self.ui_device(resourceId=element).screenshot()
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
                           'store_verify': self.handle_live_store_photo_info(NameCollectionENum.fxd.value),
                           'store_live_feature': self.handler_all_timeing_live_info(),
                           'store_photo': self.handle_live_store_photo_info(NameCollectionENum.fxf.value)
                           }

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

    @staticmethod
    def handler_atom_info(content, per_element):
        for j in per_element:
            content.append(j.get('text'))
        content.append(" ".join(content))

    def handler_receive_verify_info(self, element):

        content = []
        for per_element in self.ui_device.xpath(element).all():
            per_element_object = per_element.elem.getchildren()
            if per_element_object:
                content_temp = []
                for per_text in per_element_object:
                    temp = []
                    WeCollectionHandleMain.handler_recursion_text(per_text, temp)
                    if temp:
                        content_temp.append(" ".join(temp))
                content.append(content_temp)
            content.append(per_element.elem.get('text'))

        return content

    def handler_photo_product_info(self, elem):
        content = {}
        content_list = self.ui_device.xpath(elem).all()
        for temp in content_list:
            temp.screenshot().save('bg.jpg')
            temp_index = temp.elem.getchildren()
            index = temp_index[1].get('text')
            with open('bg.jpg', "rb") as b:
                data = base64.b64encode(b.read())
            content[index] = data
        return content

    @staticmethod
    def handler_recursion_text(elem, result):
        if elem.getchildren():
            for k in elem.getchildren():
                WeCollectionHandleMain.handler_recursion_text(k, result)
        else:
            temp_text = elem.get('text')
            if temp_text != '':
                result.append(temp_text)

    def handler_all_timeing_live_info(self):
        if self.ui_device(resourceId=NameCollectionENum.fe7.value).exists:
            self.ui_device(resourceId=NameCollectionENum.fe7.value).click()
            timeing_task = self.handler_receive_verify_info(NameCollectionENum.kp2_xpath.value)
            self.ui_device(resourceId=NameCollectionENum.h64.value).click()
            return " ".join(timeing_task)
        else:
            fe5_text = self.handler_receive_verify_info(NameCollectionENum.fe5.value)
            return " ".join(fe5_text)

    @staticmethod
    def handler_keep_data_complete(arg):
        flag = False
        flag_price_status = False
        if type(arg) is list and len(arg) != 0:
            try:
                int(arg[0].split(" ")[0])
                flag = True
            except Exception as e:
                flag = False
                print(e)
            if '￥' in arg[-1] or '$' in arg[-1] or '价' in arg[-1]:
                flag_price_status = True

        return True if flag and flag_price_status else False

    def handler_live_product_info(self):
        last_product = 1
        store_status = True
        store_info_base = {}
        collection_result = []
        stop_cycle_condition = True
        if True:#self.ui_device(resourceId=NameCollectionENum.fl9.value).exists:
            # self.ui_device(resourceId=NameCollectionENum.fl9.value).click()

            while stop_cycle_condition:

                index_max = self.handler_receive_verify_info(NameCollectionENum.l7n_xpath.value)

                if last_product == int(max(index_max)):
                    stop_cycle_condition = False
                else:
                    text_price_content = self.handler_receive_verify_info(NameCollectionENum.fll_xpath.value)

                    text_keep_complete = filter(lambda x: WeCollectionHandleMain.handler_keep_data_complete(x),
                                                text_price_content)

                    photo_content = self.handler_photo_product_info(NameCollectionENum.huu_xpath.value)

                    for index_value in text_keep_complete:

                        collection_result.append({
                            "store_product": index_value[1],
                            "store_price": index_value[-1],
                            "store_photo": photo_content[index_value[0].split(" ")[0]]
                        })

                if store_status:
                    store_info_base["store_id"] = self.get_sub_title(NameCollectionENum.mui.value)
                    store_info_base["store_point"] = self.get_sub_title(NameCollectionENum.mug.value)
                    store_status = False

                self.ui_device.swipe(int(self.screen[0] * 0.5), int(self.screen[1] * 0.95), int(self.screen[0] * 0.5),
                                     int(self.screen[1] * 0.35), duration=0.1)

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
        we_collection_store_product.store_photo = store_info_base['store_photo']
        we_collection_store_product.store_live_feature = store_info_base['store_live_feature']
        we_collection_store_product.store_class = store_class
        we_collection_store_product.store_verify = store_base_information['store_verify']
        we_collection_store_product.store_update_date = datetime.datetime.now()
        self.insert_data_to_database(we_collection_store_product)

    def handle_we_collection_shop_database(self, store_base_information, store_live_product_information):
        result = []
        for meta_value in store_live_product_information:
            we_collection_shop_product = WeCollectionShopProduct()
            we_collection_shop_product.we_chat_shop_name = store_base_information['store_name']
            we_collection_shop_product.shop_product_description = meta_value['store_product']
            we_collection_shop_product.shop_sale_price = meta_value['store_price']
            we_collection_shop_product.shop_product_photo = meta_value['store_photo']
            we_collection_shop_product.product_update_date = datetime.datetime.now()
        self.insert_data_to_database(result)

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
        self.handler_live_product_info()
        # self.destroy_current_app()
        # self.start_current_app()
        # self.move_to_button()

    def cycle_living_store(self):
        for per_nuw_key, per_nuw_value in self.elements_value.items():
            for per_value in per_nuw_value:
                if per_nuw_key != per_value:
                    self.move_to_main_page(per_nuw_key, per_value)
                else:
                    self.move_to_main_page(per_nuw_key, None, False)
