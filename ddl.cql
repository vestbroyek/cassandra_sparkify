create table if not exists sparkify.item_in_session
(
    user_id int,
    session_id int,
    item_in_session int,
    first_name text,
    last_name text,
    gender text,
    location text,
    level text,
    song text,
    artist text,
    length float,
    PRIMARY KEY ((session_id), item_in_session))

;

create table if not exists sparkify.artist_song_user
(
    user_id int,
    session_id int,
    item_in_session int,
    first_name text,
    last_name text,
    gender text,
    location text,
    level text,
    song text,
    artist text,
    length float,
    PRIMARY KEY ((user_id, session_id), item_in_session))

;

create table if not exists sparkify.song_filter
(
    user_id int,
    session_id int,
    item_in_session int,
    first_name text,
    last_name text,
    gender text,
    location text,
    level text,
    song text,
    artist text,
    length float,
    PRIMARY KEY ((song), first_name, last_name, user_id))