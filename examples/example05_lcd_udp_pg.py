###############################################################################
# μIoT LCD for Raspberry Pi Pico W + AQM0802A [無線LAN対応版]
# UDPを受信してLCDへ表示します
# 双方向通信を維持するための Ping を送信します
#                                         Copyright (c) 2021-2023 Wataru KUNINO
###############################################################################

# AE-AQM0802A
##############################
# aqm0802 # Pico # GPIO
##############################
#    GND  #  3   # GND
#    SDA  #  4   # GP2
#    SCL  #  5   # GP3
#  RESET  #  6   # GP4
#     +V  #  7   # GP5
##############################

SSID = "1234ABCD"                               # 無線LANアクセスポイント SSID
PASS = "password"                               # パスワード

port = 1024                                     # UDPポート番号
buf_n= 128                                      # 受信バッファ容量(バイト)
aqm0802 = 0x3E                                  # LCD AQM0802AのI2Cアドレス

import network                                  # ネットワーク通信
import socket                                   # ソケット通信
from machine import Pin,I2C                     # machineのI2Cを組み込む
from utime import sleep                         # μtimeからsleepを組み込む
import errno

led = Pin("LED", Pin.OUT)                       # Pico W LED用ledを生成
rst = Pin(4, Pin.OUT)                           # GP4をaqm0802のRESETに接続
rst.value(0)                                    # RESETに0Vを出力
vdd = Pin(5, Pin.OUT)                           # GP5をaqm0802のV+ピンに接続
vdd.value(1)                                    # V+用に3.3Vを出力
i2c = I2C(1, scl=Pin(3), sda=Pin(2))            # GP3をaqm0802のSCL,GP2をSDAに
sleep(0.1)                                      # RESET待機
rst.value(1)                                    # RESETに3.3Vを出力
sleep(0.2)                                      # RESET待機
i2c.writeto_mem(aqm0802, 0x00, b'\x39')         # IS=1
i2c.writeto_mem(aqm0802, 0x00, b'\x11')         # OSC
i2c.writeto_mem(aqm0802, 0x00, b'\x70')         # コントラスト  0
i2c.writeto_mem(aqm0802, 0x00, b'\x56')         # Power/Cont 6
i2c.writeto_mem(aqm0802, 0x00, b'\x6C')         # FollowerCtrl  C
sleep(0.2)
i2c.writeto_mem(aqm0802, 0x00, b'\x38')         # IS=0
i2c.writeto_mem(aqm0802, 0x00, b'\x0C')         # DisplayON C

def i2c_lcd_out(y, text):
    text += '        '                          # 空白8文字を追記
    if y == 0:
        i2c.writeto_mem(aqm0802, 0x00, b'\x80') # 1行目
    else:
        i2c.writeto_mem(aqm0802, 0x00, b'\xC0') # 2行目
    i2c.writeto_mem(aqm0802, 0x40, bytearray(text.encode())) # 文字出力

i2c_lcd_out(0,'ex05 LCD')                       # タイトルをLCDに表示
i2c_lcd_out(1,'UDP Logr')                       # Send a string to LCD

def checksum_calc(payload):
    if len(payload)%2 == 1:
        payload += b'\x00'  # total length is odd, padded with one octet of zeros
    sum = 0x0000
    for i in range(len(payload)//2):    #  1 の補数和
        sum += int(payload[i*2]) * 256
        sum += int(payload[i*2+1])
        if sum > 0xFFFF:
            sum += 1
            sum &= 0xFFFF
    sum = ~(sum) & 0xFFFF
    return sum.to_bytes(2, 'big')

icm_type = b'\x08'      # header[0] Type = echo message
icm_code = b'\x00'      # header[1] Code = 0
icm_csum = b'\x00\x00'  # header[2:4] Checksum = 0x0000 計算前の初期値
icm_idnt = b'\x12\x34'  # header[4:6] Identifier
icm_snum = b'\x00\x00'  # header[6:8] Sequence Number

def send_icmp(adr):
    print('Ping',adr,end=' ')
    global icm_snum
    sequence = int.from_bytes(icm_snum,'big')
    sequence += 1
    icm_snum = sequence.to_bytes(2, 'big')         # Sequence Number
    header = icm_type + icm_code + icm_csum + icm_idnt + icm_snum
    checksum = checksum_calc(header)
    header = icm_type + icm_code + checksum + icm_idnt + icm_snum
    try:
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1)
    except Exception as e:                      # 例外処理発生時
        print(e)                                # エラー内容を表示
        return False
    sock2.sendto(header,(adr,0))                # Ping送信
    sock2.settimeout(1)
    while sock2:
        try:
            icmp = sock2.recv(256)              # 受信データの取得
        except OSError as e:                    # 例外処理発生時
            if e.errno == errno.EAGAIN:
                continue
            sock2.close()                       # ソケットの切断
            if e.errno == errno.ETIMEDOUT:
                print('Timeout') 
            else:
                print(e)                        # エラー内容を表示
            return False
        if icmp[0] == 0x45 and icmp[9] == 0x01 and icmp[20] == 0x00\
          and int.from_bytes(icmp[24:26], 'big') == int.from_bytes(icm_idnt,'big')\
          and int.from_bytes(icmp[26:28], 'big') == int.from_bytes(icm_snum,'big')\
          and  not int.from_bytes(checksum_calc(icmp[20:]),'big'):
            print("Passed")
            sock2.close()                       # ソケットの切断
            return True

