import flask 
import psycopg2 
import time, random
import secrets
import string, os
import base64

from kubernetes import client, config
if os.getenv('KUBERNETES_SERVICE_HOST'):
    configs = config.load_incluster_config()
else:
    configs = config.load_kube_config()
v1 = client.CoreV1Api()
secret = v1.read_namespaced_secret("postgres-application.credentials", "litmus")

t_host = "postgres-application.postgres.svc" #base64.b64decode(secret.data["host"]).decode('utf-8').replace('\n', '') #os.getenv('SERVICE', "postgres-application.postgres.svc")
t_port = base64.b64decode(secret.data["port"]).decode('utf-8').replace('\n', '') #os.getenv('PORT', "5432")
t_dbname = base64.b64decode(secret.data["dbname"]).decode('utf-8').replace('\n', '') #os.getenv("DBNAME", "postgres")
t_name_user = base64.b64decode(secret.data["username"]).decode('utf-8').replace('\n', '') #os.getenv("DATA_SOURCE_USER", "zalando")
t_password =  base64.b64decode(secret.data["password"]).decode('utf-8').replace('\n', '')

class DBDetails(object):
    def __init__(self, db_conn=None, db_cursor=None):
        self.db_conn      = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_name_user, password=t_password)
        self.db_cursor       = self.db_conn.cursor()

    def createTable(self, db):
       
        db.db_cursor = db.db_conn.cursor()
        letters = string.ascii_lowercase
        t_name_tbl = ''.join(random.choice(letters) for i in range(5))
        s = ""
        s += "CREATE TABLE " + t_name_tbl + "("
        s += " id serial NOT NULL"
        s += ", id_session int4 NULL DEFAULT 0"
        s += ", t_name_item varchar(64) NULL"
        s += ", t_contents text NULL"
        s += ", d_created date NULL DEFAULT now()"
        s += ", CONSTRAINT " + t_name_tbl + "_pkey PRIMARY KEY (id)"
        s += " ); "
        s += "CREATE UNIQUE INDEX " + t_name_tbl + "_id_idx ON public." + t_name_tbl + " USING btree (id);"

        db.db_cursor.execute(s)
        db.db_conn.commit()
        return t_name_tbl
            
    def dropTable(self, db, table):
        
        s = "DROP TABLE IF EXISTS " + table+";"
        db.db_cursor.execute(s)
        db.db_conn.commit()
        

def Main():
    print(t_name_user, t_dbname, t_host, t_port, t_password)
    db = DBDetails()
    table = db.createTable(db)
    db.dropTable(db, table)
    print(0)

Main()