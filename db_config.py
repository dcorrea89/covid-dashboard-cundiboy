from sqlalchemy import create_engine

def get_engine():
    # Reemplaza con tus valores reales
    #user = 'root'       # o 'root' si no creaste otro
    #password = 'ETLpassword123!'
    user = 'etl_user'
    password = 'ETLpassword123!'
    host = '34.41.26.161'
    database = 'covid_data'
    
    url = f'mysql+pymysql://{user}:{password}@{host}:3306/{database}'
    return create_engine(url)
