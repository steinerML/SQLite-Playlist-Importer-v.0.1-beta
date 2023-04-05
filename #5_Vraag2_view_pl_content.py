import sqlite3

with sqlite3.connect("chinook.db") as db:
    cursor = db.cursor()

def view_playlist_content():
    try:
        cursor.execute("SELECT Name FROM playlists ORDER BY PlaylistId DESC LIMIT 1;")
        name = cursor.fetchone()
        name_string = " ".join(name)
        input(f"<<Press ENTER to view songs in {name_string} playlist>>: ")
        cursor.execute("""SELECT t.name AS "Track Name",ar.name AS "Artist Name"
                        FROM playlists AS pl INNER JOIN playlist_track AS plt
                        ON pl.PlaylistId = plt.PlaylistId INNER JOIN tracks AS t
                        ON plt.TrackId = t.TrackId INNER JOIN albums AS ab
                        ON t.AlbumId = ab.AlbumId INNER JOIN artists AS ar
                        ON ar.ArtistId = ab.ArtistId WHERE pl.PlaylistId = (SELECT MAX(PlaylistId) FROM playlists);""")
        content = cursor.fetchall()
        for index, song in enumerate(content,1):
            print(index,*song)
    except sqlite3.Error:
        print("Database Error")
    db.commit()
    db.close()
view_playlist_content()