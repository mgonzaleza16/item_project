import logging
from typing import List
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dataclasses import dataclass
from contextlib import contextmanager

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PostgresUpdater:
    """
    Una clase que recibe:
        un dataframe,
        nombre de tabla y esquema,
        una lista de columnas de clave primaria,
        una lista de columnas para actualizar,
        nombre de tabla temporal.

    La clase puede insertar datos en la tabla temporal usando
    copy_expert, insertar datos en la tabla final desde la tabla temporal,
    actualizar datos, eliminar datos que no están en la tabla temporal,
    eliminar la tabla temporal, cerrar la conexión y hacer un rollback en caso de error en la tabla.
    """
    df: pd.DataFrame
    table_name: str
    schema_name: str
    pk_cols: List[str]
    update_cols: List[str]
    temp_table_name: str

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    @contextmanager
    def database_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            yield conn
        except Exception as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            raise
        finally:
            if conn:
                conn.close()

    @contextmanager
    def database_cursor(self):
        with self.database_connection() as conn:
            cur = None
            try:
                cur = conn.cursor()
                yield cur
            except Exception as e:
                logger.error(f"Error al obtener el cursor de la base de datos: {e}")
                conn.rollback()
                raise
            finally:
                if cur:
                    cur.close()

    def insert_data_to_temp_table(self):
        """
        Inserta datos en la tabla temporal utilizando copy_expert.
        """
        self.df.to_csv(f'{self.temp_table_name}.csv', index=False, header=False)
        with self.database_cursor() as cur:
            try:
                cur.execute(f"CREATE TEMP TABLE {self.temp_table_name} (LIKE {self.schema_name}.{self.table_name} INCLUDING DEFAULTS) ON COMMIT DROP;")
                with open(f'{self.temp_table_name}.csv', 'r') as f:
                    cur.copy_expert(f'COPY {self.temp_table_name} FROM STDIN DELIMITER \',\' CSV HEADER', f)
                cur.connection.commit()
            except Exception as e:
                logger.error(f"Error al insertar datos en la tabla temporal: {e}")
                cur.connection.rollback()
                raise

    def insert_data_to_final_table(self):
        """
        Inserta datos en la tabla final desde la tabla temporal.
        """
        with self.database_cursor() as cur:
            try:
                cur.execute(f"INSERT INTO {self.schema_name}.{self.table_name} SELECT * FROM {self.temp_table_name} "
                            f"ON CONFLICT ({', '.join(self.pk_cols)}) DO UPDATE SET "
                            f"{', '.join([f'{col}=excluded.{col}' for col in self.update_cols])};")
                cur.connection.commit()
            except Exception as e:
                logger.error(f"Error al insertar datos en la tabla final: {e}")
                cur.connection.rollback()
                raise

    def delete_data_not_in_temp_table(self):
        """
        Elimina datos de la tabla final que no están en la tabla temporal.
        """
        with self.database_cursor() as cur:
            try:
                cur.execute(f"DELETE FROM {self.schema_name}.{self.table_name} WHERE NOT EXISTS "
                            f"(SELECT 1 FROM {self.temp_table_name} "
                            f"WHERE {self.table_name}.{self.pk_cols[0]}={self.temp_table_name}.{self.pk_cols[0]} "
                            f"AND {self.table_name}.{self.pk_cols[1]}={self.temp_table_name}.{self.pk_cols[1]})")
                cur.connection.commit()
            except Exception as e:
                logger.error(f"Error al eliminar datos no presentes en la tabla temporal: {e}")
                cur.connection.rollback()
                raise

    def drop_temp_table(self):
        """
        Elimina la tabla temporal.
        """
        with self.database_cursor() as cur:
            try:
                cur.execute(f"DROP TABLE IF EXISTS {self.temp_table_name}")
                cur.connection.commit()
            except Exception as e:
                logger.error(f"Error al eliminar la tabla temporal: {e}")
                cur.connection.rollback()
                raise
