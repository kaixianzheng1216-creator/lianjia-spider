import logging
import random
import re
import time
from typing import Dict, List, Any, Optional

import requests
from bs4 import BeautifulSoup, Tag
from fake_useragent import UserAgent

from config import settings
from src.utils.csv_util import CsvUtil

logger = logging.getLogger(__name__)


class LianJiaSpider:
    _PATTERNS = {
        'layout': re.compile(r'(\d+)室(\d+)厅(\d+)卫'),
        'area': re.compile(r'(\d+\.?\d*)㎡'),
        'orientation': re.compile(r'/\s*([\u4e00-\u9fa5\s]+)\s*/'),
        'floor_level': re.compile(r'([\u4e00-\u9fa5]+)楼层'),
        'total_floors': re.compile(r'（(\d+)层）')
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': UserAgent().random,
            'Cookie': settings.COOKIE
        })

    def run(self, specific_cities):
        for city_code, city_name in specific_cities.items():
            data = self._crawl_city(city_name, city_code)
            CsvUtil.save_data(data, prefix='raw', city_name=city_name)

    def _crawl_city(self, city_name: str, city_code: str) -> List[Dict]:
        logger.info(f">>> 启动抓取: {city_name} ({city_code})")
        items = []
        consecutive_failures = 0

        for page in range(settings.START_PAGE, settings.END_PAGE + 1):
            logger.info(f"[{city_name}] 正在处理第 {page} 页...")

            page_data = self._fetch_page(city_code, page, city_name)

            if page_data:
                items.extend(page_data)
                consecutive_failures = 0
                logger.info(f"    √ 获取 {len(page_data)} 条")
            else:
                consecutive_failures += 1
                logger.info(f"    × 第 {page} 页无数据")

            if consecutive_failures >= settings.MAX_FAILURES:
                logger.error(f"连续失败触发熔断: {city_name}")
                exit(1)

            time.sleep(random.uniform(settings.MIN_DELAY, settings.MAX_DELAY))

        return items

    def _fetch_page(self, city_code: str, page: int, city_name: str) -> List[Dict]:
        url = f"https://{city_code}.lianjia.com/zufang/pg{page}/"

        try:
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.content, 'html.parser')
            cards = soup.select('div.content__list--item')

            results = []
            for card in cards:
                results.append(self._parse_card(card, city_name))
            return results
        except Exception as e:
            logger.error(f"请求异常 (Page {page}): {e}")
            return []

    def _parse_card(self, card: Tag, city_name: str) -> Dict[str, Any]:
        def _text(selector: str) -> str:
            el = card.select_one(selector)
            return el.get_text(strip=True) if el else ""

        def _regex(text: str, key: str, dtype: type = str, default: Any = None) -> Any:
            match = self._PATTERNS[key].search(text)
            if match:
                try:
                    return dtype(match.group(1)) if match.lastindex == 1 else match.groups()
                except (ValueError, IndexError):
                    pass
            return default

        desc = _text('p.content__list--item--des')
        floor_txt = _text('p.content__list--item--des span.hide')
        title = _text('p.content__list--item--title')

        locs = []
        for a in card.select('p.content__list--item--des a')[:3]:
            locs.append(a.get_text(strip=True))
        
        # padding
        for _ in range(3 - len(locs)):
            locs.append('')

        layout = self._PATTERNS['layout'].search(desc)
        rooms = [0, 0, 0]
        if layout:
            rooms = []
            for x in layout.groups():
                rooms.append(int(x))

        price_str = _text('span.content__list--item-price em')
        tag_texts = []
        for i in card.select('p.content__list--item--bottom i'):
            tag_texts.append(i.get_text(strip=True))
        tags = '|'.join(tag_texts)

        return {
            'city': city_name,
            'title': title,
            'rent_type': '整租' if '整租' in title else ('合租' if '合租' in title else '独栋'),
            'district': locs[0],
            'sub_district': locs[1],
            'community': locs[2],
            'area_sqm': _regex(desc, 'area', float, 0.0),
            'bedrooms': rooms[0],
            'living_rooms': rooms[1],
            'bathrooms': rooms[2],
            'orientation': _regex(desc, 'orientation', str, '').strip(),
            'floor_level': _regex(floor_txt, 'floor_level', str, ''),
            'total_floors': _regex(floor_txt, 'total_floors', int, 0),
            'tags': tags,
            'platform': _text('p.content__list--item--brand span.brand'),
            'update_time': _text('p.content__list--item--brand span.content__list--item--time'),
            'price_rmb': price_str
        }