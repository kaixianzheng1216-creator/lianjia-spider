import logging
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import settings
from src.utils.image_util import ImageUtil

logger = logging.getLogger(__name__)


class RentalDataVisualizer:
    LABELS_MAP = {
        'city': '城市',
        'price_avg': '月租均价 (元)',
        'price_per_sqm': '每平米单价 (元/㎡)',
        'is_subway': '房源类型',
        'district': '行政区',
        'count': '房源数量',
        'range': '价格区间'
    }

    COLOR_SEQ = px.colors.qualitative.Plotly

    def __init__(self, df: pd.DataFrame):
        self.df = df[df['district'] != '未知'].copy()

        self.df['price_per_sqm'] = self.df['price_avg'] / self.df['area_sqm']

        self.df['is_subway'] = np.where(
            self.df['tags'].str.contains('近地铁'), '地铁房', '普通房'
        )

    def run(self):
        logger.info("开始生成数据可视化图表...")

        self._plot_city_comparison()
        self._plot_subway_premium()

        target_city = settings.ANALYSIS_CITY
        city_data = self.df[self.df['city'] == target_city]

        if city_data.empty:
            logger.warning(f"未找到城市 {target_city} 的数据，跳过该城市深度分析图表")
            return

        self._plot_district_price_distribution(city_data, target_city)
        self._plot_district_top10(city_data, target_city)
        self._plot_price_segments(city_data, target_city)

        logger.info("所有图表已保存完成。")

    def _apply_style(self, fig, title: str):
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'y': 0.95,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            template="plotly_white",
            font=dict(family="Microsoft YaHei", size=12),
            margin=dict(l=40, r=40, t=80, b=40),
            showlegend=True
        )
        return fig

    def _plot_city_comparison(self):
        metrics = (
            self.df
            .groupby('city')[['price_avg', 'price_per_sqm']]
            .mean()
            .reset_index()
        )

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Bar(
                x=metrics['city'],
                y=metrics['price_avg'],
                name="月租均价",
                marker_color=self.COLOR_SEQ[0],
            ),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(
                x=metrics['city'],
                y=metrics['price_per_sqm'],
                name="每平米单价",
                mode='lines+markers',
                line=dict(color=self.COLOR_SEQ[1], width=3)
            ),
            secondary_y=True
        )

        fig.update_yaxes(title_text="月租均价 (元)", secondary_y=False)
        fig.update_yaxes(title_text="每平米单价 (元/㎡)", secondary_y=True, showgrid=False)
        fig.update_xaxes(title_text="城市")

        self._apply_style(fig, "各城市租金水平对比")

        ImageUtil.save_plot(fig, "各城市租金水平对比")

    def _plot_subway_premium(self):
        metrics = (
            self.df
            .groupby('is_subway')['price_avg']
            .mean()
            .reset_index()
        )

        fig = px.bar(
            metrics,
            x='is_subway',
            y='price_avg',
            labels=self.LABELS_MAP,
            color='is_subway',
            color_discrete_sequence=self.COLOR_SEQ,
            text_auto='.2f'
        )

        fig.update_traces(textposition='outside')

        self._apply_style(fig, "地铁房 vs 普通房：月租均价对比")

        ImageUtil.save_plot(fig, "地铁房 vs 普通房：月租均价对比")

    def _plot_district_price_distribution(self, df: pd.DataFrame, city: str):
        fig_box = px.box(
            df,
            x='district',
            y='price_avg',
            labels=self.LABELS_MAP,
            color='district',
            color_discrete_sequence=self.COLOR_SEQ
        )

        fig_box.update_xaxes(categoryorder='median ascending')

        self._apply_style(fig_box, f"{city} - 各区域租金分布")

        ImageUtil.save_plot(fig_box, f"{city} - 各区域租金分布")

    def _plot_district_top10(self, df: pd.DataFrame, city: str):
        top10 = (
            df
            .groupby('district')['price_avg']
            .mean()
            .nlargest(10)
            .reset_index()
        )

        fig_bar = px.bar(
            top10,
            x='price_avg',
            y='district',
            orientation='h',
            labels=self.LABELS_MAP,
            color='price_avg',
            color_continuous_scale='Blues'
        )

        fig_bar.update_yaxes(autorange="reversed")

        self._apply_style(fig_bar, f"{city} - 租金最贵行政区 Top 10")

        ImageUtil.save_plot(fig_bar, f"{city} - 租金最贵行政区 Top 10")

    def _plot_price_segments(self, df: pd.DataFrame, city: str):
        bins = [0, 2000, 4000, 6000, 8000, 10000, float('inf')]
        labels = ['2k以下', '2k-4k', '4k-6k', '6k-8k', '8k-1w', '1w以上']

        counts = pd.cut(df['price_avg'], bins=bins, labels=labels).value_counts().reset_index()
        counts.columns = ['range', 'count']

        fig = px.pie(
            counts,
            values='count',
            names='range',
            labels=self.LABELS_MAP,
            color_discrete_sequence=self.COLOR_SEQ,
            hole=0.4
        )

        fig.update_traces(textposition='inside', textinfo='percent+label')

        self._apply_style(fig, f"{city} - 房源价格区间占比")

        ImageUtil.save_plot(fig, f"{city} - 房源价格区间占比")