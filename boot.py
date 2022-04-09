# coding: utf-8
# This file is executed on every boot (including wake-boot from deepsleep)
import network
import time
from machine import PWM
from machine import Pin

import esp
esp.osdebug(None)

BLINK_GPIO_R = 3
BLINK_GPIO_G = 4
BLINK_GPIO_B = 5

b_pwm_led = PWM(Pin(BLINK_GPIO_B), freq=50, duty=10)

def connect_to_wifi():
    try:
        import wifi_client_cfg as wifi
    except Exception:
        r_pwm_led = PWM(Pin(BLINK_GPIO_B), freq=50, duty=10)
        print("No wifi_client_cfg found, wifi_client_cfg.py文件是否存在。")
    wlan = network.WLAN(network.STA_IF) # create station interface
    if not wlan.isconnected():
        wlan.active(True)       # activate the interface
        print("Wifi list: ", wlan.scan())             # scan for access points
        print("Wifi isconnected: ", wlan.isconnected())      # check if the station is connected to an AP
        wlan.connect(wifi.EXTERNEL_WIFI_SSID, wifi.EXTERNEL_WIFI_PASSWORD) # connect to an AP
        for i in range(10):
            if not wlan.isconnected():
                print("Attemp connect to WiFi, ", i, "second")
                time.sleep(1)

        print("Wifi isconnected: ", wlan.isconnected())
        print("Wifi client MAC: ", wlan.config('mac'))      # get the interface's MAC address
        print("Wifi client IP: ", wlan.ifconfig())         # get the interface's IP/netmask/gw/DNS addresses
        
connect_to_wifi()
g_pwm_led = PWM(Pin(BLINK_GPIO_G), freq=50, duty=10)

# 启动webrepl服务
import webrepl
webrepl.start()

b_pwm_led.deinit()    # 启动完成关闭蓝灯

