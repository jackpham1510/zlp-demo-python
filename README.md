# Demo tích hợp ZaloPay cho Python

Demo tích hợp các API của ZaloPay cho python

## Môi trường

* Ubuntu 18.04
* Python 3.6.7

## Cài đặt

1. [front-end](https://github.com/tiendung1510/zlp-demo-frontend)
2. [ngrok](https://ngrok.com/download)
3. [mysql](https://www.mysql.com/downloads/)
4. [python3](https://www.python.org/downloads/)
5. [pip3](https://pip.pypa.io/en/stable/installing/) (Đối với Linux/macOS)
6. Clone project này về

```bash
git clone https://github.com/tiendung1510/zlp-demo-python

cd zlp-demo-python
```

7. Tạo môi trường python ảo (virtual env)

```bash
python3 -m venv env
source env/bin/activate
``` 

- Đối với Linux/macOS cần cài đặt `python3-venv` trước

```bash
sudo apt-get install python3-venv # ubuntu
```

8. Tạo một database mới (`utf8_unicode_ci`) trong mysql và thay đổi cấu hình trong `config.json`

```json
{
  "db": {
    "user": "<username>",
    "password": "<password>",
    "port": 3306,
    "host": "localhost",
    "dbname": "<dbname>"
  }
}
```

## Chạy Project

1. Chạy phần front-end
2. Tạo ngrok public url cho localhost:1789

```bash
ngrok http 1789 # tạo ngrok public url
```

3. Chạy project

```bash
python3 main.py # port 1789
```

## Thay đổi App Config

Khi muốn thay đổi app config (appid, key1, key2, publickey, privatekey), để nhận được callback ở localhost thì **Merchant Server** cần xử lý forward callback như sau:

1. Khi nhận được callback từ ZaloPay Server, lấy **ngrok public url** trong `embeddata.forward_callback` của callback data:

```json
{
  "embeddata": {
    "forward_callback": "<ngrok public url khi chạy lệnh `ngrok http 1789`>"
  }
}
```

2. Post callback data (`application/json`) cho **ngrok public url** vừa lấy

## Các API tích hợp trong demo

* Xử lý callback
* Thanh toán QR
* Cổng ZaloPay
* QuickPay
* Mobile Web to App
* Hoàn tiền
* Lấy trạng thái hoàn tiền