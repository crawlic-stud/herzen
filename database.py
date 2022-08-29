import firebase_admin as fba
from firebase_admin import db

cred = fba.credentials.Certificate('firebase_key.json')
default_app = fba.initialize_app(cred,
                                 {'databaseURL': "https://herzenbot-default-rtdb.europe-west1.firebasedatabase.app/"})

ref = db.reference("/")

data = [
        "факультет биологии",
        "очная форма обучения",
        "бакалавриат, 1 курс, группа 1об БИО 1"
]

ref.set(data)
print(ref.get())
