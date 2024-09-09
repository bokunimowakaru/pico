###############################################################################
# Raspberry Pi Pico / Pico W の動作確認 Lチカ＋ログ出力表示
###############################################################################
# 内容
# ・5秒おきにスリープ状態を推移します。推移時にLEDの点滅で状態変更を示します。
# ・ディープスリープ復帰後はリセットがかかります。
# ・プログラムを書き込んでいた場合は、リセット後にプログラムが再開します。
# ・Wi-Fi機能をOFFにするとLED表示機能が動作しません。
#
# LED表示      Num.  スリープ状態                   継続時間
# －－－－－    0    sleep (通常)                   5秒
# ･－－－－     1    lightsleep (ライトスリープ)    5秒
# ･･－－－      2    deepsleep (ディープスリープ)   5秒
#
# 消費電流の測定結果例
#
# モデル名              sleep       lightsleep  deepsleep	Version
# Raspberry Pi Pico W   19.4 mA      1.4 mA      1.4 mA		v1.23.0 2024-06-02
# Raspberry Pi Pico 2	16.1 mA     16.0 mA     15.8 mA		v1.24.0-preview.201
#
#                                         Copyright (c) 2021-2024 Wataru KUNINO
###############################################################################

from machine import Pin                 # ライブラリmachineのPinを組み込む
from machine import deepsleep,lightsleep
from utime import sleep

sleep_duration = 5                      # スリープ時間（秒）
wifi = Pin(23, Pin.OUT)
wifi.value(0)                           # Wi-Fi機能をOFF

class sleepmode:
    num = 3
    mode_sleep = 0
    mode_lightsleep = 1
    mode_deepsleep = 2
    mode_name = ['sleep','lightsleep','deepsleep']

def goto_sleep(mode):
    print('Sleep Mode =',sleepmode.mode_name[mode])
    sleep(0.1)
    if mode == sleepmode.mode_sleep:
        sleep(sleep_duration)           # 待ち時間処理 utime.sleep
    if mode == sleepmode.mode_lightsleep:
        lightsleep(sleep_duration*1000) # 待ち時間処理 machine.lightsleep
    if mode == sleepmode.mode_deepsleep:
        deepsleep(sleep_duration*1000)  # 待ち時間処理 machine.deepsleep

def led_disp(n):                        # LEDの点滅で数字を示す 0～9
    for i in range(1,6):
        led.value(1)
        if n<0 or n>9:
            sleep(0.2 if i%2 else 0.6)  # i%2 ? 0.2 : 0.6
        elif i <= n%5:
            sleep(0.2 if n<=5 else 0.6) # n<=5 ? 0.2 : 0.6
        else:
            sleep(0.6 if n<=5 else 0.2) # n<=5 ? 0.6 : 0.2
        led.value(0)
        sleep(0.2)
    sleep(0.6)

try:
    led = Pin("LED", Pin.OUT)           # GPIO出力用ledを生成(Pico W 用)
except TypeError:
    led = Pin(25, Pin.OUT)              # GPIO出力用ledを生成(Pico 用)

for mode in range(sleepmode.num):
   led_disp(mode)                       # スリープ番号0～2をLEDの点滅で出力
   goto_sleep(mode)                     # スリープ番号0～2を実行

###############################################################################
# 以下は実行されない(使用方法例)
mode = sleepmode.mode_deepsleep
goto_sleep(mode)
exit()
