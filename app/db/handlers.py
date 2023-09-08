from app.db import Session
from app.db.models import CompaniesPage, ParsedData


def get_all_companies() -> list[CompaniesPage]:
    with Session() as session:
        actions = session.query(CompaniesPage).all()
    return actions


def filter_actions(**filter_data) -> list[ParsedData]:
    with Session() as session:
        actions = session.query(ParsedData).filter_by(**filter_data).all()
    return actions
