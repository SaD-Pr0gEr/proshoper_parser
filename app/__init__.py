import os.path

import requests

from app.db import Session
from app.db.handlers import get_all_companies, filter_actions
from app.db.models import ParsedData
from app.parsers.bs4.action_page import ActionPageParser
from app.parsers.bs4.catalog_page import CatalogParser
from app.parsers.interfaces.action import ActionPhoto
from app.parsers.interfaces.catalog import CatalogData
from config import config


def app():
    companies = get_all_companies()
    for company in companies:
        response = requests.get(company.url)
        catalog_parser = CatalogParser(response.text)
        catalogs = catalog_parser.parse_catalogs_block()
        company_name = catalog_parser.parse_company_name()
        for catalog in catalogs:
            parsed_catalog = catalog_parser.parse_catalog_data(catalog)
            action_check = filter_actions(ID_ACTION=parsed_catalog.ACTION_ID)
            if action_check:
                continue
            ACTION_DIR = config.parser.PHOTOS_DIR / str(
                parsed_catalog.ACTION_ID
            )
            if not os.path.exists(
                ACTION_DIR
            ):
                os.mkdir(ACTION_DIR)
            action_page = requests.get(
                config.parser.PARSER_SITE_HOST + parsed_catalog.PAGE_LINK
            )
            actions_parser = ActionPageParser(action_page.text)
            photo_links = actions_parser.parse_photo_links()
            photos_data: str = ''
            pages_count = 0
            for id_, link in enumerate(photo_links, start=1):
                photo = ActionPhoto(id_, link)
                db_display_photo_path = photo.load_photo(
                    config.parser.PHOTOS_DIR, parsed_catalog.ACTION_ID
                )
                photos_data += db_display_photo_path + ','
                pages_count += 1
            with Session() as session:
                data = ParsedData(
                    NAME=parsed_catalog.NAME,
                    IMAGES=photos_data,
                    DATE_START=parsed_catalog.DATE_START,
                    DATE_FINISH=parsed_catalog.DATE_FINISH,
                    ID_ACTION=parsed_catalog.ACTION_ID,
                    PAGES=pages_count,
                    CITY=company.CITY,
                    CITY_CHEK=company.CITY_CHEK,
                    COMPANY=company_name
                )
                session.add(data)
                session.commit()
