from utils.config import SQL_DIR

def load_sql(filename, subfolder=''):
    return (SQL_DIR / subfolder / filename).read_text()

