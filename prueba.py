from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://etl_user:ETLpassword123!@34.41.26.161:3306/covid_data")
with engine.connect() as conn:
    print("✅ Conexión exitosa")
