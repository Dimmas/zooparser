from pydantic import BaseSettings
from typing import Union, List


class Config(BaseSettings):
    CATEGORIES: List[str] = None
    OUT_DIR: str = 'out'
    DELAY: Union[int, list] = 0  # [0, 3]
    MAX_RETRIES: int = 3
    HEADERS: dict = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)"}
    LOG_DIR: str = 'logs'
    RESTART_COUNT: int = 3
    RESTART_INTERVAL: float = 0.1
    PROXIES_COUNT: int = 2
    PROXIES: dict = None
    VSCALE_CID: int = 77935
    VSCALE_API_KEY: str = "10baad3b0420f1006ba991ffda24505821f9ce2ca6c2bb4b44cd348b763135fd"


config = Config()
