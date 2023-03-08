DROP TABLE IF EXISTS user;
  CREATE TABLE user (
    id = db.Column(db.Integer, primary_key=True)
  Name = db.Column(db.text, nullable=False)
  Username = db.Column(db.text, nullable=False, unique=True)
  Password = db.Column(db.text, nullable=False)
  Email = db.Column(db.text, nullable=False)
  );
  