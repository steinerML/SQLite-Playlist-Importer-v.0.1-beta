import sqlite3

with sqlite3.connect("chinook.db") as db:
    cursor = db.cursor()

def delete_playlist():
    try:
        input("Press ENTER to delete the current playlist: ")
        cursor.execute("DELETE FROM playlist_track WHERE PlaylistId = (SELECT MAX(PlaylistId) FROM playlists);")
        cursor.execute("DELETE FROM playlists WHERE PlaylistId = (SELECT MAX(PlaylistId) FROM playlists);")
        cursor.execute("SELECT count(*) FROM playlists WHERE PlaylistId = last_insert_rowid();")
        delete_check = cursor.fetchone()[0]
        if delete_check == 0:
            print("Delete operation successful!")
        else:
            print("Delete operation didn't work. There might be an error somewhere!")
    except sqlite3.Error:
        print("Database Error")
    db.commit()
    db.close()
delete_playlist()