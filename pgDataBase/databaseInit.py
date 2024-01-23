# -*- encoding:utf-8 -*-

from pgDataBase import *


class InitDatabaseOperation:

    def __init__(self, config):
        self.config = config

        self.session = self.db_session()

    def init_database_connection(self):
        db_engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
            self.config.database.username, self.config.database.password,
            self.config.database.host, self.config.database.port,
            self.config.database.database_name), max_overflow=10)

        Base.metadata.create_all(db_engine)

        db_session = sessionmaker(bind=db_engine)
        return db_session

    def db_session(self):
        return self.init_database_connection()()

    def insert_data_to_database(self, data_content):

        if type(data_content) is list:
            self.session.add_all(data_content)
        else:
            self.session.add(data_content)
        self.session.commit()
        self.session.close()
