from datetime import date

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from app.db import BASE, engine, Session


class CompaniesPage(BASE):

    __tablename__ = 'parser_actions_urls'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(sa.Text)
    CITY: Mapped[str] = mapped_column(sa.String(120), nullable=True)
    CITY_CHEK: Mapped[int]


class ParsedData(BASE):

    __tablename__ = 'parser_actions'

    ID: Mapped[int] = mapped_column(primary_key=True)
    NAME: Mapped[str] = mapped_column(sa.String(120), nullable=True)
    IMAGES: Mapped[str] = mapped_column(sa.Text, nullable=True)
    DATE_START: Mapped[date]
    DATE_FINISH: Mapped[date]
    IMPORTED: Mapped[str] = mapped_column(
        sa.String(120),
        nullable=True,
        default=None
    )
    ID_ACTION: Mapped[int]
    PAGES: Mapped[int]
    CITY: Mapped[str] = mapped_column(sa.String(120), nullable=True)
    CITY_CHEK: Mapped[int]
    COMPANY: Mapped[str] = mapped_column(sa.String(120), nullable=True)


if __name__ == '__main__':
    BASE.metadata.create_all(bind=engine)
