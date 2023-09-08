from dataclasses import dataclass
from datetime import date


@dataclass
class CatalogData:
    NAME: str
    DATE_START: date
    DATE_FINISH: date
    PAGES: int
    ACTION_ID: int
    PAGE_LINK: str
