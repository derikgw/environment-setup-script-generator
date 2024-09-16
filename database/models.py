from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the SQLite database URL
DATABASE_URL = "sqlite:///env_setup.db"

# Initialize the engine
engine = create_engine(DATABASE_URL, echo=False)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)

# Create a Base class for declarative class definitions
Base = declarative_base()


# Define the Profile model
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the SQLite database URL
DATABASE_URL = "sqlite:///env_setup.db"

# Initialize the engine
engine = create_engine(DATABASE_URL, echo=False)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)

# Create a Base class for declarative class definitions
Base = declarative_base()


# Define the Profile model
class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_name = Column(String(255), nullable=False, unique=True)
    os = Column(String(50), nullable=False)
    packages = Column(Text)
    environment_variables = Column(Text)
    symlinks = Column(Text)
    custom_commands = Column(Text)  # Add custom commands column


# Function to initialize the database and create tables if they don't exist
def initialize_database():
    # This creates the tables if they do not exist
    Base.metadata.create_all(engine)
