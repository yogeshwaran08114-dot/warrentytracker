from app.core.deps import engine, Base

from app.models.user import User
from app.models import Category, Product, Registration, Warranty, Claim


def init_db():
    Base.metadata.create_all(bind=engine)