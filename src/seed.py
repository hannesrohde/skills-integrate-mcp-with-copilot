from sqlmodel import Session, select
from .db import get_engine
from .models import Activity, User


def seed_data(engine=None):
    eng = engine or get_engine()
    with Session(eng) as sess:
        # Check if any activities exist
        existing = sess.exec(select(Activity)).first()
        if existing:
            return

        activities = [
            Activity(name="Chess Club", description="Learn strategies and compete in chess tournaments", schedule="Fridays, 3:30 PM - 5:00 PM", max_participants=12),
            Activity(name="Programming Class", description="Learn programming fundamentals and build software projects", schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM", max_participants=20),
            Activity(name="Gym Class", description="Physical education and sports activities", schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM", max_participants=30),
            Activity(name="Soccer Team", description="Join the school soccer team and compete in matches", schedule="Tuesdays and Thursdays, 4:00 PM - 5:30 PM", max_participants=22),
            Activity(name="Basketball Team", description="Practice and play basketball with the school team", schedule="Wednesdays and Fridays, 3:30 PM - 5:00 PM", max_participants=15),
            Activity(name="Art Club", description="Explore your creativity through painting and drawing", schedule="Thursdays, 3:30 PM - 5:00 PM", max_participants=15),
            Activity(name="Drama Club", description="Act, direct, and produce plays and performances", schedule="Mondays and Wednesdays, 4:00 PM - 5:30 PM", max_participants=20),
            Activity(name="Math Club", description="Solve challenging problems and participate in math competitions", schedule="Tuesdays, 3:30 PM - 4:30 PM", max_participants=10),
            Activity(name="Debate Team", description="Develop public speaking and argumentation skills", schedule="Fridays, 4:00 PM - 5:30 PM", max_participants=12),
        ]

        for a in activities:
            sess.add(a)

        # Create a sample teacher/admin user
        admin = User(email="teacher@mergington.edu", name="Teacher")
        sess.add(admin)

        sess.commit()


if __name__ == "__main__":
    seed_data()
