# Cassandra Sparkify project
## Introduction
This project is about a fictional startup, Sparkify. It has developed a new music streaming app and wants to analyse the data they've been collecting about songs and user activity. 

The analytics team is particularly interested in understanding which songs users are listening to. However, there is currently no easy way to interact with the data, since it's in a directory of csv files. 

The aim is to create an Apache Cassandra database which can query this song data. The team has already planned the queries they'd like to run. 

This project involves writing a small ETL pipeline in Python and designing a data model in Apache Cassandra. The pipeline will transform the data from several csv files into a single, streamlined file. This data will then be modelled and inserted into Apache Cassandra tables.

## Dataset
This project involves an `event_data` dataset. It's initially a directory of csv files, with each file representing a day. Example filepaths look like

`event_data/2018-11-08-events.csv`
`event_data/2018-11-09-events.csv`

We'll write a small script, `etl.py`, that concatenates these files into a single, bigger csv that we can load into Cassandra.

The resulting dataset has around 8,000 rows, with the following fields:

    - artist
    - first name
    - gender
    - item in session
    - last name
    - length
    - level
    - location
    - session ID
    - song
    - user ID

![Alt text](/images/data_sample.png?raw=true)

## Cassandra
### Setting up 
#### Connecting to the cluster
First, we need to connect to the cluster. In this case, for the purpose of reproducibility, I've created a cluster in a Docker container. I've used the official Cassandra image by running

```
docker run \
--name cassandra \
-p 127.0.0.1:9042:9042 \
-e CASSANDRA_CLUSTER_NAME=MyCluster \
-d \
cassandra
```

This will give us a containerised Cassandra instance called MyCluster, which will be accessible at 127.0.0.1, port 9042 (the default Cassandra port). 

![Alt text](/images/cassandra_container.png?raw=true)

We'll proceed to connect to it[1] and create a keyspace called Sparkify. 

I've made a `Cassandra` class that makes connecting and executing queries easy. We can simply create a session by doing `with Cassandra().connect() as session:` and execute queries like `session.execute("some query")`.

We can see our cluster and keyspace appearing in DBeaver!

![Alt text](/images/cluster_connection.png?raw=true)

In our Python logic, we'll set the keyspace.

### Data modelling
In Cassandra, we need to model our data for the queries we want to run. 

#### Inserting the data
In the upcoming queries, we'll use the Python driver to open our new master file and insert it into a Cassandra table. We'll create the table and then we'll open our file with `csv.DictReader`. I've made the column order more logical than in the source csv.

Once we load the data, we can see it show up in DBeaver!

![Alt text](/images/successful_load.png?raw=true)

For each query, we'll model the data differently, however. The key difference will be what we choose as the primary key.

#### Query 1
Let's say we want to find the artist, song title and song's length in the music app history that was heard during session_id = 338, and item_in_session = 4. 

The query might look like
```
select 
    artist, song, song_length
from 
    sparkify.sessions 
where 
    session_id = 338 
and 
    item_in_session = 4
```

In this case, we can set session ID and item in session as a composite primary key, either by setting them jointly as the partition key or one as the partition key and the other as a clustering column. 

We'll create a table specific to this query as follows:

```
create table if not exists sparkify.item_in_session
(
    user_id int,
    ...
    length float,
    PRIMARY KEY ((session_id), item_in_session)
)
```

Let's now run our query...

![Alt text](/images/query_1.png?raw=true)

Success!

#### Query 2
The second query is to find the name of artist and song (sorted by item in session ID) and user (first and last name) for user ID 10 and session ID 182.

Here, we need to create a new table. We'll set user ID and session ID as the partition key and item in session as the clustering column. I'm choosing item in session as the clustering column because it determines how the data is sorted on disk, so it will be very quick to run a query which sorts by that column. 

I'll run the below DDL: 

```
create table if not exists sparkify.artist_song_user
(
    user_id int,
    ...
    length float,
    PRIMARY KEY ((user_id, session_id), item_in_session)
)
```
Then we will run the below query:

```
select
    artist,
    song,
    user
from 
    sparkify.artist_song_user
where
    user_id = 10
and
    session_id = 182
```

Let's run it ... 

![Alt text](/images/query_2.png?raw=true)

Success!

#### Query 3
The third query looks for every user name (first and last) who listened to the song 'All Hands Against His Own'. 

We'll want to run a query like this:

```
select
    first_name,
    last_name
from 
    sparkify.song_filter
where
    song = 'All Hands Against His Own'
```

We'll definitely want the song to be part of the primary key. 

Moreover, we'll need first name, last name, and user ID to finish the primary key. (Names by themselves are not a reliable primary key.) 

We'll run:

```
create table if not exists sparkify.song_filter
(
    user_id int,
    ...
    length float,
    PRIMARY KEY ((song), first_name, last_name, user_id)
)
```

Let's run the query...

![Alt text](/images/query_3.png?raw=true)

Success!

---

[1] Note: As an extra bit of functionality, I\'ve connected to Cassandra via DBeaver. This is a nicer interface than relying on the Python driver or using `cqlsh` via the command line. (To do this, you first need to configure the Cassandra driver in DBeaver by downloading the appropriate .jar file.)