import pandas as pd
from typing import Any
import io


def build_db_config_string(db_config: dict) -> str:
    return " ".join([f"{key}='{db_config[key]}'" for key in db_config.keys()])


def insert_data_from_buffer(df: pd.DataFrame, connection: Any):
    with connection.cursor() as cursor:
        buffer = io.StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)
        df_columns = df.columns
        comma_separated_df_columns_str = ", ".join(df_columns)
        cursor.copy_expert(
            f"COPY transactions({comma_separated_df_columns_str}) FROM STDIN (FORMAT 'csv', HEADER false)",
            buffer,
        )
        connection.commit()
