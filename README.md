# pico

This repository "Wireless Communication Code Examples for Raspberry Pi Pico W, by [bokunimo.net](https://bokunimo.net/)" is a collection of the code examples.  
It includes MicroPython code for the micro IoT sensor devices which send sensor values via UDP and a micro LCD device which receives from them to display the sensor values on it.  

## ボクにもわかる μIoT for Raspberry Pi Pico W 		

MicroPython を使った Raspberry Pi Pico W の学習用サンプル・プログラム集です。

![Raspberry Pi Pico W](https://bokunimo.net/blog/wp-content/uploads/2023/04/DSC_2562wide.jpg)

* example01_hello.py  
	LED Control Example Code for Learning MicroPython  
	Raspberry Pi Pico W の動作確認 Lチカ＋ログ出力表示  
* example02_temp.py  
	Get Value of Internal CPU Temperature Sensor  
	温度を測定してシリアルモニタに表示  
* example03_temp_udp.py  
	Micro IoT Transmitter for Temperature Sensor  
	μIoT 温度計; 温度をUDPで送信  
* example04_hum_udp.py  
	Micro IoT Transmitter for Humidity Sensor  
	μIoT 温湿度計; 温度と湿度をUDPで送信  
* example05_lcd_udp.py  
	Micro IoT LCD Monitor for Micro IoT Sensors  
	UDPを受信してLCDに表示  
* example05_lcd_udp_pg.py  
	Added Ping Function to example05_lcd_udp  
	UDPを受信してLCDに表示(Ping併用版)  
* example06_temp_ambi.py  
	Micro IoT Transmitter using HTTP Client  
	温度値を [Ambient](https://ambidata.io/) に送信  

## bokunimo.net Blog Site

- 解説ページ(bokunimo.netのブログ内)：  
	[https://bokunimo.net/blog/raspberry-pi/3494](https://bokunimo.net/blog/raspberry-pi/3494)  
- Google Transrate to English：  
	[https://bokunimo.net/blog/raspberry-pi/3494](https://bokunimo-net.translate.goog/blog/raspberry-pi/3494/?_x_tr_sl=ja&_x_tr_tl=en)  

The picture below is a example of a micro IoT sensor on a breadboard.  

![μIoT 温湿度計](https://bokunimo.net/blog/wp-content/uploads/2023/04/DSC_0048wide.jpg)  

Following picture is the receiver for the above board. The sensor values which send from the micro IoT Sensors are displayed on the LCD.  

![μIoT LCD](https://bokunimo.net/blog/wp-content/uploads/2023/04/DSC_0034wide.jpg)  

--------------------------------------------------------------------------------
## 関連書籍

本稿の基となる MicroPython 用プログラムは、「Pythonで作るIoTシステム プログラム・サンプル集 (CQ出版社)」の第8章～第9章で解説しています(執筆時点で未発売だったPico Wの記事はありません)。  

### CQ出版社の販売サイト：  

Pythonで作るIoTシステム プログラム・サンプル集  
https://shop.cqpub.co.jp/hanbai/books/MTR/MTRZ202112.html  
- 上記の販売サイトに目次などが紹介されています。  
- クレジットカード支払いの場合、送料無料です。  
- The Book Written in Japanese Language  

### 筆者サポートサイト：  

Pythonで作るIoTシステム プログラム・サンプル集  
https://bokunimo.net/iot/cq/  

----------------------------------------------------------------

## GitHub Pages (This Document)
* [https://git.bokunimo.com/pico/](https://git.bokunimo.com/pico/)  

----------------------------------------------------------------

# git.bokunimo.com GitHub Pages site
[http://git.bokunimo.com/](http://git.bokunimo.com/)  

----------------------------------------------------------------
