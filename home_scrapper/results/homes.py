# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Homes(Base):
    __tablename__ = "homes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    city = Column(String)
    neighbourhood = Column(String)
    price = Column(Float)
    price_last = Column(Float)
    currency = Column(String)
    type = Column(String)
    area = Column(String)
    phone = Column(String)
    floor = Column(Integer)
    rooms = Column(Integer)
    heating = Column(String)
    url = Column(String, unique=True)

    def to_db(self, database: Engine):
        """dumps home to database!

        :param database: SDLAlchemy database engine
        """
        with Session(bind=database) as session:
            home = session.query(Homes).filter_by(url=self.url).first()

            # add if url does not exist
            if home is None:
                session.add(self)
                session.commit()

            # update price if different price
            else:
                if self.price != home.price:
                    home.price_last = home.price
                    home.price = self.price
                    session.commit()
