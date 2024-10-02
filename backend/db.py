import os
import psycopg2

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = os.environ["DATABASE_URL"]


def insertItem(eventTitle: str, eventDesc: str, itemType: str):

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    if itemType == "announcements":
        session.execute(text(
            """CREATE TABLE IF NOT EXISTS announcements(
            id SERIAL PRIMARY KEY,
            eventTitle text NOT NULL,
            eventDesc text NOT NULL);
        """
        ))

        session.execute(text(
            """
            INSERT INTO announcements(eventTitle, eventDesc) VALUES(:eventTitle, :eventDesc);
            """),
            {"eventTitle": eventTitle, "eventDesc": eventDesc}
        )

    elif itemType == "events":
        session.execute(text(
            """CREATE TABLE IF NOT EXISTS events(
            id SERIAL PRIMARY KEY,
            eventTitle text NOT NULL,
            eventDesc text NOT NULL);
        """
        ))

        session.execute(text(
            """
            INSERT INTO events(eventTitle, eventDesc) VALUES(:eventTitle, :eventDesc);
            """),
            {"eventTitle": eventTitle, "eventDesc": eventDesc}
        )

    else:
        pass

    session.commit()
    session.close()
