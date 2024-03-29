# -*- encoding:utf-8 -*-
import random
import time

from packaging.version import InvalidVersion

from . import *


class WeCollectionHandleMain(InitDeviceApp, InitDatabaseOperation, CollectionLog):

    def __init__(self, config, device_ip, elements_value):
        """
        :param config: 包含环境配置文件
        :param device_ip: 设备识别码
        :param elements_value:分类
        """
        self.config = config
        self.device_serial = device_ip
        self.elements_value = elements_value
        InitDeviceApp.__init__(self, self.config, self.device_serial)
        InitDatabaseOperation.__init__(self, self.config)
        CollectionLog.__init__(self, self.config.logHandler.log_conf_path)
        self.screen = self.screen_size()
        self.redis_con = redis.StrictRedis(host=self.config.redis_info.host, port=6379, db=0)
        self.last_class = ''
        self.store_count = 1
        self.iter_to_live_number = 1
        self.invalid_count = 1

    def check_spider_status(self, iter_status=False):
        """
        处理异常和重启函数
        :return:
        """

        self.rotating_logger.info("check_spider_status: starting")
        try:
            self.start_current_app()
            self.handler_android_err()
            self.handler_setting_page()
            content = self.check_now_activity_status().output
            if NameCollectionENum.we_chat_start_page.value in content:
                if self.ui_device(resourceId=NameCollectionENum.a4p.value).exists:
                    self.ui_device(resourceId=NameCollectionENum.a4p.value).click()
                    time.sleep(1)
                self.rotating_logger.info("activity: wechat 首页")
                self.move_to_button()
                self.move_to_project_main()
                self.iter_to_live(iter_status)
            elif NameCollectionENum.enter_live_main_activity.value in content:
                self.rotating_logger.info("activity: wechat 直播列表页")
                self.move_to_project_main()
                self.iter_to_live(iter_status)
            elif NameCollectionENum.enter_more_live_activity.value in content:
                self.rotating_logger.info("activity: wechat 直播列表详情页")
                self.iter_to_live(iter_status)
            elif NameCollectionENum.enter_live_store_activity.value in content:
                if self.last_class == '':
                    self.rotating_logger.info("activity: wechat 直播列表页， 没有分类")
                    self.move_to_project_main()
                    self.iter_to_live(iter_status)
                else:
                    self.rotating_logger.info("activity: wechat 直播列表页， 有分类")
                    if iter_status:
                        self.click_enter_live_page(self.last_class)
                    else:
                        self.move_to_main_class_page(self.last_class)
            elif NameCollectionENum.enter_store_profile_activity.value in content:
                self.ui_device.swipe(0, int(self.screen[1] * 0.5), int(self.screen[0] * 0.7), int(self.screen[1] * 0.5),
                                     steps=2)
                time.sleep(2)
                self.rotating_logger.info("activity: wechat 直播基本信息页")
                if iter_status:
                    self.click_enter_live_page(self.last_class)
                else:
                    self.move_to_main_class_page(self.last_class)
            elif NameCollectionENum.enter_store_permission_activity.value in content:
                self.rotating_logger.info("activity: wechat 直播列表页 授权页")
                self.check_spider_status(iter_status=iter_status)
            elif NameCollectionENum.setting.value in content:
                self.rotating_logger.info("activity: android 权限设置")
                time.sleep(2)
                self.ui_device.xpath('//*[@content-desc="向上导航"]').click()
                time.sleep(2)
                self.check_spider_status(iter_status=iter_status)
            else:
                self.rotating_logger.info("activity: wechat starting")
                self.move_to_button()
                self.move_to_live()
                self.iter_to_live(iter_status)
        except (uiautomator2.exceptions.GatewayError, InvalidVersion) as e:
            self.rotating_logger.info("exception : wechat restarting {}".format(e))
            if self.invalid_count > 3:
                self.destroy_current_app()
                self.invalid_count = 0
                time.sleep(1)
            self.invalid_count = self.invalid_count + 1

            for _ in range(2):
                self.check_atx_instrument()

            self.start_uiautomator2()
            self.check_spider_status(iter_status=iter_status)

    def handler_cancel_btn(self):
        """
        处理出现权限异常
        :return:
        """
        content = self.check_now_activity_status().output
        if NameCollectionENum.enter_store_permission_activity.value in content:
            self.ui_device(resourceId=NameCollectionENum.mm_alert_cancel_btn.value).click()
            time.sleep(1)

    def handler_cancel(self, value):
        if self.ui_device(resourceId=value).exists:
            self.ui_device(resourceId=value).click()
            time.sleep(1)

    def handler_cancel_network(self):
        """
        处理网络异常
        :return:
        """
        if self.ui_device(resourceId=NameCollectionENum.jlg.value).exists:
            self.ui_device(resourceId=NameCollectionENum.mm_alert_ok_btn.value).click()
            time.sleep(1)

    def handler_android_err(self):
        """
        处理系统异常
        :return:
        """

        self.handler_cancel(NameCollectionENum.a_err_close.value)

        self.handler_cancel_network()

        self.handler_cancel(NameCollectionENum.bz2.value)

    def handler_setting_page(self):
        """
        处理进入权限设置
        :return:
        """
        if self.ui_device(resourceId=NameCollectionENum.action_bar_title.value, text='显示在其他应用的上层').exists:
            self.ui_device.xpath('//*[@content-desc="向上导航"]').click()
            time.sleep(2)

    def search_key_word_page(self, text):
        """
        搜索页面
        :param text: 直播间名
        :return:
        """
        if self.ui_device(resourceId=NameCollectionENum.b1i.value).exists:
            self.ui_device(resourceId=NameCollectionENum.b1i.value).click()
            self.ui_device.xpath("//android.widget.EditText").set_text(text)
            self.ui_device.xpath('//*[@content-desc="搜索"]').click()
            self.ui_device.xpath('//*[@content-desc="{}"]'.format(text)).click()
            self.ui_device(resourceId=NameCollectionENum.aa4.value).click()

            self.ui_device.swipe(int(self.screen[0] * 0.1), int(self.screen[1] * 0.5),
                                 int(self.screen[0]), int(self.screen[1] * 0.5),
                                 steps=2)

            self.handle_live_store_base_info()

    def iter_to_live(self, iter_status):
        """
        搜集各种类型直播间
        :return:
        """
        self.rotating_logger.info("start function iter to live")
        content = self.check_now_activity_status().output
        if NameCollectionENum.enter_more_live_activity.value in content:
            main_iter_number = 0
            for per_nuw_key, per_nuw_value in self.elements_value.items():
                if main_iter_number > 5:
                    self.ui_device.swipe(int(self.screen[0] * 0.9), int(self.screen[1] * 0.2), 0,
                                         int(self.screen[1] * 0.2),
                                         steps=2)
                    time.sleep(1)
                    self.handler_android_err()
                    main_iter_number = 0
                sub_main_iter_number = 0
                for per_value in per_nuw_value:
                    if self.store_count > 3:
                        self.destroy_current_app()
                        time.sleep(3)
                        self.store_count = 0
                        self.check_spider_status()
                    if sub_main_iter_number > 5:
                        self.ui_device.swipe(int(self.screen[0] * 0.9), int(self.screen[1] * 0.2), 0,
                                             int(self.screen[1] * 0.2),
                                             steps=2)
                        time.sleep(1)
                        self.handler_android_err()
                        sub_main_iter_number = 0
                    if per_nuw_key != per_value:
                        self.last_class = per_nuw_key + ":" + per_value
                        self.rotating_logger.info(f"start {self.last_class}")
                        # 从主页刷新
                        if iter_status:
                            self.move_to_main_page(per_nuw_key, per_value)
                        else:
                            self.scroll_main_page(per_nuw_key, per_value)
                        # 从直播间刷新
                        #
                        sub_main_iter_number = sub_main_iter_number + 1
                    else:
                        self.last_class = per_nuw_key
                        self.rotating_logger.info(f"start {self.last_class}")
                        if iter_status:
                            self.move_to_main_page(per_nuw_key, None)
                        else:
                            self.scroll_main_page(per_nuw_key, None)
                main_iter_number = main_iter_number + 1
        else:
            self.rotating_logger.info("restart into live")
            if self.iter_to_live_number >= 3:
                self.destroy_current_app()
                self.iter_to_live_number = 0
                time.sleep(1)
            self.iter_to_live_number = self.iter_to_live_number + 1
            self.check_spider_status(iter_status=iter_status)

    def scroll_main_page(self, text, sub_text):
        content = self.check_now_activity_status().output
        if NameCollectionENum.enter_more_live_activity.value in content:
            self.handler_android_err()
            try:
                # self.processing_sleep(NameCollectionENum.nuw.value, 5)
                self.ui_device(resourceId=NameCollectionENum.nuw.value, text='{}'.format(text)).click()
                if sub_text:
                    self.ui_device(resourceId=NameCollectionENum.nqn.value, text="{}".format(sub_text)).click()
                # time.sleep(2.0)
                self.handler_android_err()
                self.rotating_logger.info('开始获取直播间信息 ---: {} : {}'.format(text, sub_text))
                load_number = 1
                load_status = False
                sleep_number = 1
                stop_condition = 0
                main_iter_number = 1
                last_collection = []
                while True:
                    if stop_condition > 3:
                        break
                    if sleep_number >= 3:
                        self.ui_device.swipe_ext('right', scale=0.7)
                        # time.sleep(3)
                        self.ui_device(resourceId=NameCollectionENum.b1h.value).click()
                        time.sleep(1)
                        print("没有加载到数据， 正在睡眠等着")
                        sleep_number = 1

                    if self.ui_device(resourceId=NameCollectionENum.fuv.value).exists:
                        if load_number >= 3:
                            print("出现加载，正在休息， 加载其他数据")
                            self.ui_device.swipe_ext('right', scale=0.9)
                            # time.sleep(2)
                            random_number = round(random.random())
                            if random_number:
                                for _ in range(random.randint(4, 6)):
                                    # time.sleep(1)
                                    self.ui_device.swipe_ext('up', scale=0.6)
                                self.move_to_project_main()
                            else:
                                self.ui_device(resourceId=NameCollectionENum.k69.value).click()
                                # time.sleep(1)
                                for _ in range(random.randint(3, 6)):
                                    time.sleep(1)
                                    self.ui_device.swipe_ext('up', scale=0.6)
                                # time.sleep(1)
                                self.ui_device(resourceId=NameCollectionENum.igx.value).click()
                                self.move_to_project_main()
                            # time.sleep(2.0)
                            load_number = 1
                            load_status = True
                            stop_condition = stop_condition + 1
                        # time.sleep(1)

                        if load_status:
                            self.ui_device.drag(int(self.screen[0] * 0.5), int(self.screen[1] * 0.85),
                                                int(self.screen[0] * 0.5),
                                                int(self.screen[1] * 0.25), duration=0.2)
                            # time.sleep(2.0)
                            load_status = False

                        if self.ui_device(resourceId=NameCollectionENum.ili.value,
                                          text='正在加载...').exists:
                            print("正在加载")
                            load_number = load_number + 1
                        else:
                            # 获取数据
                            k69_result = self.handler_receive_verify_info(NameCollectionENum.k69_xpath.value)
                            k69_text = [jk.elem.get('text') for jk in self.ui_device.xpath(
                                NameCollectionENum.fuv_xpath.value).all()]

                            temp_collection = set(k69_text).difference(set(last_collection))

                            result = zip(k69_result, k69_text)
                            index = filter(lambda x: True if x[1] in temp_collection else False,
                                           [(i, j[1]) for i, j in enumerate(result) if '直播已结束' not in j[0]])

                            if index and temp_collection:
                                for i_index in index:
                                    self.handler_cancel_btn()
                                    self.handler_android_err()
                                    self.ui_device(resourceId=NameCollectionENum.k69.value, index=i_index[0]).click()
                                    self.move_to_main_class_page(sub_text or text)
                            if not temp_collection:
                                load_status = True
                            last_collection = k69_text
                    else:
                        time.sleep(1)
                        sleep_number = sleep_number + 1
                    self.handler_cancel_btn()
                    self.handler_android_err()
                    self.handler_setting_page()
                    self.ui_device.drag(int(self.screen[0] * 0.5), int(self.screen[1] * 0.85),
                                        int(self.screen[0] * 0.5),
                                        int(self.screen[1] * 0.25), duration=0.2)

                    main_iter_number = main_iter_number + 1
            except (uiautomator2.exceptions.UiObjectNotFoundError, KeyError) as e:
                self.rotating_logger.info('move_to_main_page {} : {} : {}'.format(e, text, sub_text))
                self.check_spider_status()

        else:
            self.rotating_logger.info('move_to_main_page activity error, restart : {} : {}'.format(text, sub_text))
            self.check_spider_status()

    def move_to_main_class_page(self, store_class):
        try:
            self.handler_cancel_btn()
            self.handler_android_err()
            self.handler_setting_page()
            time.sleep(2)
            content = self.check_now_activity_status().output
            if NameCollectionENum.enter_live_store_activity.value in content:
                store_live_active_information = self.handler_live_active_level_info()
                self.handler_cancel_btn()
                self.handler_android_err()
                time.sleep(1)
                self.ui_device(resourceId=NameCollectionENum.k3o.value).click()
                time.sleep(2)
                self.handler_cancel_btn()
                self.handler_android_err()
                self.handler_setting_page()
                store_base_information = self.handle_live_store_base_info()
                sub_store_name = store_base_information.get('finder_id', None)

                self.rotating_logger.info(
                    '开始获取直播间店铺数据 : {} : {}'.format(store_class, sub_store_name))

                if sub_store_name and self.updated_store_data(sub_store_name):

                    self.add_store(store_base_information)
                    self.handler_android_err()
                    store_live_product_information, store_info_base = self.handler_live_product_info()
                    if len(store_base_information) > 0 and len(store_info_base) > 0:
                        self.rotating_logger.info(
                            '开始写直播间数据到数据库: {} -- {} --'.format(store_class, sub_store_name))
                        self.handle_we_collection_store_database(store_class,
                                                                 store_base_information,
                                                                 store_info_base,
                                                                 store_live_active_information)

                        self.handle_we_collection_shop_database(store_base_information,
                                                                store_live_product_information)

                        self.handle_we_collection_status_database(store_base_information)
                        self.rotating_logger.info(
                            '--写入数据完成: {} -- {} --'.format(store_class, sub_store_name))
                time.sleep(1)
                self.ui_device.swipe_ext('right', scale=0.9)
                # self.ui_device.drag(int(self.screen[0] * 0.8), int(self.screen[1] * 0.65),
                #                      int(self.screen[0] * 0.8),
                #                      0, duration=0.1)
            else:
                time.sleep(1)
                self.check_spider_status()
        except (uiautomator2.exceptions.GatewayError, InvalidVersion) as e:
            self.rotating_logger.info('获取直播间数据异常， 重启: {} : {}'.format(e, store_class))
            for _ in range(2):
                self.check_atx_instrument()

            time.sleep(1)
            self.start_uiautomator2()
            time.sleep(1)
            self.check_spider_status()
        except uiautomator2.exceptions.UiObjectNotFoundError as e:
            self.rotating_logger.info('没有查询到元素, 重启: {} : {}'.format(store_class, e))
            self.check_spider_status()

    def move_to_main_page(self, text, sub_text):
        """
        进入直播间，并获取相关数据
        :param text: 大类
        :param sub_text: 小类
        :return:
        """
        self.rotating_logger.info('move_to_main_page: {} : {}'.format(text, sub_text))
        content = self.check_now_activity_status().output
        if NameCollectionENum.enter_more_live_activity.value in content:
            self.handler_android_err()
            try:
                self.processing_sleep(NameCollectionENum.nuw.value, 5)
                self.ui_device(resourceId=NameCollectionENum.nuw.value, text='{}'.format(text)).click()
                if sub_text:
                    self.ui_device(resourceId=NameCollectionENum.nqn.value, text="{}".format(sub_text)).click()
                time.sleep(2.0)
                self.handler_android_err()
                index_zero = 0
                while True:
                    if self.ui_device(resourceId=NameCollectionENum.f98.value).exists:
                        result = self.handler_receive_verify_info(NameCollectionENum.f98_xpath)
                        index = [i for i, j in enumerate(result) if '直播已结束' not in j]
                        if index:
                            index_zero = index[0]
                            break
                        else:
                            self.ui_device.swipe(int(self.screen[0] * 0.5), int(self.screen[1] * 0.3),
                                                 int(self.screen[0] * 0.5), int(self.screen[1] * 0.9), steps=1)
                    else:
                        break

                self.ui_device(resourceId=NameCollectionENum.k69.value, index=index_zero).click()
                time.sleep(1.0)
                self.rotating_logger.info('开始获取直播间信息: {} : {}'.format(text, sub_text))
                self.click_enter_live_page(sub_text)
                time.sleep(1.0)
                self.ui_device(resourceId=NameCollectionENum.igx.value).click_exists()
            except (uiautomator2.exceptions.UiObjectNotFoundError, KeyError) as e:
                self.rotating_logger.info('move_to_main_page {} : {} : {}'.format(e, text, sub_text))
                self.check_spider_status(iter_status=True)
        else:
            self.rotating_logger.info('move_to_main_page activity error, restart : {} : {}'.format(text, sub_text))
            self.check_spider_status(iter_status=True)

    def click_enter_live_page(self, store_class):
        """
        进入具体的直播间，获取直播数据
        :param store_class:
        :return:
        """
        store_name = ""
        self.rotating_logger.info('click_enter_live_page {} '.format(store_class))
        while True:
            try:
                self.handler_cancel_btn()
                self.handler_android_err()
                self.handler_setting_page()
                time.sleep(2)
                content = self.check_now_activity_status().output
                if NameCollectionENum.enter_live_store_activity.value in content:

                    store_live_active_information = self.handler_live_active_level_info()
                    self.handler_cancel_btn()
                    self.handler_android_err()
                    self.ui_device(resourceId=NameCollectionENum.k3o.value).click()
                    time.sleep(3)
                    self.handler_cancel_btn()
                    self.handler_android_err()
                    self.handler_setting_page()

                    store_base_information = self.handle_live_store_base_info()
                    sub_store_name = store_base_information.get('finder_id', None)

                    self.rotating_logger.info(
                        '开始获取直播间店铺数据 : {} : {}'.format(store_class, sub_store_name))

                    if sub_store_name is None or sub_store_name == store_name:
                        self.rotating_logger.info('--click page end: {} -- {} --'.format(store_class, sub_store_name))
                        if sub_store_name is None:
                            self.store_count = self.store_count + 1
                        break

                    if sub_store_name and self.updated_store_data(sub_store_name):
                        self.add_store(store_base_information)
                        self.handler_android_err()
                        store_live_product_information, store_info_base = self.handler_live_product_info()

                        if len(store_base_information) > 0 and len(store_info_base) > 0:
                            self.rotating_logger.info(
                                '开始写直播间数据到数据库: {} -- {} --'.format(store_class, sub_store_name))
                            self.handle_we_collection_store_database(store_class,
                                                                     store_base_information,
                                                                     store_info_base,
                                                                     store_live_active_information)

                            self.handle_we_collection_shop_database(store_base_information,
                                                                    store_live_product_information)

                            self.handle_we_collection_status_database(store_base_information)
                            self.rotating_logger.info(
                                '--写入数据完成: {} -- {} --'.format(store_class, sub_store_name))
                    store_name = sub_store_name
                    time.sleep(1)
                    self.ui_device.swipe(int(self.screen[0] * 0.5), int(self.screen[1] * 0.6),
                                         int(self.screen[0] * 0.5),
                                         int(self.screen[1] * 0.15), steps=5)
                else:
                    time.sleep(1)
                    self.check_spider_status(iter_status=True)
            except (uiautomator2.exceptions.GatewayError, InvalidVersion) as e:
                self.rotating_logger.info('获取直播间数据异常， 重启: {} : {}'.format(e, store_class))
                for _ in range(2):
                    self.check_atx_instrument()

                time.sleep(1)
                self.start_uiautomator2()
                time.sleep(1)
                self.check_spider_status(iter_status=True)
            except (uiautomator2.exceptions.UiObjectNotFoundError, KeyError) as e:
                self.rotating_logger.info('没有查询到元素, 重启: {} : {}'.format(store_class, e))
                self.check_spider_status(iter_status=True)

    def updated_store_data(self, store_name):
        """
        更新数据，使用redis控制只有一台设备在运行一个直播间
        :param store_name:店名
        :return:
        """
        if not self.redis_con.get(store_name):
            self.rotating_logger.info('开始更新 : {} 数据'.format(store_name))
            self.redis_con.set(store_name, 1, 24 * 60 * 60)
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
        """
        获取认证信息和截图信息
        :param element:
        :return:
        """
        data = '沒有發現認證信息'
        if self.ui_device(resourceId=element).exists:
            p = self.ui_device(resourceId=element).screenshot()
            p.save('tmp.jpg')
            with open('tmp.jpg', "rb") as b:
                data = base64.b64encode(b.read())
        return data

    def get_sub_title(self, text):
        self.handler_cancel_btn()
        return self.ui_device(
            resourceId=text).get_text() or "0x00"  # if self.ui_device(resourceId=text).exists else "0x00"

    def handle_live_store_base_info(self):
        """
        获取直播店数据
        :return:
        """
        # time.sleep(3)
        self.handler_cancel_btn()
        self.handler_android_err()
        self.handler_setting_page()
        time.sleep(2)
        store_base_info = {}
        content = self.check_now_activity_status().output

        if NameCollectionENum.enter_store_profile_activity.value in content:
            self.rotating_logger.info('开始获取直播间基本数据')
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
                        finder_temp = self.get_sub_title(NameCollectionENum.cu2.value)
                        store_base_info['finder_id'] = None if finder_temp == '0x00' else finder_temp
                        self.rotating_logger.info(
                            '--enter store base info === : {}'.format(store_base_info.get('finder_id', None)))
                        self.ui_device.swipe(0, int(self.screen[1] * 0.5), int(self.screen[0] * 0.7),
                                             int(self.screen[1] * 0.5),
                                             steps=2)
            time.sleep(2)
        self.ui_device.swipe(0, int(self.screen[1] * 0.5), int(self.screen[0] * 0.7), int(self.screen[1] * 0.5),
                             steps=2)
        return store_base_info

    def handler_live_active_level_info(self):
        """获取热度等信息"""
        store_active = {'store_look_hot_class': self.get_sub_title(NameCollectionENum.i94.value),
                        'store_like_class': self.get_sub_title(NameCollectionENum.f6i.value)}
        return store_active

    @staticmethod
    def handler_atom_info(content, per_element):
        for j in per_element:
            content.append(j.get('text'))
        content.append(" ".join(content))

    def handler_receive_verify_info(self, element):
        """
        循环获取数据
        :param element:
        :return:
        """
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
        """
        获取产品缩略图
        :param elem: 页面元素名
        :param have_dict:过滤字典
        :param have_temp_dict: 删除字典
        :return:
        """
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
        """
        预约直播时间
        :return:
        """
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
        """
        获取直播店产品
        :return:
        """
        last_product = 1
        have_dict = {}
        store_status = True
        store_info_base = {}
        collection_result = []
        stop_cycle_condition = True
        # self.processing_sleep(NameCollectionENum.fl9.value)

        content = self.check_now_activity_status().output

        if NameCollectionENum.enter_live_store_activity.value in content:
            self.handler_cancel_btn()
            if self.ui_device(resourceId=NameCollectionENum.fl9.value).exists:
                self.ui_device(resourceId=NameCollectionENum.fl9.value).click()

            # time.sleep(3)
            self.handler_cancel_btn()
            self.rotating_logger.info('开始循环获取商品')
            while stop_cycle_condition:
                self.handler_android_err()
                index_max = self.handler_receive_verify_info(NameCollectionENum.l7n_xpath.value)
                if not index_max or last_product == int(max(index_max)):
                    stop_cycle_condition = False
                    self.rotating_logger.info('获取商品信息结束')

                filter_dict = {}
                have_temp_dict = {}
                text_price_content = self.handler_receive_verify_info(NameCollectionENum.fll_xpath.value)

                text_keep_complete = WeCollectionHandleMain.handler_keep_data_complete(text_price_content,
                                                                                       filter_dict)

                photo_content = self.handler_photo_product_info(NameCollectionENum.huu_xpath.value, have_dict,
                                                                have_temp_dict)
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
                    point = self.handler_receive_verify_info(NameCollectionENum.mub.value)
                    store_info_base["store_point"] = " ".join(point[0]) if point else '0x00'
                    store_status = False

                last_product = int(max(index_max)) if index_max else 1

                self.ui_device.swipe(int(self.screen[0] * 0.5), int(self.screen[1] * 0.9),
                                     int(self.screen[0] * 0.5),
                                     int(self.screen[1] * 0.35), steps=2)

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
                self.rotating_logger.info(f'写入 {store_base_information["finder_id"]} 失败 :{e}')

    def handle_we_collection_shop_database(self, store_base_information, store_live_product_information):
        """
        写数据到数据产品表
        :param store_base_information: 直播间基本信息
        :param store_live_product_information:  产品基本信息
        :return:
        """
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
                    self.rotating_logger.info(e)
            self.insert_data_to_database(result)

    def handle_we_collection_status_database(self, store_base_information):
        """
        基本信息
        :param store_base_information: 直播间基本信息
        :return:
        """
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
                self.rotating_logger.info(e)

    def add_store(self, store_base_information):
        """
        增量添加直播间
        :param store_base_information: 直播间基本信息
        :return:
        """
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
