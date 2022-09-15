from firebase_admin import firestore

import random
import string
import os
import datetime

credential_path = "roofstack-a20899a9a240.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
db = firestore.Client()


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


collnameref = db.collection(u'users')
for d in range(10):

    user_data = {
        u'name': f'{get_random_string(10)}',
        u'state': f'{get_random_string(10)}',
        u'createdAt': datetime.datetime.now(),
        u'modifiedAt' : datetime.datetime.now()
    }

    added_data = collnameref.add(user_data)
    inserted_data = added_data[1]
    number_of_items = random.randint(0, 5)
    for it in range(number_of_items):
        item_data = {
            u'itemName': f'{get_random_string(10)}',
            u'userRef': f'{inserted_data.path}',
            u'createdAt': datetime.datetime.now(),
            u'modifiedAt' : datetime.datetime.now()
        }
        obj_added_data = inserted_data.collection(u'items').add(item_data)