###############################################################################
# Raspberry Pi Pico W + 湿度センサ SHT31 for Ambient [無線LAN対応版]
#                                             Copyright (c) 2023 Wataru KUNINO
###############################################################################

# coding: utf-8
# IoT連携 Ambientへ送信 HTTP POST μrequests for MicroPython (μrequests使用)
# Copyright (c) 2019 Wataru KUNINO

# ご注意：ESP32マイコンのWi-FiをONにします。
# 　　　　使い方を誤ると、電波法に違反する場合があります。
# 　　　　作成者は一切の責任を負いません。

# インストール方法
# (1) wifi_ssidとwifi_pass、ambient_chid、ambient_wkeyの4項目を設定する
# (2) プログラム末尾のdeepsleepを有効にする（#を消してインデントを無くす）
# (3) ファイル名をmain.pyに変更する
# (4) WebREPLで転送する

SSID = "1234ABCD"                               # 無線LANアクセスポイント SSID
PASS = "password"                               # パスワード
ambient_chid='0000'                             # Ambientで取得したチャネルIDを入力
ambient_wkey='0123456789abcdef'                 # ここにはライトキーを入力
amdient_tag='d1'                                # データ番号d1～d8のいずれかを入力

import network                                  # ネットワーク通信ライブラリ
import urequests                                # HTTP通信ライブラリ
from sys import exit                            # ライブラリsysからexitを組み込む
from machine import ADC, Pin, deepsleep, reset  # GPIO用Pinとディープスリープを組込
from time import sleep                          # ライブラリtimeからsleepを組み込む

url = 'http://ambidata.io/api/v2/channels/'+ambient_chid+'/data' # アクセス先
head = {'Content-Type':'application/json'}      # ヘッダを変数head_dictへ
body = {'writeKey':ambient_wkey, amdient_tag:0.0} # 内容を変数bodyへ

led = Pin("LED", Pin.OUT)                       # Pico W LED用ledを生成
wlan = network.WLAN(network.STA_IF)             # Wi-Fi接続用インスタンスの生成
wlan.active(True)                               # Wi-Fiの起動
wlan.connect(SSID, PASS)                        # 無線LANに接続
while not wlan.isconnected():                   # 接続待ち
    print('.', end='')                          # 接続中表示
    led.toggle()                                # LEDの点灯／非点灯の反転
    sleep(1)                                    # 1秒間の待ち時間処理
print(wlan.ifconfig()[0])                       # IPアドレスを表示

adc = ADC(4)                                    # 温度センサ用ADCポートadcを生成
while True:                                     # 繰り返し処理
    val = adc.read_u16()                        # ADCから値を取得して変数valに代入
    mv = val * 3300 / 65535                     # ADC値を電圧(mV)に変換
    temp = 27 - (mv - 706) / 1.721              # ADC電圧値を温度(℃)に変換
    temp_s = str(round(temp,1))                 # 小数点第1位で丸めた結果を文字列に
    print('Temperature =',temp_s,end=',')       # 温度を表示する
    body[amdient_tag] = temp                    # 辞書型変数body内に埋め込む
    led.value(1)                                # LEDを点灯
    try:                                        # 例外処理の監視を開始
        res = urequests.post(url, json=body, headers=head)  # HTTPリクエストを送信
        print(' HTTP Stat =', res.status_code)
    except Exception as e:                      # 例外処理発生時
        print(e)                                # エラー内容を表示
    res.close()
    led.value(0)                                # LEDを消灯
    sleep(30)                                   # 5秒間の待ち時間処理

###############################################################################
# 引用コード
''' 
    https://github.com/bokunimowakaru/iot/blob/master/micropython/esp32/test_htpost_ambient.py
'''
