from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
engine = create_engine('sqlite:///app.db')
Base = declarative_base()

class Temporizador(Base):
    __tablename__ = 'temporizadores'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tiempo_restante = Column(Integer)
    corriendo = Column(Boolean)
    pausado = Column(Boolean)

class Cronometro(Base):
    __tablename__ = 'cronometros'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tiempo_transcurrido = Column(Integer)
    corriendo = Column(Boolean)

class Pomodoro(Base):
    __tablename__ = 'pomodoros'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    duracion_trabajo = Column(Integer)
    duracion_descanso = Column(Integer)
    ciclos = Column(Integer)
    ciclo_actual = Column(Integer)

# Crear todas las tablas
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()
