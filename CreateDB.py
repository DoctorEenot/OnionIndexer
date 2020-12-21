import DBclient
from Configuration import DB_SCHEME, ENTRY_URL
import time

a = input('You Sure?')


db = DBclient.DB('127.0.0.1',666)
db.connect()

for db_name in list(DB_SCHEME.keys()):
    count_of_columns = len(list(DB_SCHEME[db_name].keys()))
    db.create_db(db_name,count_of_columns,0)
    for i in range(count_of_columns):
        column_name = list(DB_SCHEME[db_name].keys())[i]
        db.init_column(db_name,i,column_name,DB_SCHEME[db_name][column_name])


        #time.sleep(1)

db.append('to_process',[ENTRY_URL],[DB_SCHEME['to_process']['url']])


db.dump()
db.close()
