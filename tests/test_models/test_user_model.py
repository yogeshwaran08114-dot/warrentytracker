from app.models.user import User


def test_user_table_schema():
    table = User.__table__
    assert table.name == "users"
    columns = {column.name: column for column in table.c}
    assert "id" in columns
    assert "email" in columns
    assert "hashed_password" in columns
    assert "full_name" in columns
    assert "mobile_number" in columns
    assert "is_active" in columns
    assert "is_verified" in columns
    assert "created_at" in columns
    assert "updated_at" in columns
    assert columns["email"].unique
    assert columns["hashed_password"].nullable is False


def test_user_creates_row(engine, db_session):
    from app.core.security import get_password_hash

    user = User(
        email="model@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Model User",
    )
    db_session.add(user)
    db_session.commit()
    assert user.id is not None
