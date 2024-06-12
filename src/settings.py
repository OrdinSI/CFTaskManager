import os

from dotenv import load_dotenv

load_dotenv()

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv('DB_HOST'),
                "port": os.getenv('DB_PORT'),
                "user": os.getenv('DB_USER'),
                "password": os.getenv('DB_PASSWORD'),
                "database": os.getenv('DB_NAME'),
            }
        },
    },
    "apps": {
        "models": {
            "models": ["src.db.models.task", "aerich.models"],
            "default_connection": "default",
        }
    },
}


BOT_TOKEN = os.getenv('BOT_TOKEN')
