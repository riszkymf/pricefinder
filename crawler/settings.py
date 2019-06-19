from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

CONF_PATH = os.getenv("CRAWLER_CONFIGURATION_PATH")
APP_URL = os.getenv("CRAWLER_URL")
DUMP_LOCATION = os.getenv("DUMP_LOCATION")