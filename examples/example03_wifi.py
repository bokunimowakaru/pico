# coding: utf-8
# IoT 温度計μ for MicroPython (よりメモリの節約が可能なusocketを使用)
# Copyright (c) 2018-2019 Wataru KUNINO

# Error ENOMEM や EADDRINUSE が出た場合はハードウェアリセットを実行してください
#   machine.reset()

SSID = "1234ABCD"                               # 無線LANアクセスポイント SSID
PASS = "password"                               # パスワード

udp_to = '255.255.255.255'                      # UDPブロードキャスト
udp_port = 1024                                 # UDPポート番号
device_s = 'temp._3'                            # デバイス識別名
interval = 10                                   # 送信間隔（秒）
temp_offset = 8.0                               # CPU温度上昇値(要調整)

from machine import ADC,Pin                     # machineからADCを組み込む
from machine import UART                        # machineからUARTを組み込む
from utime import sleep                         # μtimeからsleepを組み込む
import network                                  # ネットワーク通信
import usocket                                  # μソケット通信

led = Pin(25, Pin.OUT)                          # GPIO出力用ledを生成
adc = ADC(4)                                    # 温度センサ用adcを生成

wlan = network.WLAN(network.STA_IF)             # Ethernet用のethを生成
wlan.active(True)                               # Ethernetを起動
wlan.connect(SSID, PASS)
while True:
    if wlan.status() == 3:
        break
    print('.', end='')
    sleep(1)
ifconf = wlan.ifconfig()
print('\n',ifconf)

while True:                                     # 繰り返し処理
    val = adc.read_u16()                        # ADC値を取得して変数valに代入
    mv = val * 3300 / 65535                     # ADC値を電圧(mV)に変換
    temp = 27 - (mv - 706) / 1.721              # ADC電圧値を温度(℃)に変換
    temp -= temp_offset                         # temp_offsetを減算
    temp_i = round(temp)                        # 整数に変換してtemp_iへ
    print('Temperature =',temp_i,'('+str(temp)+')') # 温度値を表示する
    led.value(1)                                # LEDをONにする

    sock = usocket.socket(usocket.AF_INET,usocket.SOCK_DGRAM) # μソケット作成
    #      ~~~~~~~        ~~~~~~~         ~~~~~~~
    udp_s = device_s + ', ' + str(temp_i)       # 表示用の文字列変数udp
    print('send :', udp_s)                      # 受信データを出力
    udp_bytes = (udp_s + '\n').encode()         # バイト列に変換

    try:
        sock.sendto(udp_bytes,(udp_to,udp_port)) # UDPブロードキャスト送信
    except Exception as e:                      # 例外処理発生時
        print(e)                                # エラー内容を表示
    sock.close()                                # ソケットの切断

    led.value(0)                                # LEDをOFFにする
    sleep(5)                                    # 5秒間の待ち時間処理
