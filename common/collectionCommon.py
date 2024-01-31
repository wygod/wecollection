# -*- encoding:utf-8 -*-
import time

from common import *
from CollectionEnum.collectionEnum import NameCollectionENum
from collectionException.collectionSelfDefineException import CollectionElementNotFoundException


class InitVenv:
    def __init__(self, config):
        self.host = config.baseTcp.master_host
        self.port = config.baseTcp.port
        self.adb_client_shell = self.adb_client()

    def adb_client(self):
        return adbClient(host=self.host, port=self.port)

    def adb_device_list(self):
        return [sub_adb.serial for sub_adb in self.adb_client_shell.devices()]


class InitDeviceApp(InitVenv):
    def __init__(self, config, device_serial):
        super(InitVenv, self).__init__(config)
        self.device_serial = device_serial
        self.ui_device = self.ui_connect()

    def ui_connect(self):
        device = u2.connect(self.device_serial)
        device.implicitly_wait(10)
        if not device.uiautomator.running():
            device.uiautomator.start()
        return device

    def screen_size(self):
        return self.ui_device.window_size()

    def start_atx_agent(self):
        start_atx_cmd = "/data/local/tmp/atx-agent server -d"
        self.ui_device.shell(start_atx_cmd)

    def check_atx_instrument(self):
        try:
            start_instrument_cmd = "am instrument -w -r -e debug false -e class com.github.uiautomator.stub.Stub com.github.uiautomator.test/androidx.test.runner.AndroidJUnitRunner"
            self.ui_device.shell(start_instrument_cmd, timeout=random.randint(5, 8))
        except Exception as e:
            print('check value')
            print(e)

    def stop_atx_agent(self):
        start_atx_cmd = "/data/local/tmp/atx-agent server stop"
        self.ui_device.shell(start_atx_cmd)

    def check_now_activity_status(self):
        activity_content = self.ui_device.shell('dumpsys activity top | grep ACTIVITY')
        return activity_content

    def check_uiautomator2_status(self):
        return self.ui_device.uiautomator.running()

    def start_uiautomator2(self):
        self.ui_device.uiautomator.start()

    def stop_uiautomator2(self):
        self.ui_device.uiautomator.stop()

    def start_current_app(self):
        if self.ui_device.xpath('//*[@text="微信"]').exists:
            self.ui_device.xpath('//*[@text="微信"]').click()
            time.sleep(3)

    def destroy_current_app(self):
        content = self.check_now_activity_status()
        if NameCollectionENum.mm.value in content.output:
            self.ui_device.app_stop("com.tencent.mm")

    def move_to_live(self):
        content = self.check_now_activity_status().output
        if NameCollectionENum.we_chat_start_page.value in content:
            if self.ui_device.xpath('//*[@text="直播"]').exists:
                self.ui_device.xpath('//*[@text="直播"]').click()
                time.sleep(6)
                self.move_to_project_main()
            else:
                self.move_to_button()

    def move_to_button(self):
        content = self.check_now_activity_status().output
        if NameCollectionENum.we_chat_start_page.value in content:
            if self.ui_device.xpath('//*[@text="发现"]').exists:
                self.ui_device.xpath('//*[@text="发现"]').click()
                time.sleep(2)
                self.move_to_live()

    def move_to_project_main(self):
        # time.sleep(3)
        content = self.check_now_activity_status().output
        if NameCollectionENum.enter_live_store_activity.value in content:
            if self.ui_device(resourceId=NameCollectionENum.igx.value).exists:
                self.ui_device(resourceId=NameCollectionENum.igx.value).click()
                time.sleep(2)

        print("start")
        content = self.check_now_activity_status().output
        if NameCollectionENum.enter_live_main_activity.value in content:
            if self.ui_device(resourceId=NameCollectionENum.b1h.value).exists:
                self.ui_device(resourceId=NameCollectionENum.b1h.value).click()
                time.sleep(2)

    def get_menu_list_text(self, source_id):
        if self.ui_device(resourceId=source_id).exists:
            sub_shop_title = self.ui_device(resourceId=source_id)
            return [i.get_text() for i in sub_shop_title]
        return None

    def loop_get_menu_text(self, source_id):
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
