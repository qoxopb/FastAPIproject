from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    userid:str = 'abc123'
    passwd:str = '987xyz'
    dbname:str = 'clouds2024.db'
    dburl:str = 'amazon_aws'
    db_conn:str = f'sqlite:///app/{dbname}'
    #db_conn = f'mysql+qymysql://{userid}:{passwd}'
    #db_conn = f'oracle+cx_oracle://{userid}:{passwd}'

    # class Config:
    #     env_file = '.env'
config = Settings()

