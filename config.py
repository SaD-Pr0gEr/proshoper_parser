import os.path
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class DbConfig:
    type: str
    port: int
    host: str

    @property
    def db_url(self):
        raise NotImplementedError


@dataclass
class MySqlConfig(DbConfig):
    username: str
    password: str
    db_name: str

    @property
    def db_url(self):
        return (f'{self.type}+pymysql://{self.username}:{self.password}'
                f'@{self.host}:{self.port}/{self.db_name}')


@dataclass
class Parser:
    PARSER_SITE_HOST: str = 'https://proshoper.ru'
    BASE_DIR: Path = Path(__file__).parent
    PHOTOS_DIR: Path = BASE_DIR.parent / 'media/public_html/actions'

    def __post_init__(self):
        if not os.path.exists(self.PHOTOS_DIR):
            os.makedirs(self.PHOTOS_DIR)


@dataclass
class Config:
    db_conf: MySqlConfig
    parser: Parser


def load_config(env_path: str | Path,
                parser_conf: Parser | None = None) -> Config:
    load_dotenv(env_path)
    return Config(
        MySqlConfig(
            type='mysql',
            port=int(os.getenv('DB_PORT')),
            host=os.getenv('DB_HOST'),
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db_name=os.getenv('DB_NAME'),
        ),
        Parser() if not parser_conf else parser_conf
    )


config = load_config('.env')
