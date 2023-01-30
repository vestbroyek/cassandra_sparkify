select
    artist, 
    song, 
    length 
from 
    sparkify.item_in_session 
where 
    session_id = 338 
and 
    item_in_session = 4

;

select
    artist,
    song,
    first_name,
    last_name 
from 
    sparkify.artist_song_user 
where
    user_id = 10 
and
    session_id = 182

;

select
    first_name,
    last_name 
from 
    sparkify.song_filter 
where
    song = 'All Hands Against His Own'