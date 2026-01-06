import logging

import plotly.graph_objects as go

from config import settings

logger = logging.getLogger(__name__)

class ImageUtil:
    @staticmethod
    def save_plot(
            fig: go.Figure,
            filename: str,
            fmt: str = 'png',
            scale: float = 2.0
    ) -> str:
        output_dir = settings.IMAGE_DIR

        file_path = output_dir / f"{filename}.{fmt}"

        try:
            if fmt == 'html':
                fig.write_html(str(file_path))
            else:
                fig.write_image(str(file_path), scale=scale)

            return str(file_path)
        except Exception as e:
            return ""