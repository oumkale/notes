import flask 
import psycopg2 
import time, random
import secrets
import string, os
import base64

t_host = os.getenv('SERVICE', "postgres-application.postgres.svc")
t_port = os.getenv('PORT', "5432")
t_dbname = os.getenv("DBNAME", "postgres")
t_name_user = os.getenv("DATA_SOURCE_USER", "zalando")
t_password =  "Ld3nWzyRuFjZQltbtAQQIedfH9j0nfD00OJlMbpDNuSEsiZeWWPwPlIlRwn0O6rB"

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
    db = DBDetails()
    table = db.createTable(db)
    db.dropTable(db, table)
    print(0)

Main()