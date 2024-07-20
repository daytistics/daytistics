from src import db


class Daytistic(db.Model):
    """
    Model for a new daytistic
    """

    __tablename__ = "daytistics"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.Date)
    time_use = {
        "work": db.Column(db.Integer),
        "study": db.Column(db.Integer),
        "exercise": db.Column(db.Integer),
        "social": db.Column(db.Integer),
        "leisure": db.Column(db.Integer),
        "sleep": db.Column(db.Integer),
        "other": db.Column(db.Integer),
        "custom01_name": db.Column(db.String(64)),
        "custom01_time": db.Column(db.Integer),
        "custom02_name": db.Column(db.String(64)),
        "custom02_time": db.Column(db.Integer),
        "custom03_name": db.Column(db.String(64)),
        "custom03_time": db.Column(db.Integer),
        "custom04_name": db.Column(db.String(64)),
        "custom04_time": db.Column(db.Integer),
        "custom05_name": db.Column(db.String(64)),
        "custom05_time": db.Column(db.Integer),
        "custom06_name": db.Column(db.String(64)),
        "custom06_time": db.Column(db.Integer),
        "custom07_name": db.Column(db.String(64)),
        "custom07_time": db.Column(db.Integer),
        "custom08_name": db.Column(db.String(64)),
        "custom08_time": db.Column(db.Integer),
        "custom09_name": db.Column(db.String(64)),
        "custom09_time": db.Column(db.Integer),
        "custom10_name": db.Column(db.String(64)),
        "custom10_time": db.Column(db.Integer),
        "custom11_name": db.Column(db.String(64)),
        "custom11_time": db.Column(db.Integer),
        "custom12_name": db.Column(db.String(64)),
        "custom12_time": db.Column(db.Integer),
        "custom13_name": db.Column(db.String(64)),
        "custom13_time": db.Column(db.Integer),
        "custom14_name": db.Column(db.String(64)),
        "custom14_time": db.Column(db.Integer),
        "custom15_name": db.Column(db.String(64)),
        "custom15_time": db.Column(db.Integer),
        "custom16_name": db.Column(db.String(64)),
        "custom16_time": db.Column(db.Integer),
        "custom17_name": db.Column(db.String(64)),
        "custom17_time": db.Column(db.Integer),
        "custom18_name": db.Column(db.String(64)),
        "custom18_time": db.Column(db.Integer),
        "custom19_name": db.Column(db.String(64)),
        "custom19_time": db.Column(db.Integer),
        "custom20_name": db.Column(db.String(64)),
        "custom20_time": db.Column(db.Integer),
    }

    mood = db.Column(db.Integer)
    productivity = db.Column(db.Integer)
    happiness = db.Column(db.Integer)
    stress = db.Column(db.Integer)
    recreation = db.Column(db.Integer)
    gratitude = db.Column(db.Integer)

    def __repr__(self):
        return "<Daytistic {}>".format(self.date)


def create_daytistic(
    user_id,
    date,
    time_use,
    mood,
    productivity,
    happiness,
    stress,
    recreation,
    gratitude,
):
    daytistic = Daytistic(
        user_id=user_id,
        date=date,
        time_use=time_use,
        mood=mood,
        productivity=productivity,
        happiness=happiness,
        stress=stress,
        recreation=recreation,
        gratitude=gratitude,
    )
    db.session.add(daytistic)
    db.session.commit()
    return daytistic


"""Creates a dict for the time_use attribute in the Daytistic model"""


def time_use(
    work=None,
    study=None,
    exercise=None,
    social=None,
    leisure=None,
    sleep=None,
    other=None,
    customs=None,
) -> dict:
    time_use = {
        "work": work,
        "study": study,
        "exercise": exercise,
        "social": social,
        "leisure": leisure,
        "sleep": sleep,
        "other": other,
    }

    # Fügen Sie die benutzerdefinierten Felder hinzu
    if customs is not None:
        for i, custom in enumerate(customs, start=1):
            time_use[f"custom{i}_name"], time_use[f"custom{i}_time"] = custom

    return time_use
