"""
Standalone DB helpers module with no dependencies on libs.* to avoid circular imports.
"""
import os
import functools
from typing import Dict, Any, Iterable, Tuple, Optional
import mysql.connector

CONF_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf', 'bot.conf')


def _strip_quotes(val: str) -> str:
    val = val.strip()
    if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
    return val


class DBHelpers:
    @staticmethod
    def load_conf(path: str = CONF_PATH) -> Dict[str, str]:
        conf: Dict[str, str] = {}
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                key, val = line.split('=', 1)
                conf[key.strip()] = _strip_quotes(val)
        return conf

    @staticmethod
    @functools.lru_cache(maxsize=1)
    def db_conf() -> Dict[str, str]:
        return DBHelpers.load_conf()

    @staticmethod
    def get_conn() -> mysql.connector.MySQLConnection:
        conf = DBHelpers.db_conf()
        db_host = conf.get('DB_HOST', 'localhost')
        db_user = conf.get('DB_USER', 'discord_bot')
        db_pass = conf.get('DB_PASSWORD')
        db_name = conf.get('DB_NAME', 'discord_bot')
        if not db_pass:
            raise RuntimeError('DB_PASSWORD in conf/bot.conf is required to use the database')
        return mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name,
            charset='utf8mb4'
        )

    @staticmethod
    def fetch_one(query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Tuple[Any, ...]]:
        conn = DBHelpers.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def fetch_all(query: str, params: Optional[Tuple[Any, ...]] = None) -> Iterable[Tuple[Any, ...]]:
        conn = DBHelpers.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def execute(query: str, params: Optional[Tuple[Any, ...]] = None) -> None:
        conn = DBHelpers.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
            conn.commit()
        finally:
            conn.close()

