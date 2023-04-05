import sqlite3

with sqlite3.connect("chinook.db") as db:
    cursor = db.cursor()

def update_pl_name():
    while True:
        try:
            new_name = str(input("<<Please enter new playlist name>>: "))
            cursor.execute("SELECT * FROM playlists WHERE Name LIKE (?)", (new_name,))
            data = cursor.fetchall()
            exists = len(data)
            if exists == 0:
                input("Name not in use!\nPress ENTER to change the playlist name!")
                cursor.execute("SELECT Name FROM playlists ORDER BY PlaylistId DESC LIMIT 1;")
                old_name = cursor.fetchone()
                old_name_string = " ".join(old_name)
                cursor.execute("""UPDATE playlists SET Name = (?) WHERE PlaylistId = (SELECT MAX(PlaylistId) 
                FROM playlists);""",(new_name,))
                print("Playlist name updated successfully from",old_name_string, "to", new_name,"!")
                break
            else:
                print("The name you've chosen already exists!", exists, "time/s. \nPlease try a different one!")
                continue
        except sqlite3.Error:
            print("Database Error")
    db.commit()
    db.close()
update_pl_name()