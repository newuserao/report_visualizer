from firebase_admin import firestore
from google.cloud import bigquery

import os
import datetime

credential_path = "roofstack-a20899a9a240.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
db = firestore.Client()

# This part should be skipped if tables are already created.
bigquery_client = bigquery.Client()
dataset_name = 'rf'
table_name = 'users'
schema = [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("state", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("createdAt", "DATETIME"),
            bigquery.SchemaField("modifiedAt", "DATETIME" ),
        ]
dataset_ref = bigquery_client.dataset(
    '{}'.format(dataset_name))
table_ref = dataset_ref.table(table_name)
table = bigquery.Table(table_ref, schema=schema)
table = bigquery_client.create_table(
    table)


table_name = 'items'
schema = [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("itemName", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("userRef", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("createdAt", "DATETIME"),
            bigquery.SchemaField("modifiedAt", "DATETIME" ),
        ]
dataset_ref = bigquery_client.dataset(
    '{}'.format(dataset_name))
table_ref = dataset_ref.table(table_name)
table = bigquery.Table(table_ref, schema=schema)
table = bigquery_client.create_table(
    table)

# Reading and inserting both users and items data
collnameref = db.collection(u'users')
docs = collnameref.stream()
all_users = []
all_items = []
for doc in docs:
    dict_doc = doc.to_dict()
    print(dict_doc.get('createdAt'))
    created_at = datetime.datetime.fromtimestamp(
        dict_doc.get('createdAt').timestamp()).strftime('%Y-%m-%d %H:%M:%S')
    modified_at = datetime.datetime.fromtimestamp(
        dict_doc.get('modifiedAt').timestamp()).strftime('%Y-%m-%d %H:%M:%S')
    data = {'id': doc.id,
            'name': dict_doc.get('name'),
            'state': dict_doc.get('state'),
            'createdAt': created_at,
            'modifiedAt':modified_at
     }
    all_users.append(data)
    for collection_ref in doc.reference.collections():
        items = collection_ref.stream()

        for item in items:
            dict_item = item.to_dict()
            created_at = datetime.datetime.fromtimestamp(
                dict_item.get('createdAt').timestamp()).strftime(
                '%Y-%m-%d %H:%M:%S')
            modified_at = datetime.datetime.fromtimestamp(
                dict_item.get('modifiedAt').timestamp()).strftime(
                '%Y-%m-%d %H:%M:%S')
            data = {
                'id': item.id,
                'itemName': dict_item.get('itemName'),
                'userRef': dict_item.get('userRef').split('/')[1],
                'createdAt': created_at,
                'modifiedAt': modified_at
                }
            all_items.append(data)

try:
    user_errors = bigquery_client.insert_rows_json(
        f"roofstack.rf.users", all_users
    )
    item_errors = bigquery_client.insert_rows_json(
        f"roofstack.rf.users", all_items
    )
except Exception:
    raise



