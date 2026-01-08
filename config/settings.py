# 链家：https://xm.lianjia.com/zufang/

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
IMAGE_DIR = PROJECT_ROOT / "images"

DATA_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

COOKIE = """lianjia_ssid=4a28a7ab-95c3-4a2a-adb2-614ada8aa564; lianjia_uuid=70e937bd-096c-43b1-876d-c72b58e8a945; crosSdkDT2019DeviceId=g4b33x-e5a4d0-07iwd5eo9m7trtn-38ptqziht; hip=AqseMDeEUD8KnaJz31REUlqEVoAaBOj7ZhKOvpCFlfRS3TlDE-eWH8vGpJgrXmHrygkJVi3BtewtwaW_BNc0KBRz5uE325UkFQNawYoIgGV1vg_GyrX8I8h8yBGOfSD9LUMuCSSYkGx93AvLwasdws2L1DDytuw1VxLjcaGmg0hXDaYQCi9xGxfDHMjhtA6SSsxU9nTKm4ERmnaX7N7PWzh7d5-ZSDsDH5EGOq4XdnElORe-kbYhWEMTq4g%3D; select_city=350200; GUARANTEE_POPUP_SHOW=true; login_ucid=2000000512872949; lianjia_token=2.0013adb9bb48a505a20200908a7396f6a0; lianjia_token_secure=2.0013adb9bb48a505a20200908a7396f6a0; security_ticket=nYOKAMd9n/QpLtgFkorqsClo/Elzf7O8IHDZLiibijk5gnMta1g4DwgwUytslHSsb+Wz1EqewjXZ3po58cIZ0E7LclTtf26iM5PlXgKCKoLr8s6t1sj2LPgvDDhfs5RcTYl5WIQSixY86e/AA2Y6n6Bf4PcQsuq3RCCz6h69MnM=; ftkrc_=a9c712e6-2d9e-44ff-a8a7-8b676f62ef8b; lfrc_=16737aa3-77b2-4858-8626-97a1824f2268; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiODY5ZWMwMWNiMzgwNDUzMTVjNDAwMTQwODU2MjJkODk3NjQyYTVjYTIzYjE2NTE2ZDA1N2UwZTk3ZDRjYTZmMzlhOWJmZDVhZjNlMjY5MTE3OTZlY2Q3YjFjZTYwMzk5MmM4MDM2NzQyNDVmYmYzNGNiZTQ2MGQyMjk2YmE5OWI4NTg3Y2JmMDVhOWU1MmYyNmY0ZWI1NzZmMWY2OGVkZmU1NGM1MGQ5YjJkN2E0ZmZlZmEzNzJjZGIzNWM4M2U0OTVhMDVlNzBmMmM3YjczNDhhNzU2NTc1YmViMmY3ZTAwNzhlMmNmNzc2ZGEwZjc1MWJkYjJjZmMzNzdlYjhmNlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI4MTAzODhmMFwifSIsInIiOiJodHRwczovL3htLmxpYW5qaWEuY29tL3p1ZmFuZy8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==; GUARANTEE_BANNER_SHOW=true"""

CITIES_MAP = {
    'bj': '北京',
    'sh': '上海',
    'gz': '广州',
    'sz': '深圳',
    'wh': '武汉',
    'cd': '成都',
    'hz': '杭州',
    'xm': '厦门'
}

START_PAGE = 1
END_PAGE = 50
MIN_DELAY = 6
MAX_DELAY = 8
MAX_FAILURES = 3

ANALYSIS_CITY = '上海'