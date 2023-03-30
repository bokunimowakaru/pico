# coding: utf-8
# UDPを受信する for Raspberry Pi Pico W [無線LAN対応版]
# Copyright (c) 2018-2023 Wataru KUNINO

# Error ENOMEM や EADDRINUSE が出た場合はハードウェアリセットを実行してください
#   machine.reset()

SSID = "1234ABCD"                               # 無線LANアクセスポイント SSID
PASS = "password"                               # パスワード
port = 1024                                     # UDPポート番号
buf_n= 128                                      # 受信バッファ容量(バイト)

import network                                  # ネットワーク通信
import socket                                   # ソケット通信

led = Pin("LED", Pin.OUT)                       # Pico W LED用ledを生成
wlan = network.WLAN(network.STA_IF)             # 無線LAN用のwlanを生成
wlan.active(True)                               # 無線LANを起動
wlan.connect(SSID, PASS)                        # 無線LANに接続
while wlan.status() != 3:                       # 接続待ち
    print('.', end='')                          # 接続中表示
    led.toggle()                                # LEDの点灯／非点灯の反転
    sleep(1)                                    # 1秒間の待ち時間処理
print('\n',wlan.ifconfig())                     # 無線LANの状態を表示

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # ソケットを作成
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # オプション
sock.bind(('',port))                            # ソケットに接続
print('Listening UDP port', port, '...')        # ポート番号表示
led.value(1)                                    # LEDをOFFにする

while sock:                                     # 永遠に繰り返す
    udp, udp_from = sock.recvfrom(buf_n)        # UDPパケットを取得
    udp = udp.decode()                          # UDPデータを文字列に変換
    led.toggle()                                # LEDの点灯／非点灯の反転
    s=''                                        # 表示用の文字列変数s
    for c in udp:                               # UDPパケット内
        if ord(c) >= ord(' ') and ord(c) <= ord('~'): # 表示可能文字
            s += c                              # 文字列sへ追加
    if s == 'Ping':                             # 受信データがPingの時
        led.value(1)                            # LEDをOFFにする
    if s == 'Pong':                             # 受信データがPongの時
        led.value(0)                            # LEDをOFFにする
    print(udp_from[0] + ', ' + s)               # 受信データを出力
    led.toggle()                                # LEDの点灯／非点灯の反転
sock.close()                                    # ソケットの切断
led.value(0)                                    # LEDをOFFにする
