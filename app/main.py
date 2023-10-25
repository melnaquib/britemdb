from dotenv import load_dotenv
load_dotenv(dotenv_path="/.env", override=True)

from .core.application import create_api
api = create_api()
