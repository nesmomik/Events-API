# shared fixtures
import pytest
from app import create_app
from models import db as _db

# create a app instance for testing
@pytest.fixture
def app():
    flask_app = create_app()
    flask_app.config.update({
        # disable error catching, allows better traces
        "TESTING": True,
        # dont use the "production" database
        # i can use ram instead of disk!
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "thiskeyneedstobeatleast32charslongtobeconsiderdsec"
    })

    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()

# test_client allows to make request without running the app
@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

# returns the in memory db object for tests that need db access
@pytest.fixture
def db(app):
    from app import db as _db
    return _db
