import logging

from bass.bass_api import Back4AppApi
from bass.gen_insert_bass import populate_bass
from bass.req_back4app import start_req_back4app
from config import BACK4APP_APPLICATION_ID, BACK4APP_REST_API_KEY
from db.db_conn import Session
from db.gen_insert_db import populate_database
from db.req_db import start_req_db


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Загрузка в бд

    # with Session() as session:
    #     populate_database(session, clear_first=True)

    # Запросы к бд
    # with Session() as session:
    #     start_req_db(session=session)

    #  Загрузка в back4app
    # back4app_api = Back4AppApi(
    #     application_id=BACK4APP_APPLICATION_ID,
    #     rest_api_key=BACK4APP_REST_API_KEY,
    # )
    # populate_bass(back4app_api)

    # Запросы к бд

    start_req_back4app(
        application_id=BACK4APP_APPLICATION_ID,
        rest_api_key=BACK4APP_REST_API_KEY,
    )


if __name__ == "__main__":
    main()
