from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///env_setup.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_name = Column(String(255), nullable=False, unique=True)
    os = Column(String(50), nullable=False)
    packages = Column(Text)
    environment_variables = Column(Text)
    symlinks = Column(Text)
    custom_commands = Column(Text)


def initialize_database():
    Base.metadata.create_all(engine)
