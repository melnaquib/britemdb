from pydantic import BaseSettings


class Config(BaseSettings):
    service_name: str = 'briteomdb'
    secret_key: str = 's3cr3t_k3y'

    secret: str = 's3cr3t'

    users_1_username: str
    users_1_password: str
    users_1_can_delete: bool

    omdb_apikey: str

    firestore_emulator_host: str



config = Config()
