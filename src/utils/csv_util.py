from pathlib import Path
from typing import Union, List, Optional

import pandas as pd

from config import settings


class CsvUtil:
    @staticmethod
    def save_data(
            data: Union[pd.DataFrame, List[dict]],
            prefix: str,
            city_name: Optional[str] = None
    ) -> Path:
        target_dir = settings.DATA_DIR

        df = pd.DataFrame(data) if not isinstance(data, pd.DataFrame) else data

        filename = f"{prefix}_{city_name}.csv" if city_name else f"{prefix}.csv"
        file_path = target_dir / filename

        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        return file_path

    @staticmethod
    def load_data(
            prefix: str,
            merge_pattern: bool = False
    ) -> Optional[pd.DataFrame]:
        target_dir = settings.DATA_DIR

        if merge_pattern:
            files = list(target_dir.glob(f"{prefix}_*.csv"))
        else:
            files = list(target_dir.glob(f"{prefix}.csv"))

        if not files:
            return None

        try:
            df_list = [pd.read_csv(f, encoding='utf-8-sig') for f in files]

            return pd.concat(df_list, ignore_index=True) if df_list else None
        except Exception as e:
            return None