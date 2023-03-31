###############################################################################
# Raspberry Pi Pico W の動作確認 Lチカ＋ログ出力表示
# 0.5秒おきにLEDの点灯と消灯を反転する
#                                         Copyright (c) 2021-2023 Wataru KUNINO
###############################################################################

from machine import Pin                 # ライブラリmachineのPinを組み込む
from utime import sleep                 # μtimeからsleepを組み込む

led = Pin("LED", Pin.OUT)               # Pico W LED用インスタンスledを生成

while True:                             # 繰り返し処理
    b = led.value()                     # 現在のLEDの状態を変数bへ代入
    b = int(not(b))                     # 変数bの値を論理反転(0→1、1→0)
    print('Hello, world! LED =',b)      # 変数bの値を表示
    led.value(b)                        # 変数bの値をLED出力
    sleep(0.5)                          # 0.5秒間の待ち時間処理

###############################################################################
# 参考文献 1
'''
    ラズベリー・パイでI/O制御 & Pico，micro:bit，STM32でクラウド通信
    Pythonで作るIoTシステム プログラム・サンプル集
    第9章 ラズベリー・パイ Pico で BLEワイヤレス・センサを作る
'''
###############################################################################
# 参考文献 2
'''
    Pico W のLED 使用方法
    https://forums.raspberrypi.com/viewtopic.php?t=336836
'''
###############################################################################
# 引用コード
''' 
    https://github.com/bokunimowakaru/iot/blob/master/micropython/raspi-pico/example01_hello.py
'''
