from cassandra_interface import Cassandra
from insert import insert_data
from etl import run_etl
import logging
logging.basicConfig(level=logging.INFO)

if __name__=="__main__":
    # first, run the etl
    run_etl()

    # connect to cassandra
    cassandra=Cassandra()
    cassandra.connect()

    # create and set keyspace
    cassandra.create_keyspace("sparkify")

    # creating tables
    # read in our DDL
    with open('ddl.cql', 'r') as f:
        ddl_file=f.read().replace("\n", "")

    ddl_list=ddl_file.split(';')

    # create tables
    for ddl in ddl_list:
        try:
            cassandra.session.execute(ddl)
        # in case of error, shut down then raise
        except Exception as e:
            cassandra.shutdown()
            raise

    # insert data
    table_names=['item_in_session', 'artist_song_user', 'song_filter']
    for table in table_names:
        try:
            insert_data(cassandra.session, table)
        except Exception as e:
            cassandra.shutdown()
            raise

    # running queries
    # read in queries
    with open('queries.cql', 'r') as f:
        queries_file=f.read().replace("\n", "")

    queries_list=queries_file.split(';')

    # run queries and print rows
    for i, query in enumerate(queries_list):
        try:
            logging.info(f'Running query {i+1}...')
            result=cassandra.session.execute(query)
            for row in result:
                print(row)
        # in case of error, shut down then raise
        except Exception as e:
            cassandra.shutdown()
            raise 

    cassandra.shutdown()