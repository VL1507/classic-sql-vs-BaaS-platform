import logging

from bass.bass_api import Back4AppApi
from bass.gen_insert_bass import populate_bass
from config import BACK4APP_APPLICATION_ID, BACK4APP_REST_API_KEY


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Загрузка в бд

    # with Session() as session:
    #     populate_database(session, clear_first=True)

    #  загрузка в back4app
    back4app_api = Back4AppApi(
        application_id=BACK4APP_APPLICATION_ID,
        rest_api_key=BACK4APP_REST_API_KEY,
    )
    populate_bass(back4app_api)


if __name__ == "__main__":
    main()
