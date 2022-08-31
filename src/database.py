import firebase_admin as fba
from firebase_admin import db

from dataclasses import dataclass, asdict
import logging


@dataclass
class UserData:
    branch: str
    study_form: str
    group: str


@dataclass
class User:
    user_id: int
    data: UserData


class Database:
    def __init__(self, database_url, key_path):
         cred = fba.credentials.Certificate(key_path)
         fba.initialize_app(cred, {'databaseURL': database_url})
         self.ref = db.reference("/")

    def get_user_data(self, user_id):
        try:
            all_users = self.ref.get()
            user = all_users.get(str(user_id))
            data_obj = UserData(**user)
            return data_obj
        except TypeError:
            return False

    def get_all_users(self):
        return self.ref.get()

    def set_user(self, user):
        try:
            self.ref.child(str(user.user_id)).set(asdict(user.data))
        except Exception as e:
            logging.error(str(e))
            return False
        return True

if __name__ == "__main__":
    user = User("test_user",
    UserData(
        "факультет филологический",
        "очная форма обучения",
        "бакалавриат, 3 курс, группа 3об_РУСФИЛ"
    )
)
