from sqlalchemy import create_engine, Column, Integer, String, NVARCHAR, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from utils.config import Config
from sqlalchemy.orm import sessionmaker
from utils.context import context

Base = declarative_base()


class Contacts(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    email = Column(NVARCHAR(320))
    first_name = Column(String(120))
    last_name = Column(String(120))
    phone = Column(VARCHAR(120))
    country = Column(VARCHAR(120))
    city = Column(VARCHAR(120))
    address = Column(VARCHAR(120))


class Database:
    def __init__(self):
        self.db = Config.DB
        self.user = Config.DB_USER
        self.password = Config.DB_PASSWORD
        self.host = Config.DB_HOST
        self.name = Config.DB_NAME
        self.engine = self._create_engine()
        self.session = sessionmaker(bind=self.engine)()

    def _create_engine(self):
        if Config.DB == 'sqlite':
            engine = create_engine(url='sqlite:///address_book.db', echo=True)
        else:
            engine = create_engine(url=f"{self.db}://{self.user}:{self.password}@{self.host}/{self.name}",
                                   echo=True)

        context.app.logger.info(f"{Config.DB} DB engine was successfully created")
        return engine

    @staticmethod
    def _check_db_answer(data, contact_id):
        if not data:
            message = f'No contact with id - {contact_id} in DB'
            context.app.logger.error(message)
            return {'Error': message}
        return None

    @staticmethod
    def clean_sys_info(rows):
        if rows.pop('_sa_instance_state', None):
            return rows
        else:
            for row in rows.values():
                row.pop('_sa_instance_state', None)
            return rows

    def configure_db(self):
        Base.metadata.create_all(self.engine)
        context.app.logger.info(f'All DB tables were created')

    def get_contacts(self):
        data = self.session.query(Contacts).all()
        rows = {row.__dict__['id']: row.__dict__ for row in data}
        context.app.logger.info(f'Got list of contacts')
        return self.clean_sys_info(rows)

    def get_contact(self, contact_id):
        data = self.session.query(Contacts).get(contact_id)
        if not data:
            context.app.logger.error(f'Failed to get contacts with id - {contact_id}')
            return {"Error": f"No contact with id - {contact_id} in DB"}
        row = data.__dict__
        context.app.logger.info(f'Found contact with id - {contact_id}')
        return self.clean_sys_info(row)

    def create_contact(self, json):
        contact = Contacts(email=json['email'],
                           first_name=json['first_name'],
                           last_name=json['last_name'],
                           phone=json['phone'],
                           country=json['country'],
                           city=json['city'],
                           address=json['address'])
        self.session.add(contact)
        self.session.commit()
        self.session.refresh(contact)
        context.app.logger.info(f'Contact with id - {contact.id} was created')
        return contact.id

    def delete_contact(self, contact_id):
        data = self.session.query(Contacts).filter(Contacts.id == contact_id).delete()
        err_message = self._check_db_answer(data, contact_id)
        if err_message:
            return err_message
        self.session.commit()
        context.app.logger.info(f'Contact with id - {contact_id} was deleted')

    def update_contact(self, contact_id, updated_fields):
        data = self.session.query(Contacts).filter(Contacts.id == contact_id). \
            update(updated_fields, synchronize_session="fetch")
        err_message = self._check_db_answer(data, contact_id)
        if err_message:
            return err_message
        self.session.commit()
