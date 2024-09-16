from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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
    symlinks = Column(Text)
    custom_commands = Column(Text)
    environment_variables = relationship("EnvironmentVariable", back_populates="profile", cascade="all, delete, delete-orphan")

class EnvironmentVariable(Base):
    __tablename__ = 'environment_variables'
    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    name = Column(String(255), nullable=False)
    value = Column(Text, nullable=False)
    append = Column(Integer, nullable=False, default=0)  # 0 or 1 for False/True
    profile = relationship("Profile", back_populates="environment_variables")

def initialize_database():
    Base.metadata.create_all(engine)