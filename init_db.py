from models.base import Base, engine
from models.user import User
from models.event import Event
from models.alert import Alert

print("Starting DB creation...")

Base.metadata.create_all(bind=engine)

print("DB created successfully")