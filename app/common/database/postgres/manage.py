from .core import Base


def init_database(engine):
    """Initializes the database."""
    Base.metadata.create_all(engine)


def drop_database(engine):
    """Drop the database."""
    Base.metadata.drop_all(engine)
