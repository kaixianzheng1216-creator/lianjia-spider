# 链家：https://xm.lianjia.com/zufang/
# 原址：https://github.com/Dyasxue/BUPT_python_final_exp_lianjiaSpider

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
IMAGE_DIR = PROJECT_ROOT / "images"

DATA_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

COOKIE = """lianjia_uuid=21879120-1b21-49b8-ae51-bf462eeea672; crosSdkDT2019DeviceId=-n8sihi-e5a4d0-yh0lk4hhy11ahyr-49vxcihat; ftkrc_=775a8b9e-29c8-4701-9d81-299c3b5bf38c; lfrc_=0794bd25-2752-46e5-999f-f277ab4340ff; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219b4b9589c6d51-049b59bc23a5d88-4c657b58-2073600-19b4b9589c715e0%22%2C%22%24device_id%22%3A%2219b4b9589c6d51-049b59bc23a5d88-4c657b58-2073600-19b4b9589c715e0%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E9%93%BE%E5%AE%B6%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyfs%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoxau%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; select_city=350200; GUARANTEE_POPUP_SHOW=true; GUARANTEE_BANNER_SHOW=true; login_ucid=2000000512872949; lianjia_token=2.00146b5cf64f63e0ef05c675c7c01d6fe3; lianjia_token_secure=2.00146b5cf64f63e0ef05c675c7c01d6fe3; security_ticket=Km1prrtLg0Rg6VBikAI5CXZQJqbJqniEkzfZBIAFsRUKMwzf3ygXT4qIzHEY+m01fEyaWujvPlNDuIIDgRrUWuVJXsRKMYvgVz/tDNPdaYKQ/s6UC9VSeLRjuRnHL9TD2PsfzmQTbaJ77eOSZHdMY01opdG0VPzeFbw10olMk9Y=; lianjia_ssid=e07cfb39-a97c-47bc-a4c7-75311a9b540d; hip=DlrVud7_QcpqSJqmQ1pb9ZK_3mRILkADZ4p7nfsgd_ldNVKpWSNYljrzceIA75Hc6CsFSLFri3HcMvtqKAAcaLrZMsMtAox8c5KYH9fLGvaupn7XDDzy58bbmVb6gAlAn5XLoqufE9apWDqjDYRxlxp8e9GkP14Vd_v0iB-33gopZTwC53PUOJ8-94hvc7xSN6TZGfVg_SThBoKscBNh8n3qk97HF7QDsPKLXnoN07omTUQ_meyk-VXcFlcyT1ZZfNSeiIEA2X9BxK_Ovn_R_MAKYbFvDmQUhCXBGg%3D%3D; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYTZjZDRkMzVmZjE3NjcxOTg5YTFhMzE4NzQ4NGMzZDBmNDMzYzYwNWFlNGM4MjVkMmJhOTdlNmM3NWI3MWUyMjFmZmJkZDdlNTNkNWQzOGQ3MjA0ZmE5MjEwOTA3OGUwNWQ5NzVkMDYyNTJmYjgwYmNiYWQxMGMzNDZmZmFkZDA3OWU0N2JlMGVmMjRmOGI1Mjc4YmIzYWNhYzY2OTNiZGUxMmUwMzFjODBjMTY1M2Q5YTdjOTRiNDMwMGVhYmJjMmJjZjU5ZjBmM2JlMzRkZGMwYTFmNzgzZmJlYjI2MTg2NzhkMDUwZjFmMTIzNjhiMWEyMDE2MDM3NWI1ZmRkYVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIzYTU3Mjg1ZlwifSIsInIiOiJodHRwczovL3htLmxpYW5qaWEuY29tL3p1ZmFuZy8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=="""

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