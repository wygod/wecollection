# -*- encoding:utf-8 -*-
import time

import redis

from . import *


class WeCollectionHandleMain(InitDeviceApp, InitDatabaseOperation, CollectionLog):

    def __init__(self, config, device_ip, elements_value):
        self.config = config
        self.device_serial = device_ip
        self.elements_value = elements_value
        InitDeviceApp.__init__(self, self.config, self.device_serial)
        InitDatabaseOperation.__init__(self, self.config)
        CollectionLog.__init__(self, self.config.logHandler.log_conf_path)
        self.screen = self.screen_size()
        self.redis_con = redis.StrictRedis(host=self.config.redis_info.host, port=6379, db=0)
        self.last_class = ''

    def check_spider_status(self):
        time.sleep(5)
        try:
            self.start_current_app()
            self.handler_android_err()
            content = self.check_now_activity_status().output
            if NameCollectionENum.we_chat_start_page.value in content:
                print(1)
                self.move_to_button()
                self.move_to_project_main()
                self.iter_to_live()
            elif NameCollectionENum.enter_live_main_activity.value in content:
                print(2)
                self.move_to_project_main()
                self.iter_to_live()
            elif NameCollectionENum.enter_more_live_activity.value in content:
                print(3)
                self.iter_to_live()
            elif NameCollectionENum.enter_live_store_activity.value in content:
                print(4)
                if self.last_class == '':
                    self.move_to_project_main()
                    self.iter_to_live()
                else:
                    self.click_enter_live_page(self.last_class)
            elif NameCollectionENum.enter_store_profile_activity.value in content:
                print(5)
                self.ui_device.swipe(0, int(self.screen[1] * 0.5), int(self.screen[0] * 0.7), int(self.screen[1] * 0.5),
                                     steps=2)
                time.sleep(2)
                self.click_enter_live_page(self.last_class)
            elif NameCollectionENum.enter_store_permission_activity.value in content:
                print(6)
                self.check_spider_status()
            else:
                self.move_to_button()
                self.move_to_live()
                self.iter_to_live()
        except u2.exceptions.GatewayError as e:
            print(e)
            print('start e')
            self.check_atx_instrument()
            self.check_spider_status()

    def handler_cancel_btn(self):
        content = self.check_now_activity_status().output
        if NameCollectionENum.enter_store_permission_activity.value in content:
            self.ui_device(resourceId=NameCollectionENum.mm_alert_cancel_btn.value).click()
            time.sleep(1)

    def handler_cancel_network(self):
        if self.ui_device(resourceId=NameCollectionENum.jlg.value).exists:
            self.ui_device(resourceId=NameCollectionENum.mm_alert_ok_btn.value).click()
            time.sleep(1)

    def handler_android_err(self):
        if self.ui_device(resourceId=NameCollectionENum.a_err_close.value).exists:
            self.ui_device(resourceId=NameCollectionENum.a_err_close.value).click()
            time.sleep(1)
        self.handler_cancel_network()

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
                                 steps=2)

    def iter_to_live(self):
        content = self.check_now_activity_status().output
        if NameCollectionENum.enter_more_live_activity.value in content:
            main_iter_number = 0
            for per_nuw_key, per_nuw_value in self.elements_value.items():
                if main_iter_number > 5:
                    self.ui_device.swipe(int(self.screen[0] * 0.9), int(self.screen[1] * 0.2), 0,
                                         int(self.screen[1] * 0.2),
                                         steps=2)
                    time.sleep(3)
                    self.handler_android_err()
                    main_iter_number = 0
                sub_main_iter_number = 0
                for per_value in per_nuw_value:
                    if sub_main_iter_number > 5:
                        self.ui_device.swipe(int(self.screen[0] * 0.9), int(self.screen[1] * 0.2), 0,
                                             int(self.screen[1] * 0.2),
                                             steps=2)
                        time.sleep(3)
                        self.handler_android_err()
                        sub_main_iter_number = 0
                    if per_nuw_key != per_value:
                        self.last_class = per_nuw_key + ":" + per_value
                        self.move_to_main_page(per_nuw_key, per_value)
                        sub_main_iter_number = sub_main_iter_number + 1
                    else:
                        self.last_class = per_nuw_key
                        self.move_to_main_page(per_nuw_key, None)
                main_iter_number = main_iter_number + 1
        else:
            self.check_spider_status()

    def move_to_main_page(self, text, sub_text):
        self.rotating_logger.info('--{} : {} --'.format(text, sub_text))
        content = self.check_now_activity_status().output
        if NameCollectionENum.enter_more_live_activity.value in content:
            self.handler_android_err()
            try:
                i = 0
                while True:
                    time.sleep(1)
                    if self.ui_device(resourceId=NameCollectionENum.nuw.value, text='{}'.format(text)).exists or i > 10:
                        break
                    i = i + 1
                self.ui_device(resourceId=NameCollectionENum.nuw.value, text='{}'.format(text)).click()
                self.ui_device(resourceId=NameCollectionENum.nqn.value, text="{}".format(sub_text)).click()
                time.sleep(2.0)
                # 進入 推出
                self.handler_android_err()
                self.ui_device(resourceId=NameCollectionENum.k69.value).click()
                time.sleep(1.0)
                self.click_enter_live_page(sub_text)
                time.sleep(1.0)
                self.ui_device(resourceId=NameCollectionENum.igx.value).click_exists()
            except u2.exceptions.UiObjectNotFoundError as e:
                print(e)
                self.check_spider_status()
        else:
            self.check_spider_status()

    def click_enter_live_page(self, store_class):
        store_name = ""
        while True:
            try:
                self.handler_cancel_btn()
                self.handler_android_err()
                content = self.check_now_activity_status().output
                if NameCollectionENum.enter_live_store_activity.value in content:
                    sub_store_name = self.get_sub_title(NameCollectionENum.ify.value)
                    self.rotating_logger.info('--click live page: {} -- {} --'.format(store_class, sub_store_name))
                    if sub_store_name == "" or sub_store_name == store_name:
                        self.rotating_logger.info('--click end page: {} -- {} --'.format(store_class, sub_store_name))
                        break

                    if self.updated_store_data(sub_store_name):
                        self.rotating_logger.info('--click live info: {} -- {} --'.format(store_class, sub_store_name))
                        store_live_active_information = self.handler_live_active_level_info()
                        self.handler_cancel_btn()
                        self.handler_android_err()
                        self.ui_device(resourceId=NameCollectionENum.k3o.value).click()

                        time.sleep(3)
                        self.handler_cancel_btn()
                        self.handler_android_err()
                        self.rotating_logger.info('--enter store info')
                        store_base_information = self.handle_live_store_base_info()
                        self.handler_android_err()
                        store_live_product_information, store_info_base = self.handler_live_product_info()

                        self.rotating_logger.info('--click live info end : {} -- {} --'.format(store_class, sub_store_name))
                        if len(store_base_information) > 0 and len(store_info_base) > 0:
                            self.handle_we_collection_store_database(store_class,
                                                                     store_base_information,
                                                                     store_info_base,
                                                                     store_live_active_information)

                            self.rotating_logger.info('--click live info shop start : {} -- {} --'.format(store_class,
                                                                                                          sub_store_name))
                            self.handle_we_collection_shop_database(store_base_information, store_live_product_information)
                            self.rotating_logger.info(
                                '--click live info shop end : {} -- {} --'.format(store_class, sub_store_name))
                            self.handle_we_collection_status_database(store_base_information)
                            self.rotating_logger.info('--write live info end: {} -- {} --'.format(store_class, sub_store_name))
                    store_name = sub_store_name
                    time.sleep(1)
                    self.ui_device.swipe(int(self.screen[0] * 0.5), int(self.screen[1] * 0.7), int(self.screen[0] * 0.5),
                                         int(self.screen[1] * 0.15), steps=2)
                    print('start screen next store')
                else:
                    self.check_spider_status()
            except u2.exceptions.GatewayError as e:
                print(e)
                self.check_atx_instrument()
                time.sleep(1)
                self.check_spider_status()
            except u2.exceptions.UiObjectNotFoundError as e:
                print(e)
                self.check_spider_status()

    def updated_store_data(self, store_name):
        if not self.redis_con.get('chat_up_key'):
            self.redis_con.set('chat_up_key', 1, 24*60*60)
            update_data = self.session.query(CheckCollectionStatus).filter_by(
                finder_store_name='{}'.format(store_name)).first()

            if update_data:
                delta = datetime.datetime.now() - datetime.datetime.strptime(
                    update_data.finder_id_update_date.strftime('%Y-%m-%d %H:%M:%S'),
                    '%Y-%m-%d %H:%M:%S')
                return True if delta.days >= 1 else False
            else:
                return True
        else:
            return False

    def handle_live_store_photo_info(self, element):
        data = '沒有發現認證信息'
        if self.ui_device(resourceId=element).exists:
            p = self.ui_device(resourceId=element).screenshot()
            p.save('tmp.jpg')
            with open('tmp.jpg', "rb") as b:
                data = base64.b64encode(b.read())
        return data

    def get_sub_title(self, text):
        self.handler_cancel_btn()
        return self.ui_device(resourceId=text).get_text() if self.ui_device(resourceId=text).exists else "0x00"

    def handle_live_store_base_info(self):
        time.sleep(3)
        self.handler_cancel_btn()
        self.handler_android_err()
        store_base_info = {}
        content = self.check_now_activity_status().output

        if NameCollectionENum.enter_store_profile_activity.value in content:

            store_base_info = {'store_name': self.get_sub_title(NameCollectionENum.fzn.value),
                               'store_province_city': self.get_sub_title(NameCollectionENum.ov9.value),
                               'video_name': self.get_sub_title(NameCollectionENum.g06.value),
                               'store_verify': self.handle_live_store_photo_info(NameCollectionENum.fxd.value),
                               'store_live_feature': self.handler_all_timeing_live_info(),
                               'store_photo': self.handle_live_store_photo_info(NameCollectionENum.fxf.value)
                               }
            self.rotating_logger.info('--enter store base info')
            if self.ui_device(resourceId=NameCollectionENum.jqi.value).exists:
                self.ui_device(resourceId=NameCollectionENum.jqi.value).click()
                time.sleep(1)
                self.handler_android_err()
                if self.ui_device(resourceId=NameCollectionENum.obc.value, text="更多信息").exists:
                    self.ui_device(resourceId=NameCollectionENum.obc.value, text="更多信息").click()
                    time.sleep(1)
                    self.handler_android_err()
                    if self.ui_device(resourceId=NameCollectionENum.cu2.value).exists:
                        store_base_info['finder_id'] = self.get_sub_title(NameCollectionENum.cu2.value)
                        self.rotating_logger.info(
                            '--enter store base info === : {}'.format(store_base_info['finder_id']))
                        time.sleep(2)
                        self.ui_device.swipe(0, int(self.screen[1] * 0.5), int(self.screen[0] * 0.7),
                                             int(self.screen[1] * 0.5),
                                             steps=2)
        time.sleep(2)
        self.ui_device.swipe(0, int(self.screen[1] * 0.5), int(self.screen[0] * 0.7), int(self.screen[1] * 0.5),
                             steps=2)
        return store_base_info

    def handler_live_active_level_info(self):
        store_active = {'store_look_hot_class': self.get_sub_title(NameCollectionENum.i94.value),
                        'store_like_class': self.get_sub_title(NameCollectionENum.f6i.value)}
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
                    if temp and temp != '':
                        content_temp.append(" ".join(temp))
                if content_temp:
                    content.append(content_temp)
            else:
                content.append(per_element.elem.get('text'))

        return content

    def handler_photo_product_info(self, elem, have_dict, have_temp_dict):
        content = {}
        content_list = self.ui_device.xpath(elem).all()
        for temp in content_list:
            temp.screenshot().save('bg.jpg')
            temp_index = temp.elem.getchildren()
            if len(temp_index) >= 2:
                index = temp_index[1].get('text')
                with open('bg.jpg', "rb") as b:
                    data = base64.b64encode(b.read())
                if index not in have_dict.keys():
                    content[index] = data
                    have_temp_dict[index] = '1'
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
        time.sleep(3)
        if self.ui_device(resourceId=NameCollectionENum.fe7.value).exists:
            self.ui_device(resourceId=NameCollectionENum.fe7.value).click()
            time.sleep(2)
            number_contain_txt = self.get_sub_title(NameCollectionENum.fe9.value)
            live_number = re.findall(r'\d+', number_contain_txt) if number_contain_txt != '' else []
            num_live = math.ceil(int(live_number[0]) / 6) if live_number else 1
            timeing_task_list = []
            for _ in range(num_live):
                timeing_task = self.handler_receive_verify_info(NameCollectionENum.kp2_xpath.value)
                if timeing_task:
                    timeing_task_list.extend(timeing_task)
                self.ui_device.swipe(int(self.screen[0] * 0.5), int(self.screen[1] * 0.92),
                                     int(self.screen[0] * 0.5), int(self.screen[1] * 0.45))
            # time.sleep(2)
            self.ui_device(resourceId=NameCollectionENum.h64.value).click()
            return "\n".join(set([" ".join(iter_text) for iter_text in timeing_task_list]))
        else:
            fe5_text = self.handler_receive_verify_info(NameCollectionENum.fe5.value)
            return "\n".join([" ".join(iter_text) for iter_text in fe5_text])

    @staticmethod
    def handler_keep_data_complete(arg, verify_dict):
        result_content = []
        if type(arg) is list and len(arg) != 0:
            for j in arg:
                temp_key_all = 0
                flag_price_status = False
                if type(j) is list and len(j) != 0:
                    print('---j -----: {}'.format(j))
                    try:
                        # number = re.findall('\d+', j[0])
                        temp_key_all = int(j[0].split(" ")[0])
                        flag = True
                    except Exception as e:
                        flag = False
                        print(e)
                    if '￥' in j[-1] or '$' in j[-1] or '价' in j[-1] or '¥' in j[-1]:
                        flag_price_status = True

                    if flag and flag_price_status:
                        verify_dict[str(temp_key_all)] = '1'
                        result_content.append(j)
        return result_content

    def handler_live_product_info(self):
        last_product = 1
        have_dict = {}
        store_status = True
        store_info_base = {}
        collection_result = []
        stop_cycle_condition = True

        self.processing_sleep(NameCollectionENum.enter_live_store_activity.value)

        content = self.check_now_activity_status().output
        if NameCollectionENum.enter_live_store_activity.value in content:
            self.handler_cancel_btn()
            if self.ui_device(resourceId=NameCollectionENum.fl9.value).exists:
                self.ui_device(resourceId=NameCollectionENum.fl9.value).click()
                print("start sleep 3")

            time.sleep(3)
            self.handler_cancel_btn()
            self.rotating_logger.info("iter store info")
            i = 0
            while stop_cycle_condition:
                self.handler_android_err()
                index_max = self.handler_receive_verify_info(NameCollectionENum.l7n_xpath.value)
                print("{} iter....".format(i))
                print(index_max)
                i = i + 1
                if not index_max or last_product == int(max(index_max)):
                    stop_cycle_condition = False
                    self.rotating_logger.info("iter store info end")
                else:
                    filter_dict = {}
                    have_temp_dict = {}
                    self.rotating_logger.info("iter store info writing")
                    text_price_content = self.handler_receive_verify_info(NameCollectionENum.fll_xpath.value)

                    text_keep_complete = WeCollectionHandleMain.handler_keep_data_complete(text_price_content,
                                                                                           filter_dict)

                    photo_content = self.handler_photo_product_info(NameCollectionENum.huu_xpath.value, have_dict,
                                                                    have_temp_dict)
                    print(photo_content)
                    for index_value in text_keep_complete:
                        temp = {
                            "shop_product_description": index_value[1],
                            "shop_sale_price": index_value[-1]
                        }

                        key = index_value[0].split(" ")[0] if " " in index_value[0] else index_value[0]
                        if key in photo_content.keys():
                            temp["shop_product_photo"] = str(photo_content[key])
                        else:
                            temp["shop_product_photo"] = ""

                        collection_result.append(temp)

                    for key_f, value in have_temp_dict.items():
                        if key_f in filter_dict.keys():
                            have_dict[key_f] = value

                    if store_status:
                        store_info_base["store_name"] = self.get_sub_title(NameCollectionENum.mui.value)
                        self.rotating_logger.info("iter store info writing {}".format(store_info_base["store_name"]))
                        point = self.handler_receive_verify_info(NameCollectionENum.mub.value)
                        store_info_base["store_point"] = " ".join(point[0]) if point else '0x00'
                        store_status = False

                    last_product = int(max(index_max)) if index_max else 1

                    self.ui_device.swipe(int(self.screen[0] * 0.5), int(self.screen[1] * 0.95),
                                         int(self.screen[0] * 0.5),
                                         int(self.screen[1] * 0.35), steps=2)
                    # time.sleep(2)

            self.ui_device.swipe(int(self.screen[0] * 0.5), int(self.screen[1] * 0.22),
                                 int(self.screen[0] * 0.5), int(self.screen[1]),
                                 steps=2)

        return collection_result, store_info_base

    def handle_we_collection_store_database(self, store_class, store_base_information,
                                            store_info_base, store_live_active_information):
        if 'finder_id' in store_base_information.keys():
            try:
                store_id = self.session.query(WeCollectionBaseInfo).filter_by(
                    finder_id='{}'.format(store_base_information['finder_id'])).first()
                if not store_id:
                    we_collection_store_product = WeCollectionBaseInfo()
                    we_collection_store_product.finder_id = store_base_information.get('finder_id', '无')
                    we_collection_store_product.video_name = store_base_information.get('store_name', '无')
                    we_collection_store_product.store_name = store_base_information.get('store_name', '无')
                    we_collection_store_product.store_province_city = store_base_information.get('store_province_city',
                                                                                                 '无')
                    we_collection_store_product.store_point = store_info_base.get('store_point', '无')
                    we_collection_store_product.store_look_hot_class = store_live_active_information.get(
                        'store_look_hot_class', '无')
                    we_collection_store_product.store_like_class = store_live_active_information.get('store_like_class',
                                                                                                     '无')
                    we_collection_store_product.store_photo = store_base_information.get('store_photo', '无')
                    we_collection_store_product.store_live_feature = store_base_information.get('store_live_feature',
                                                                                                '无')
                    we_collection_store_product.store_class = store_class
                    we_collection_store_product.store_verify = store_base_information.get('store_verify', '无认证')
                    we_collection_store_product.store_update_date = datetime.datetime.now()
                    self.insert_data_to_database(we_collection_store_product)
                    self.rotating_logger.info("writing database {}".format(store_base_information['finder_id']))
                else:
                    self.session.query(WeCollectionBaseInfo).filter_by(
                        finder_id='{}'.format(store_base_information['finder_id'])).update(
                        {'store_point': store_info_base.get('store_point', '暂无评分'),
                         'store_look_hot_class': store_live_active_information.get('store_look_hot_class', '0'),
                         'store_like_class': store_live_active_information.get('store_like_class', '0'),
                         'store_live_feature': store_base_information.get('store_live_feature', '0')})
                    self.session.commit()
            except Exception as e:
                print(e)

    def handle_we_collection_shop_database(self, store_base_information, store_live_product_information):
        if 'store_name' in store_base_information.keys():
            result = []
            for meta_value in store_live_product_information:
                try:
                    we_collection_shop_product = WeCollectionShopProduct()
                    we_collection_shop_product.we_chat_shop_name = store_base_information.get('store_name', '0')
                    we_collection_shop_product.shop_product_description = meta_value.get('shop_product_description',
                                                                                         '0')
                    we_collection_shop_product.shop_sale_price = meta_value.get('shop_sale_price', '0')
                    we_collection_shop_product.shop_product_photo = meta_value.get('shop_product_photo', '0')
                    we_collection_shop_product.product_update_date = datetime.datetime.now()
                    result.append(we_collection_shop_product)
                except Exception as e:
                    print(e)
            self.insert_data_to_database(result)

    def handle_we_collection_status_database(self, store_base_information):
        if 'finder_id' in store_base_information.keys():
            try:
                store_id = self.session.query(CheckCollectionStatus).filter_by(
                    finder_id='{}'.format(store_base_information['finder_id'])).first()
                if not store_id:
                    we_collection_status = CheckCollectionStatus()
                    we_collection_status.finder_id = store_base_information["finder_id"]
                    we_collection_status.finder_store_name = store_base_information["store_name"]
                    we_collection_status.finder_id_status = 1
                    we_collection_status.finder_id_update_date = datetime.datetime.now()
                    self.insert_data_to_database(we_collection_status)
                else:
                    self.session.query(CheckCollectionStatus).filter_by(
                        finder_id='{}'.format(store_base_information['finder_id'])).update(
                        {
                            "finder_id_update_date": datetime.datetime.now()
                        }
                    )
                    self.session.commit()
            except Exception as e:
                print(e)

    def add_store(self, store_base_information):
        store_id = self.session.query(WeChatLive).filter_by(
            finder_id='{}'.format(store_base_information['finder_id'])).first()
        if not store_id:
            we_chat_live = WeChatLive()
            we_chat_live.finder_id = store_base_information['finder_id']
            we_chat_live.finder_store_name = store_base_information['store_name']
            we_chat_live.finder_id_update_date = datetime.datetime.now()
            self.insert_data_to_database(we_chat_live)


class WeConfigParse:
    def __init__(self):
        pass

    @staticmethod
    def parse_base_config(config_path):
        return OmegaConf.load(config_path)
