from app.models import User


def test_create_user(_db):
    print(vars(_db))
    # user = User(username='test', email='test', password='test')
    # _db.session.add(user)
    # _db.session.commit()
    
    row = _db.session.query(User).filter_by(username='test').first()
    assert row.username == 'test'
