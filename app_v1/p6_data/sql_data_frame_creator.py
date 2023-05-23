from pydantic import BaseModel
from typing import Dict, Any
import pandas as pd
import pymssql
import logging
from settings import settings

class SQLParams(BaseModel):
    params: Dict[str, Any]

class SQLDataFrameCreator:
    def __init__(self, query_file: str, params: SQLParams):
        self.host = settings.DB_PRIMAVERA_HOST
        self.port = settings.DB_PRIMAVERA_PORT
        self.user = settings.DB_PRIMAVERA_USERNAME
        self.password = settings.DB_PRIMAVERA_PASSWORD
        self.database = settings.DB_PRIMAVERA_DBNAME
        self.query_file = query_file
        self.params = params.params
        self.logger = logging.getLogger(__name__)

    def get_dataframe(self):
        # Open SQL file
        with open(self.query_file, 'r') as f:
            sql_query = f.read()

        # Replace parameters in SQL query
        for key, value in self.params.items():
            sql_query = sql_query.replace(f'{{{key}}}', str(value))

        # Connect to SQL Server
        with pymssql.connect(server=self.host, port=self.port, user=self.user, password=self.password, database=self.database) as conn:
            try:
                self.logger.info("Running SQL query...")
                df = pd.read_sql_query(sql_query, conn)
                self.logger.info("SQL query successfully run.")
                return df
            except Exception as e:
                self.logger.error("Failed to run SQL query: ", exc_info=True)
                return pd.DataFrame()  # Return empty DataFrame on error
