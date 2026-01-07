# 链家租房数据爬虫与分析 (Lianjia Spider & Analysis)

本项目是一个全流程的链家租房数据分析工具，包含**数据爬取**、**数据清洗**、**可视化分析**以及**租金预测建模**四个主要阶段。

## 🚀 功能特性

1.  **数据爬取 (Spider)**:
    *   针对链家网租房频道进行数据抓取。
    *   支持多城市配置（北京、上海、广州、深圳、厦门等）。
    *   自动处理分页、反爬限制及 Cookie 管理。
    *   核心代码: `src.spiders.spider.LianJiaSpider`

2.  **数据清洗 (Cleaning)**:
    *   对原始数据进行去重、缺失值处理。
    *   提取数值型特征（面积、价格）。
    *   解析房屋朝向、楼层、地铁距离等结构化信息。
    *   核心代码: `src.processing.cleaning.DataCleaner`

3.  **可视化分析 (Visualization)**:
    *   生成多维度的租房市场分析图表。
    *   包括：区域租金分布、价格区间占比、租金 Top 10 行政区、地铁房对比等。
    *   核心代码: `src.analysis.visualization.RentalDataVisualizer`

4.  **价格预测建模 (Modeling)**:
    *   基于清洗后的数据训练机器学习模型（CatBoost, XGBoost 等）。
    *   预测房源租金，并分析特征重要性。
    *   核心代码: `src.analysis.modeling.ModelPipeline`

## 🛠️ 安装与配置

### 1. 环境准备

确保已安装 Python 3.8+，并安装项目依赖：

```bash
pip install -r requirements.txt
```

### 2. 项目配置

修改 `config/settings.py` 文件以适配你的需求：

*   **COOKIE**: *重要*，请替换为你自己在链家网登录后的 Cookie，以确保爬虫正常运行。
*   **ANALYSIS_CITY**: 设置需要分析的目标城市（如 '厦门', '深圳', '上海' 等）。
*   **CITIES_MAP**: 支持的城市列表映射。

## 🏃‍♂️ 运行项目

直接运行 `main.py` 即可按顺序执行所有阶段：

```bash
python main.py
```

程序将依次执行：
1.  **启动爬虫**: 检查 `data/` 目录下是否已有该城市数据，若无则开始爬取。
2.  **数据清洗**: 处理 `raw_*.csv` 文件，生成清洗后的数据。
3.  **数据可视化**: 在 `images/` 目录下生成分析图表。
4.  **价格预测建模**: 训练模型并输出性能评估。

## 📊 效果示例

运行后将在 `images/` 目录下生成如下可视化结果：

| 区域租金分布 (示例) | 核心特征贡献排行 (示例) |
| :---: | :---: |
| ![区域租金分布](images/上海%20-%20各区域租金分布.png) | ![特征贡献](images/CatBoost%20核心特征贡献排行.png) |

*(注：以上图片需在运行项目后生成)*

## 📂 项目结构

```text
lianjia-spider/
├── config/             # 配置文件 (settings.py)
├── data/               # 数据存储 (raw_*.csv)
├── images/             # 可视化结果输出
├── src/
│   ├── analysis/       # 分析与建模 (modeling, visualization)
│   ├── processing/     # 数据处理 (cleaning)
│   ├── spiders/        # 爬虫逻辑 (spider)
│   └── utils/          # 工具函数
├── main.py             # 程序主入口
├── requirements.txt    # 项目依赖
└── README.md           # 项目说明
```

## ⚠️ 免责声明

本项目仅供学习与技术研究使用。请勿将爬虫用于商业用途或对目标网站造成过度压力。使用本工具产生的任何后果由使用者自行承担。
