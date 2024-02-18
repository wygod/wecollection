# -*- encoding:utf-8 -*-
import time

from common import *
from CollectionEnum.collectionEnum import NameCollectionENum


class InitVenv:
    def __init__(self, config, device_serial):
        """
        :param config:环境配置文件，包含adb
        :param device_serial: 设备
        """
        self.host = config.baseTcp.master_host
        self.port = config.baseTcp.port
        self.device_serial = device_serial
        self.adb_client_shell = self.adb_client()
        self.ui_device = self.ui_connect()

    def adb_client(self):
        """
        adb 链接设备
        :return:
        """
        return adbClient(host=self.host, port=self.port)

    def adb_device_list(self):
        return [sub_adb.serial for sub_adb in self.adb_client_shell.devices()]

    def ui_connect(self):
        """
        链接设备
        :return:
        """
        device = u2.connect(self.device_serial)
        device.implicitly_wait(10)
        if not device.uiautomator.running():
            device.uiautomator.start()
        return device

    def start_atx_agent(self):
        """
        启动start_atx_agent
        :return:
        """
        start_atx_cmd = "/data/local/tmp/atx-agent server -d"
        self.ui_device.shell(start_atx_cmd)

    def check_atx_instrument(self, low=8):
        """
        授权调试设备
        :param low:
        :return:
        """
        try:
            start_instrument_cmd = "am instrument -w -r -e debug false -e class com.github.uiautomator.stub.Stub com.github.uiautomator.test/androidx.test.runner.AndroidJUnitRunner"
            self.ui_device.shell(start_instrument_cmd, timeout=random.randint(low, 2 * low))
        except Exception as e:
            print('check value')
            print(e)
        finally:
            self.ui_device.uiautomator.start()

    def stop_atx_agent(self):
        """
        stop atx
        :return:
        """
        start_atx_cmd = "/data/local/tmp/atx-agent server stop"
        self.ui_device.shell(start_atx_cmd)


class InitDeviceApp(InitVenv):
    def __init__(self, config, device_serial):
        InitVenv.__init__(self, config=config, device_serial=device_serial)

    def processing_sleep(self, task, step=10):
        """
        等待页面加载完成
        :param task: 页面元素
        :param step: 等待次数
        :return:
        """
        i = 0
        while True:
            if self.ui_device(resourceId=task).exists or i > step:
                break
            time.sleep(1)
            i = i + 1

    def screen_size(self):
        """
        设备大小
        :return:
        """

        # if self.ui_device(resourceId=NameCollectionENum.recent_apps.value).exists:
        #     return self.ui_device.window_size()[0], int(self.ui_device.window_size()[1]*0.9)
        return self.ui_device.window_size()

    def check_now_activity_status(self):
        """
        安卓activity
        :return:
        """
        time.sleep(1)
        activity_content = self.ui_device.shell('dumpsys activity top | grep ACTIVITY')
        return activity_content

    def check_uiautomator2_status(self):
        return self.ui_device.uiautomator.running()

    def start_uiautomator2(self):
        self.ui_device.uiautomator.start()

    def stop_uiautomator2(self):
        self.ui_device.uiautomator.stop()

    def start_current_app(self):
        """
        启动微信
        """
        if self.ui_device.xpath('//*[@text="微信"]').exists:
            self.ui_device.xpath('//*[@text="微信"]').click()
            time.sleep(3)

    def destroy_current_app(self):
        """
        退出微信
        :return:
        """
        content = self.check_now_activity_status()
        if NameCollectionENum.mm.value in content.output:
            self.ui_device.app_stop("com.tencent.mm")

    def move_to_live(self):
        """
        点击进入直播间
        :return:
        """
        content = self.check_now_activity_status().output
        if NameCollectionENum.we_chat_start_page.value in content:
            if self.ui_device.xpath('//*[@text="直播"]').exists:
                self.ui_device.xpath('//*[@text="直播"]').click()
                time.sleep(2)
                self.move_to_project_main()
            else:
                self.move_to_button()

    def move_to_button(self):
        """
        点击进入直播按钮页面
        :return:
        """
        content = self.check_now_activity_status().output
        if NameCollectionENum.we_chat_start_page.value in content:
            if self.ui_device.xpath('//*[@text="发现"]').exists:
                self.ui_device.xpath('//*[@text="发现"]').click()
                time.sleep(2)
                self.move_to_live()

    def move_to_project_main(self):
        """
        进入直播更多页面
        :return:
        """
        content = self.check_now_activity_status().output
        if NameCollectionENum.enter_live_store_activity.value in content:
            if self.ui_device(resourceId=NameCollectionENum.igx.value).exists:
                self.ui_device(resourceId=NameCollectionENum.igx.value).click()
                time.sleep(2)

        content = self.check_now_activity_status().output
        # self.processing_sleep(NameCollectionENum.b1h.value, 5)

        if NameCollectionENum.enter_live_main_activity.value in content:
            if self.ui_device(resourceId=NameCollectionENum.b1h.value).exists:
                self.ui_device(resourceId=NameCollectionENum.b1h.value).click()
                time.sleep(2)

    def get_menu_list_text(self, source_id):
        """
        注：原来获取按钮文字函数
        :param source_id:
        :return:
        """
        if self.ui_device(resourceId=source_id).exists:
            sub_shop_title = self.ui_device(resourceId=source_id)
            return [i.get_text() for i in sub_shop_title]
        return None

    def loop_get_menu_text(self, source_id):
        """
        注：原来获取按钮文字函数
        :param source_id:
        :return:
        """
        all_menu_text = []
        while True:
            menu_list = self.get_menu_list_text(source_id)
            if all_menu_text[-1] == menu_list[-1] or None:
                break
            else:
                if menu_list:
                    all_menu_text.extend(
                        [per_menu_text for per_menu_text in menu_list if per_menu_text not in all_menu_text])
                    self.ui_device.swipe(956, 382, 0, 382, duration=1)

        return all_menu_text
