import logging
import re
from datetime import datetime, timedelta

import pandas as pd

from src.utils.csv_util import CsvUtil

logger = logging.getLogger(__name__)


class DataCleaner:
    COLS_TEXT = [
        'city', 'title', 'rent_type', 'district', 'sub_district',
        'community', 'orientation', 'floor_level', 'tags',
        'platform', 'update_time', 'price_rmb'
    ]
    COLS_NUM = ['area_sqm', 'bedrooms', 'living_rooms', 'bathrooms', 'total_floors']

    _PATTERN_PRICE = re.compile(r'(\d+\.?\d*)')
    _PATTERN_REL_DATE = re.compile(r'(\d+)\s*(天|周|个月|月|年)前')
    _DATE_OFFSET_MAP = {'天': 1, '周': 7, '月': 30, '年': 365}

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.now = datetime.now()

    @classmethod
    def execute_task(cls) -> pd.DataFrame:
        raw_df = CsvUtil.load_data("raw", merge_pattern=True)

        if raw_df is None or raw_df.empty:
            logger.warning("跳过清洗：无原始数据")
            return pd.DataFrame()

        cleaner = cls(raw_df)
        cleaned_df = cleaner.process()

        CsvUtil.save_data(cleaned_df, prefix='cleaned')
        return cleaned_df

    def process(self) -> pd.DataFrame:
        initial_len = len(self.df)
        logger.info(f"开始清洗，原始数据量: {initial_len}")

        self.df = (
            self.df
            .pipe(self._clean_text)
            .pipe(self._clean_numeric)
            .pipe(self._parse_prices)
            .pipe(self._standardize_dates)
            .pipe(self._remove_outliers)
        )

        dropped = initial_len - len(self.df)
        logger.info(f"清洗完成: {initial_len} -> {len(self.df)} (剔除 {dropped} 条)")
        return self.df

    def _clean_text(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = df.columns.intersection(self.COLS_TEXT)

        df[cols] = df[cols].fillna('未知').astype(str).apply(lambda x: x.str.strip())
        df[cols] = df[cols].replace(r'^(nan|NaN|None|NULL|)$', '未知', regex=True)

        return df

    def _clean_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = df.columns.intersection(self.COLS_NUM)

        for col in cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        return df

    def _parse_prices(self, df: pd.DataFrame) -> pd.DataFrame:
        def _calc_stats(val: str) -> pd.Series:
            raw_nums = self._PATTERN_PRICE.findall(str(val))
            nums = []
            for x in raw_nums:
                nums.append(float(x))
            if not nums:
                return pd.Series([0.0, 0.0, 0.0])
            return pd.Series([min(nums), max(nums), sum(nums) / len(nums)])

        stats = df['price_rmb'].apply(_calc_stats)
        stats.columns = ['price_min', 'price_max', 'price_avg']

        return pd.concat([df, stats], axis=1)

    def _standardize_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        def _parse(date_str: str) -> str:
            if '今天' in date_str:
                return self.now.strftime('%Y-%m-%d')

            match = self._PATTERN_REL_DATE.search(date_str)
            if match:
                val, unit = match.groups()
                unit_key = unit.replace('个', '')
                days = int(val) * self._DATE_OFFSET_MAP.get(unit_key, 0)
                return (self.now - timedelta(days=days)).strftime('%Y-%m-%d')

            return date_str

        df['clean_date'] = df['update_time'].apply(_parse)

        return df

    def _remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[df['price_avg'] > 0]

        if df.empty:
            return df

        low = df['price_avg'].quantile(0.03)
        high = df['price_avg'].quantile(0.97)

        return df[(df['price_avg'] >= low) & (df['price_avg'] <= high)]