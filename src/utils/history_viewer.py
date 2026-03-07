import pandas as pd
import os
from sqlalchemy import create_engine


def fetch_warroom_history():

    DB_URI = (
        f"postgresql+psycopg://{os.getenv('PSQL_USERNAME')}:"
        f"{os.getenv('PSQL_PASSWORD')}@"
        f"{os.getenv('PSQL_HOST')}:"
        f"{os.getenv('PSQL_PORT')}/"
        f"{os.getenv('PSQL_DATABASE')}"
    )

    engine = create_engine(DB_URI)

    query = """
    SELECT thread_id,
           checkpoint_id,
           metadata,
           ts
    FROM checkpoints
    ORDER BY ts DESC
    LIMIT 20
    """

    df = pd.read_sql(query, engine)

    return df