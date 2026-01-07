import logging

from config import settings
from src.analysis.modeling import ModelPipeline
from src.analysis.visualization import RentalDataVisualizer
from src.processing.cleaning import DataCleaner
from src.spiders.spider import LianJiaSpider


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%H:%M:%S'
    )

def check_missing_cities() -> dict:
    existing_files = list(settings.DATA_DIR.glob("raw_*.csv"))

    existing_names = set()
    for p in existing_files:
        parts = p.stem.split('_')
        existing_names.add(parts[1])

    missing_cities = {}
    for code, name in settings.CITIES_MAP.items():
        if name not in existing_names:
            missing_cities[code] = name

    return missing_cities

def main():
    setup_logging()

    logger = logging.getLogger(__name__)

    missing_cities = check_missing_cities()

    if missing_cities:
        logger.info(f">>> 阶段 1/4: 开始爬取 (目标: {list(missing_cities.values())})")
        LianJiaSpider().run(missing_cities)
    else:
        logger.info(">>> 阶段 1/4: 数据已完整，跳过爬取")

    logger.info(">>> 阶段 2/4: 数据清洗")
    df_clean = DataCleaner.execute_task()

    logger.info(">>> 阶段 3/4: 数据可视化")
    RentalDataVisualizer(df_clean).run()

    logger.info(">>> 阶段 4/4: 价格预测建模")
    ModelPipeline(df_clean).run()

if __name__ == '__main__':
    main()