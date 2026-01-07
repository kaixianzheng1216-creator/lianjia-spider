import logging
from typing import Tuple, List, Dict

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from catboost import CatBoostRegressor, Pool
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder

from src.utils.image_util import ImageUtil

logger = logging.getLogger(__name__)


class ModelPipeline:
    CATEGORICAL_FEATURES = ['city', 'rent_type', 'district', 'sub_district', 'orientation', 'floor_level']
    NUMERIC_FEATURES = ['area_sqm', 'bedrooms', 'living_rooms', 'bathrooms', 'total_floors', 'is_subway']
    TARGET_COLUMN = 'price_avg'

    FEATURE_DISPLAY_MAP = {
        'city': '城市', 'rent_type': '租赁方式', 'district': '行政区',
        'sub_district': '商圈', 'orientation': '朝向', 'floor_level': '楼层等级',
        'area_sqm': '面积(㎡)', 'bedrooms': '室数', 'living_rooms': '厅数',
        'bathrooms': '卫数', 'total_floors': '总楼层', 'is_subway': '是否近地铁'
    }

    COLOR_SEQ = px.colors.qualitative.Plotly

    def __init__(self, raw_df: pd.DataFrame):
        self.all_feature_names = None
        self.raw_df = raw_df
        self.performance_metrics: List[Dict] = []

    def run(self):
        features, target = self._prepare_data()
        self.all_feature_names = features.columns.tolist()

        train_features, test_features, train_target, test_target = train_test_split(
            features, target, test_size=0.2, random_state=42
        )

        logger.info("正在训练 CatBoost 模型...")
        catboost_model = self._train_catboost(train_features, train_target, test_features, test_target)
        self._evaluate(catboost_model, test_features, test_target, "CatBoost")

        logger.info("正在训练 RandomForest 模型...")
        rf_model, test_features_encoded = self._train_random_forest(train_features, train_target, test_features)
        self._evaluate(rf_model, test_features_encoded, test_target, "RandomForest")

        self._plot_metrics_comparison()
        self._plot_importance(catboost_model)

    def _prepare_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        df = self.raw_df.copy()
        df['is_subway'] = df['tags'].str.contains('近地铁', na=False).astype(int)
        return df[self.CATEGORICAL_FEATURES + self.NUMERIC_FEATURES], df[self.TARGET_COLUMN]

    def _train_catboost(self, train_x, train_y, test_x, test_y):
        train_pool = Pool(train_x, train_y, cat_features=self.CATEGORICAL_FEATURES)
        test_pool = Pool(test_x, test_y, cat_features=self.CATEGORICAL_FEATURES)

        model = CatBoostRegressor(
            iterations=1000,
            learning_rate=0.05,
            depth=5,
            loss_function='RMSE',
            verbose=0,
            early_stopping_rounds=50,
            allow_writing_files=False
        )
        model.fit(train_pool, eval_set=test_pool, use_best_model=True)
        return model

    def _train_random_forest(self, train_x, train_y, test_x):
        encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
        train_x_encoded = train_x.copy()
        test_x_encoded = test_x.copy()

        train_x_encoded[self.CATEGORICAL_FEATURES] = encoder.fit_transform(train_x[self.CATEGORICAL_FEATURES])
        test_x_encoded[self.CATEGORICAL_FEATURES] = encoder.transform(test_x[self.CATEGORICAL_FEATURES])

        model = RandomForestRegressor(
            n_estimators=1000,
            max_depth=20,
            n_jobs=-1,
            random_state=42
        )
        model.fit(train_x_encoded, train_y)
        return model, test_x_encoded

    def _evaluate(self, model, features, target, model_name: str):
        target_pred = model.predict(features)
        
        rmse = np.sqrt(mean_squared_error(target, target_pred))
        mae = mean_absolute_error(target, target_pred)
        r2 = r2_score(target, target_pred)

        logger.info(f"模型评估: {model_name}: RMSE={rmse:.3f}, MAE={mae:.3f}, R2={r2:.3f}")

        self.performance_metrics.extend([
            {'Model': model_name, 'Metric': 'RMSE', 'Value': rmse},
            {'Model': model_name, 'Metric': 'MAE', 'Value': mae},
            {'Model': model_name, 'Metric': 'R2', 'Value': r2}
        ])

    def _apply_style(self, fig, title: str):
        fig.update_layout(
            title={'text': title, 'x': 0.5, 'y': 0.95, 'xanchor': 'center', 'yanchor': 'top'},
            template="plotly_white",
            font=dict(family="Microsoft YaHei", size=12),
            margin=dict(l=40, r=40, t=80, b=40),
            showlegend=True
        )
        return fig

    def _plot_metrics_comparison(self):
        metrics_df = pd.DataFrame(self.performance_metrics)
        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=("模型拟合度 (R2)", "误差指标 (RMSE/MAE)")
        )

        r2_df = metrics_df[metrics_df['Metric'] == 'R2']
        fig.add_trace(
            go.Bar(
                x=r2_df['Model'],
                y=r2_df['Value'],
                name='R2 Score',
                text=r2_df['Value'].round(4),
                textposition='auto',
                marker_color=self.COLOR_SEQ[0]
            ),
            row=1,
            col=1
        )

        rmse_df = metrics_df[metrics_df['Metric'] == 'RMSE']
        fig.add_trace(
            go.Bar(
                x=rmse_df['Model'],
                y=rmse_df['Value'],
                name='RMSE',
                marker_color=self.COLOR_SEQ[1]
            ),
            row=1,
            col=2
        )

        mae_df = metrics_df[metrics_df['Metric'] == 'MAE']
        fig.add_trace(
            go.Bar(
                x=mae_df['Model'],
                y=mae_df['Value'],
                name='MAE',
                marker_color=self.COLOR_SEQ[2]
            ),
            row=1,
            col=2
        )

        fig.update_layout(barmode='group')

        self._apply_style(fig, "模型性能评估对比")

        ImageUtil.save_plot(
            fig=fig,
            filename="模型性能对比图"
        )

    def _plot_importance(self, model):
        importance_df = pd.DataFrame({
            'feature': self.all_feature_names,
            'score': model.get_feature_importance()
        })
        importance_df['feature_cn'] = importance_df['feature'].map(self.FEATURE_DISPLAY_MAP)
        importance_df = importance_df.sort_values('score', ascending=True).tail(10)

        fig = px.bar(
            importance_df,
            x='score',
            y='feature_cn',
            orientation='h',
            labels={
                'score': '贡献度指数',
                'feature_cn': '特征名称'
            },
            color='score',
            color_continuous_scale='Viridis'
        )

        fig.update_layout(coloraxis_showscale=False)

        self._apply_style(fig, "CatBoost 核心特征贡献排行")

        ImageUtil.save_plot(
            fig=fig,
            filename="CatBoost 核心特征贡献排行"
        )