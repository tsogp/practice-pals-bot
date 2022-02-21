# File with config for bot

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get('BOT_TOKEN')

MAXIMUM_NUMBER_OF_LIKES = 100

LINK_TO_YOOMONEY = "https://yoomoney.ru/to/410015159768343/0"

DATABASE_FILE_NAME = "database.db"
