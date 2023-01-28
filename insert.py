from cassandra_interface import Cassandra
import csv

def insert_data(session, table_name):
    # insert data 
    file = 'event_datafile_new.csv'
    insert_query= f"""
        insert into sparkify.{table_name}
        (user_id, session_id, item_in_session, first_name, last_name, gender, location, level, song, artist, length)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    with open(file, encoding = 'utf8') as f:
        # use dictreader to access columns by name, 
        # not index (which is hard to read, especially 
        # because I'm reordering columns)
        csvreader = csv.DictReader(f)
        next(csvreader) # skip header
        for line in csvreader:
            session.execute(
                insert_query,
                (
                    int(line['userId']), int(line['sessionId']), int(line['itemInSession']), 
                    line['firstName'], line['lastName'], line['gender'], line['location'], line['level'],
                    line['song'], line['artist'], float(line['length'])
                ))

    session.shutdown()