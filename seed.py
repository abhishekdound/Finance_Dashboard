from app.database import SessionLocal, engine, Base
from app.models.user import User, Role
from app.core.security import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()


def seed_all():
    admin_role = Role(name="Admin", description="Full Management")
    analyst_role = Role(name="Analyst", description="Read + Analytics")
    viewer_role = Role(name="Viewer", description="Read Only")

    db.add_all([admin_role, analyst_role, viewer_role])
    db.commit()

    users = [
        User(email="admin@test.com", role_id=admin_role.id, hashed_password=get_password_hash("pass123")),
        User(email="analyst@test.com", role_id=analyst_role.id, hashed_password=get_password_hash("pass123")),
        User(email="viewer@test.com", role_id=viewer_role.id, hashed_password=get_password_hash("pass123"))
    ]

    db.add_all(users)
    db.commit()
    print(" Seeded: Admin (admin@test.com), Analyst (analyst@test.com), Viewer (viewer@test.com)")


if __name__ == "__main__":
    seed_all()
