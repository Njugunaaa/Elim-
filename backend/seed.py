import os
from datetime import datetime, timedelta
from flask import Flask
from models import db
from models.user import User, UserRole
from models.sermon import Sermon
from models.event import Event
from models.church_structure import Region, Church, Ministry

# --- Config ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def seed_database():
    with app.app_context():
        print("Dropping and recreating database (development only)...")
        db.drop_all()
        db.create_all()

        # --- USERS ---
        print("Seeding users...")
        admin = User(
            email="admin@church.test",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN
        )
        admin.set_password("Passw0rd!")
        member = User(
            email="member@church.test",
            first_name="John",
            last_name="Doe",
            role=UserRole.MEMBER
        )
        member.set_password("Passw0rd!")
        demo_users = [
            User(
                email=f"user{i}@church.test",
                first_name=f"User{i}",
                last_name="Demo",
                role=UserRole.MEMBER
            )
            for i in range(1, 4)
        ]
        for u in demo_users:
            u.set_password("Passw0rd!")
        db.session.add_all([admin, member] + demo_users)
        db.session.commit()

        # --- REGIONS ---
        print("Seeding regions...")
        region_objs = [Region(name=f"Region {i}") for i in range(1, 6)]
        db.session.add_all(region_objs)
        db.session.commit()

        regions = Region.query.all()

        # --- CHURCHES ---
        print("Seeding churches...")
        churches = []
        for i, region in enumerate(regions, start=1):
            c = Church(
                name=f"Church {i}",
                address=f"{i} Church Street, City",
                point_of_contact=f"Pastor {i}",
                phone=f"0712{i:06d}"[-10:],
                email=f"church{i}@example.com",
                region_id=region.id
            )
            churches.append(c)
        churches.append(Church(
            name="Central Fellowship",
            address="Central Ave",
            point_of_contact="Pastor A",
            phone="0712345678",
            email="central@example.com",
            region_id=regions[0].id
        ))
        churches.append(Church(
            name="Hope Community",
            address="Hope Rd",
            point_of_contact="Pastor B",
            phone="0712987654",
            email="hope@example.com",
            region_id=regions[0].id
        ))
        db.session.add_all(churches)
        db.session.commit()

        # --- MINISTRIES ---
        print("Seeding ministries...")
        created_churches = Church.query.all()
        ministries = []
        for church in created_churches:
            ministries.append(Ministry(
                name=f"Youth Ministry {church.id}",
                description="Youth outreach and programs",
                church_id=church.id
            ))
            ministries.append(Ministry(
                name=f"Music Ministry {church.id}",
                description="Worship and choir",
                church_id=church.id
            ))
        db.session.add_all(ministries)
        db.session.commit()

        # --- EVENTS ---
        print("Seeding events...")
        now = datetime.utcnow()
        events = [
            Event(
                title=f"Community Event {i}",
                date=(now + timedelta(days=i*3)),
                description=f"Details for event {i}",
                location="Main Hall",
                image_url=f"https://example.com/event{i}.jpg"
            )
            for i in range(1, 6)
        ]
        db.session.add_all(events)
        db.session.commit()

        # --- SERMONS ---
        print("Seeding sermons...")
        sermons = [
            Sermon(
                title=f"Sermon {i}",
                preacher=f"Pastor {i}",
                description=f"Powerful message on topic {i}",
                date=(now - timedelta(days=i*7)),
                scripture="John 3:16"
            )
            for i in range(1, 6)
        ]
        db.session.add_all(sermons)
        db.session.commit()

        print("Seed completed.")
        print("Admin login: admin@church.test / Passw0rd!")
        print("Member login: member@church.test / Passw0rd!")

if __name__ == "__main__":
    seed_database()
