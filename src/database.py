import firebase_admin as fba
from firebase_admin import db

from dataclasses import dataclass, asdict
import logging


@dataclass
class UserData:
    branch: str = ""
    study_form: str = ""
    group: str = ""
    subscribed: bool = True


@dataclass
class User:
    chat_id: int
    data: UserData


class Database:
    def __init__(self, database_url, key_path):
        cred = fba.credentials.Certificate(key_path)
        fba.initialize_app(cred, {'databaseURL': database_url})
        self.ref = db.reference("/")

    def get_user(self, user_id):
        try:
            all_users = self.ref.get()
            user_data = all_users.get(str(user_id))
            return User(chat_id=user_id, data=UserData(**user_data))
        except TypeError:
            return None

    def get_all_users(self):
        return self.ref.get()

    def set_user(self, user):
        try:
            self.ref.child(str(user.chat_id)).set(asdict(user.data))
        except Exception as e:
            logging.error(str(e))
            return False
        return True

    def update_all_users_fields(self):
        users = self.get_all_users()        
        if not users:
            return

        # iterate over keys which is ids
        for user_id in users: 
            user_obj = User(user_id, UserData())
            self.set_user(user_obj)           

    def user_has_empty_fields(self, user):
        if not user:
            return False

        user_data = list(asdict(user.data).values())
        if any(not data for data in user_data):
            return True
        return False


if __name__ == "__main__":
    # testing
    database = Database(
        database_url="https://herzenbot-default-rtdb.europe-west1.firebasedatabase.app/", 
        key_path="src/firebase_key.json"
    )

    database.update_all_users_fields()
    #print(database.user_has_empty_fields(361944343))
