import firebase_admin as fba
from firebase_admin import db

from dataclasses import dataclass, asdict


@dataclass
class UserData:
    branch: str
    study_form: str
    group: str


@dataclass
class User:
    user_id: str
    data: UserData


class Database:
    def __init__(self, database_url, key_path):
         cred = fba.credentials.Certificate(key_path)
         fba.initialize_app(cred, {'databaseURL': database_url})
         self.ref = db.reference("/")

    def get_user(self, user_id):
        user = self.ref.get().get(user_id)
        return user

    def get_all_users(self):
        return self.ref.get()

    def set_user(self, user):
        self.ref.child(user.user_id).set(asdict(user.data))
            

user = User("test_user",
    UserData(
        "факультет филологический",
        "очная форма обучения",
        "бакалавриат, 3 курс, группа 3об_РУСФИЛ"
    )
)

database = Database("https://herzenbot-default-rtdb.europe-west1.firebasedatabase.app/", "firebase_key.json")
database.set_user(user)
print(database.get_user(user.user_id))
