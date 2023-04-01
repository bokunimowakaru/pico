###############################################################################
# IoT温度センサ for Raspberry Pi Pico W [Ambient対応] [無線LAN対応]
# 温度値を Ambient (https://ambidata.io/) に送信します。
#                                       Copyright (c) 2019 - 2023 Wataru KUNINO
###############################################################################

SSID = "1234ABCD"                               # 無線LANアクセスポイント SSID
PASS = "password"                               # パスワード
ambient_chid='0000'                             # Ambientで取得したチャネルID
ambient_wkey='0123456789abcdef'                 # ここにはライトキーを入力
amdient_tag='d1'                                # データ番号d1～d8のいずれか

import network                                  # ネットワーク通信ライブラリ
import urequests                                # HTTP通信ライブラリ
from sys import exit                            # sysからexitを組み込む
from machine import ADC, Pin, lightsleep, reset # Pinやlightsleep等を組み込む
from time import sleep                          # timeからsleepを組み込む

url = 'http://ambidata.io/api/v2/channels/'+ambient_chid+'/data' # アクセス先
head = {'Content-Type':'application/json'}      # ヘッダを変数head_dictへ
body = {'writeKey':ambient_wkey, amdient_tag:0.0} # 内容を変数bodyへ

led = Pin("LED", Pin.OUT)                       # Pico W LED用ledを生成
wlan = network.WLAN(network.STA_IF)             # Wi-Fi接続用インスタンス生成
wlan.active(True)                               # Wi-Fiの起動
wlan.connect(SSID, PASS)                        # 無線LANに接続
while not wlan.isconnected():                   # 接続待ち
    print('.', end='')                          # 接続中表示
    led.toggle()                                # LEDの点灯／非点灯の反転
    sleep(1)                                    # 1秒間の待ち時間処理
print(wlan.ifconfig()[0])                       # IPアドレスを表示

adc = ADC(4)                                    # 温度センサ用ADCポートadc生成
while True:                                     # 繰り返し処理
    val = adc.read_u16()                        # ADC値を取得して変数valに代入
    mv = val * 3300 / 65535                     # ADC値を電圧(mV)に変換
    temp = 27 - (mv - 706) / 1.721              # ADC電圧値を温度(℃)に変換
    temp_s = str(round(temp,1))                 # 小数点第1位で丸めて文字列に
    print('Temperature =',temp_s,end=',')       # 温度を表示する
    body[amdient_tag] = temp                    # 辞書型変数body内に埋め込む
    led.value(1)                                # LEDを点灯
    try:                                        # 例外処理の監視を開始
        res = urequests.post(url, json=body, headers=head) # HTTPリクエスト送信
        print(' HTTP Stat =', res.status_code)
    except Exception as e:                      # 例外処理発生時
        print(e)                                # エラー内容を表示
    res.close()                                 # ソケットの切断
    led.value(0)                                # LEDを消灯
    lightsleep(30000)                           # 送信間隔用の待ち時間処理

###############################################################################
# 参考文献 1 ESP32 マイコン用 MicroPython プログラム
'''
    https://bokunimo.net/iot/cq/esp32.pdf
'''
###############################################################################
# 参考文献 2 Raspberry Pi Pico のシリアルCOMが表示されないときの修復方法
'''
    https://bokunimo.net/blog/raspberry-pi/1460/
'''
###############################################################################
# 引用コード 本プログラムは下記のコードを変更して作成したものです
''' 
    # IoT連携 Ambientへ送信 HTTP POST μrequests for MicroPython (μrequests使用)
    # Copyright (c) 2019 Wataru KUNINO
    https://github.com/bokunimowakaru/iot/blob/master/micropython/esp32/test_htpost_ambient.py
'''
