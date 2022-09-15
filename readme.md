# ROOF Stacks Report Visualizer #  

I will introduce what I did step by step in the below section:

## Summary ##

This system is designed like a pipeline between bigquery and firestore. For visualization I used datastudio. I thought that, creating a mini flask app to show embeded data studio report on web application would be suitable. 
This Project requires a service account key file as json. It should be uploaded on the main folder. I did not upload it for the security. 
If this project goes live, Airflow needed to create dependencies between each task while keeping it in a single DAG.
```create_firestore_data.py --> upload_to_bq.py --> run app```

## Steps ##
* This project requires docker to fully run as an app
* A new GCP project called as *roofstack* created.
![Alt text](images/gcp_project.png?raw=true)
* Firestore enabled.
* New service account created and new key created as json file.
![Alt text](images/service_key.png?raw=true)
* Editor role granted to that service account from IAM concole.
![Alt text](images/service_as_user.png?raw=true)
* Created virtualenv then installed requirements.txt
* Activated virtualenv.
* Ran the *create_firestore_data.py* script.
* 2 collections created on firestore. One of them is users and other one is subcollection under users as items.
![Alt text](images/firestore_collections.png?raw=true)
![Alt text](images/firestore_items.png?raw=true)
* Same script also generated 10 random data and inserted them into collections.
* Created Bigquery dataset called as rf.
* Ran the *upload_to_bq* script.
* 2 tables created on Bigquery.
* All users inserted into table called as users with related schemas.
```python
user_schema = [
    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("state", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("createdAt", "DATETIME"),
    bigquery.SchemaField("modifiedAt", "DATETIME" )
]
  ```
* All items inserted into table called as items with related schemas.
```python
items_schema = [
    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("itemName", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("userRef", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("createdAt", "DATETIME"),
    bigquery.SchemaField("modifiedAt", "DATETIME" ),
]
  ```
![Alt text](images/bq_items.png?raw=true)
![Alt text](images/bq_users.png?raw=true)
* Created new datastudio report.
* Added users and items table as datasource.
![Alt text](images/bq_to_ds.png?raw=true)
* Joined tables on users_id = items_userRef.
* Basic Bar Chart and Pie Chart created.
![Alt text](images/datastudio_report.png?raw=true)
* Opened report to public.
* Under the file section there is embed report section. By using embed report iframe created.
![Alt text](images/embed_report.png?raw=true)
* Created basic flask app
* Put iframe into datastudio.html
* Created Dockerfile for that mini flask app.
* Ran ```docker build -t report .``` for building container.
* Ran ```docker run -p 105:105 report``` to run app.
![Alt text](images/docker_concole.png?raw=true)
* Report looked like;
![Alt text](images/flask_datastudio.png?raw=true "Flask Web Page")

