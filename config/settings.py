# 链家：https://xm.lianjia.com/zufang/

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
IMAGE_DIR = PROJECT_ROOT / "images"

DATA_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

COOKIE = """lianjia_uuid=70e937bd-096c-43b1-876d-c72b58e8a945; crosSdkDT2019DeviceId=g4b33x-e5a4d0-07iwd5eo9m7trtn-38ptqziht; login_ucid=2000000512872949; lianjia_token=2.0013adb9bb48a505a20200908a7396f6a0; lianjia_token_secure=2.0013adb9bb48a505a20200908a7396f6a0; security_ticket=nYOKAMd9n/QpLtgFkorqsClo/Elzf7O8IHDZLiibijk5gnMta1g4DwgwUytslHSsb+Wz1EqewjXZ3po58cIZ0E7LclTtf26iM5PlXgKCKoLr8s6t1sj2LPgvDDhfs5RcTYl5WIQSixY86e/AA2Y6n6Bf4PcQsuq3RCCz6h69MnM=; ftkrc_=a9c712e6-2d9e-44ff-a8a7-8b676f62ef8b; lfrc_=16737aa3-77b2-4858-8626-97a1824f2268; lianjia_ssid=d867bba5-c082-45bd-b851-468f79ac30ce; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219b9c0da69b457-092f2ac479eff18-4c657b58-2304000-19b9c0da69c1053%22%2C%22%24device_id%22%3A%2219b9c0da69b457-092f2ac479eff18-4c657b58-2304000-19b9c0da69c1053%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; hip=__qqy8va5t686dQ0QeT2MQDo-OmYsizGk6E13qzXRPfAz46uO5WBUa6hi7riGb-Ml11a7fUMPIv_JKVMIxikMMoaW6Rx8AC74e8OAKQ6cxWHQpvon43Hmlq7pvd7v9MTe4Sabeo8jtj2diluIqfm0eGKBbtsbBU7q6SqHjgR5QFc_7ecdqZO9aWZjH4OhRsO9kiR0IruurJYoePZNIq30Ben9ascT-D-6Fc8KcIbrFshhAPkbyxtnWgp9GQRwGk2ZR-bP6zBapx9ehgbsdFlU_ksf5tfN3Zin3Z-_w%3D%3D; select_city=340800; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiODY5ZWMwMWNiMzgwNDUzMTVjNDAwMTQwODU2MjJkODk3NjQyYTVjYTIzYjE2NTE2ZDA1N2UwZTk3ZDRjYTZmMzlhOWJmZDVhZjNlMjY5MTE3OTZlY2Q3YjFjZTYwMzk5MmM4MDM2NzQyNDVmYmYzNGNiZTQ2MGQyMjk2YmE5OWI4NTg3Y2JmMDVhOWU1MmYyNmY0ZWI1NzZmMWY2OGVkZjUxOTk4MTE3NzZkNWI5ZTBmM2VlNDc3YzBiNmY2YTZhMzcyNzczNjFjN2RhMzk3NzEyMzVkMzdjZGY1YjI5ZTViZWM2NDZjMTJlZDBlMjE5Y2JlODNlOGYzMWExZTYwMFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJkZjk4MmVmNVwifSIsInIiOiJodHRwczovL2FxLmxpYW5qaWEuY29tL3p1ZmFuZy8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=="""

CITIES_MAP = {
    'bj': '北京',
    'sh': '上海',
    'gz': '广州',
    'sz': '深圳',
    'tj': '天津',
    'cd': '成都',
    "nj": '南京',
    'hz': '杭州',
    'qd': '青岛',
    'sy': '沈阳',
    'xm': '厦门',
    'wh': '武汉',
}

START_PAGE = 1
END_PAGE = 50
MIN_DELAY = 6
MAX_DELAY = 8
MAX_FAILURES = 3

ANALYSIS_CITY = '上海'
