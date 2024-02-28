from api.routes import handlers
from database.schema import create_tables

if __name__ == "__main__":
    # create DB tables if they aren't there
    create_tables()

    handlers.run(host='0.0.0.0', port=8080)