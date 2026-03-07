from langgraph.checkpoint.postgres import PostgresSaver
import os
from urllib.parse import quote_plus


username = os.getenv("PSQL_USERNAME")
password = quote_plus(os.getenv("PSQL_PASSWORD"))  # encode special chars
host = os.getenv("PSQL_HOST")
port = os.getenv("PSQL_PORT")
database = os.getenv("PSQL_DATABASE")

DB_URI = f"postgresql://{username}:{password}@{host}:{port}/{database}"


def get_checkpointer():

    checkpointer_cm = PostgresSaver.from_conn_string(DB_URI)

    class CheckpointerWrapper:
        def __enter__(self):
            self.checkpointer = checkpointer_cm.__enter__()
            self.checkpointer.setup()  # create tables
            return self.checkpointer

        def __exit__(self, exc_type, exc_val, exc_tb):
            return checkpointer_cm.__exit__(exc_type, exc_val, exc_tb)

    return CheckpointerWrapper()