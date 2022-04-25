from adress_book_api import run_api
from utils.context import context
from utils.db_utils import Database

if __name__ == '__main__':
    context.db = Database()
    context.db.configure_db()
    run_api()
