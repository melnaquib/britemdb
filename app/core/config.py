from pydantic import BaseSettings


class Config(BaseSettings):
    service_name: str = 'briteomdb'
    secret_key: str = 's3cr3t_k3y'

    secret: str = 's3cr3t'

    users_1_username: str
    users_1_password: str
    users_1_can_delete: bool

    omdb_apikey: str

    movies_collection: str = "movies"

    init_db_search: str = "star"

    # firestore_emulator_host: str = ""
    firestore_local: bool = False
    run_mode_db_init: bool = False


config = Config()
