#!/usr/bin/env python3
# CPUに負荷をかけます。

from machine import Pin                 # ライブラリmachineのPinを組み込む
wifi = Pin(23, Pin.OUT)
wifi.value(0)                           # Wi-Fi機能をOFF

def noop():
    return None

print("Started Nop Stress Test")
while 1:
    noop()
