import logging

from db.db_conn import Session
from db.gen_insert_db import populate_database


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    with Session() as session:
        populate_database(session, clear_first=True)


if __name__ == "__main__":
    main()