wlan = network.WLAN(network.STA_IF)             # 無線LAN用のwlanを生成
wlan.active(True)                               # 無線LANを起動
wlan.connect(SSID, PASS)                        # 無線LANに接続
while not wlan.isconnected():                   # 接続待ち
    print('.', end='')                          # 接続中表示
    led.toggle()                                # LEDの点灯／非点灯の反転
    sleep(1)                                    # 1秒間の待ち時間処理
print(wlan.ifconfig()[0])                       # IPアドレスを表示
adr_ping = str(wlan.ifconfig()[2])
i2c_lcd_out(0,'Listen..')                       # Send a string to LCD
i2c_lcd_out(1,'Port'+str(port))                 # ポート番号表示
led.value(0)                                    # LEDをOFFにする

while True:                                     # 永遠に繰り返す
    if send_icmp(adr_ping) == False:
        adr_ping = str(wlan.ifconfig()[2])
    try:
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # ソケットを作成
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # オプション
        sock.settimeout(10)
        sock.bind(('',port))                    # ソケットに接続
    except Exception as e:                      # 例外処理発生時
        i2c_lcd_out(0,'ERROR')                  # Send a string to LCD
        i2c_lcd_out(1,str(e))                   # 例外内容表示
        print('Exception',e)                    # エラー内容を表示
        continue                                # retry to bind sock
    try:
        udp, udp_from = sock.recvfrom(buf_n)    # UDPパケットを取得
    except OSError as e:                        # 例外処理発生時
        if e.errno != errno.ETIMEDOUT:
            i2c_lcd_out(0,'ERROR')              # Send a string to LCD
            i2c_lcd_out(1,str(e))               # 例外内容表示
            print('Exception',e)                # エラー内容を表示
        sock.close()
        adr_ping = str(wlan.ifconfig()[2])
        continue                                # retry to bind sock
    udp = udp.decode()                          # UDPデータを文字列に変換
    led.toggle()                                # LEDの点灯／非点灯の反転
    s=''                                        # 表示用の文字列変数s
    for c in udp:                               # UDPパケット内
        if ord(c) >= ord(' ') and ord(c) <= ord('~'): # 表示可能文字
            s += c                              # 文字列sへ追加
    if s == 'Ping':                             # 受信データがPingの時
        led.value(1)                            # LEDをONにする
    if s == 'Pong':                             # 受信データがPongの時
        led.value(0)                            # LEDをOFFにする
    print(udp_from[0] + ', ' + s)               # 受信データをシリアル出力
    i2c_lcd_out(0,s[0:8])                       # 受信データの先頭8文字を表示
    i2c_lcd_out(1,s[8:])                        # 8文字目以降を表示
    adr_ping = str(udp_from[0])
    led.toggle()                                # LEDの点灯／非点灯の反転
    sock.close()                                # ソケットの切断

###############################################################################
# 参考文献 1 Pythonで作るIoTシステム プログラム・サンプル集 (CQ出版社)
#            (ラズベリー・パイでI/O制御 & Pico，micro:bit，STM32でクラウド通信)
'''
    https://www.amazon.co.jp/dp/4789859894
    第8章 STM32マイコン用 MicroPythonプログラム
'''
###############################################################################
# 参考文献 2 ESP32 マイコン用 MicroPython プログラム
'''
    https://bokunimo.net/iot/cq/esp32.pdf
'''
###############################################################################
# 参考文献 3 Raspberry Pi Pico のシリアルCOMが表示されないときの修復方法
'''
    https://bokunimo.net/blog/raspberry-pi/1460/
'''
###############################################################################
# 参考文献 4 Pico W のLED 使用方法
'''
    https://forums.raspberrypi.com/viewtopic.php?t=336836
'''

###############################################################################
# 参考文献 5 ICMP Ping Code Examples
'''
    https://github.com/bokunimowakaru/ping
'''

###############################################################################
# 引用コード 本プログラムは下記のコードを変更して作成したものです
''' 
    https://github.com/bokunimowakaru/iot/blob/master/micropython/nucleo-f767zi/udp_logger_lcd.py
    https://github.com/bokunimowakaru/iot/blob/master/micropython/raspi-pico/test_lcd.py
'''
