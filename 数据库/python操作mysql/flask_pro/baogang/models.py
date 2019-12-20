from exts import db


class Pictures(db.Model):
    __tablename__ = "pictures"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gray0 = db.Column(db.String(20), nullable=False)
    gray1 = db.Column(db.String(20), nullable=False)
    gray2 = db.Column(db.String(20), nullable=False)
    gray3 = db.Column(db.String(20), nullable=False)
    gray4 = db.Column(db.String(20), nullable=False)
    gray5 = db.Column(db.String(20), nullable=False)
    gray6 = db.Column(db.String(20), nullable=False)
    gray7 = db.Column(db.String(20), nullable=False)
    gray8 = db.Column(db.String(20), nullable=False)
    gray9 = db.Column(db.String(20), nullable=False)
    path = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(20))
    work_id = db.Column(db.String(20))

    def json(self):
        return {"gray0": self.gray0, "gray1": self.gray1, "gray2": self.gray2,
                "gray3": self.gray3, "gray4": self.gray4, "gray5": self.gray5,
                "gray6": self.gray6, "gray7": self.gray7, "gray8": self.gray8,
                "gray9": self.gray9, "path": self.path, "time": self.time, "work_id": self.work_id}
