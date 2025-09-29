"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
from sqlmodel import select
from sqlmodel import Session

from .db import init_db, get_engine, get_session
from .models import Activity, User, Signup
from .seed import seed_data


app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=current_dir / "static"), name="static")


@app.on_event("startup")
def on_startup():
    eng = init_db()
    seed_data(eng)


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    eng = get_engine()
    with Session(eng) as sess:
        activities = sess.exec(select(Activity)).all()
        result = []
        for a in activities:
            participants = [
                s.user.email for s in a.signups if getattr(s, "user", None)
            ]
            result.append({
                "id": a.id,
                "name": a.name,
                "description": a.description,
                "schedule": a.schedule,
                "max_participants": a.max_participants,
                "participants": participants,
            })
        return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    eng = get_engine()
    with Session(eng) as sess:
        # Load activity with SELECT ... FOR UPDATE semantics via session
        activity = sess.exec(select(Activity).where(Activity.name == activity_name)).one_or_none()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Ensure user exists or create
        user = sess.exec(select(User).where(User.email == email)).one_or_none()
        if not user:
            user = User(email=email)
            sess.add(user)
            sess.commit()
            sess.refresh(user)

        # Re-fetch activity to ensure signups list is current
        sess.refresh(activity)
        current_count = len(activity.signups or [])

        # Check if user already signed up
        already = sess.exec(select(Signup).where(Signup.activity_id == activity.id, Signup.user_id == user.id)).one_or_none()
        if already:
            raise HTTPException(status_code=400, detail="Student is already signed up")

        if current_count >= activity.max_participants:
            raise HTTPException(status_code=400, detail="Activity is full")

        # Create signup
        signup = Signup(user_id=user.id, activity_id=activity.id)
        sess.add(signup)
        sess.commit()
        return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    eng = get_engine()
    with Session(eng) as sess:
        activity = sess.exec(select(Activity).where(Activity.name == activity_name)).one_or_none()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        user = sess.exec(select(User).where(User.email == email)).one_or_none()
        if not user:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        signup = sess.exec(select(Signup).where(Signup.activity_id == activity.id, Signup.user_id == user.id)).one_or_none()
        if not signup:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        sess.delete(signup)
        sess.commit()
        return {"message": f"Unregistered {email} from {activity_name}"}
