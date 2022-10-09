from decouple import Csv, config

DATABASE = {
    "mongo_url": config("MONGO_URL"),
    "db_name": config("DB_NAME"),
}

CORS_ORIGIN_WHITELIST = config("CORS_ORIGIN_WHITELIST", cast=Csv(), default="")
LOGGING_CONFIG_FILE = config("LOGGING_CONFIG_FILE")
