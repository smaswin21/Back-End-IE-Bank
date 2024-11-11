import pytest
from iebank_api.models import Account, User
from iebank_api import db, app

@pytest.fixture
def testing_client(scope='module'):
    with app.app_context():
        db.create_all()

        created_user = User("created", "email@email.com", "scrypt:32768:8:1$Pj5ltEig2ys89mOH$19627e267381583adb2da7ad15b30b11e6ebfee3c6ac308f5e4894e3cbe0323f1c4c4f8f91debebceef08dab19a898a652e975c1612362253d7f64cc3f12ddb7", admin=False)
        db.session.add(created_user)



        db.session.commit()


    with app.test_client() as testing_client:
        yield testing_client

    with app.app_context():
        db.drop_all()
@pytest.fixture
def user(scope='module'):
    return User(
        "username",
        "user@iebank.com",
        "scrypt:32768:8:1$Pj5ltEig2ys89mOH$19627e267381583adb2da7ad15b30b11e6ebfee3c6ac308f5e4894e3cbe0323f1c4c4f8f91debebceef08dab19a898a652e975c1612362253d7f64cc3f12ddb7", # my_password
        admin=False)

@pytest.fixture
def admin(scope='module'):
    return User(
        "admin1",
        "admin@iebank.com",
        "scrypt:32768:8:1$hHRF3oC2m9buHURx$b8b5b9afd0c18a51d6a06dc136fe79533a9c39b3e7a478fb6ef977f030c233e6e6ec498f7c01a822ca19edaf4d828a9154b87230638e2f492c0dc0310fffe164", # my_password1
        admin=True)
