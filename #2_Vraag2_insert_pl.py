import sqlite3

with sqlite3.connect("chinook.db") as db:
    cursor = db.cursor()

def insert():
    global playlist
    while True:
        try:
            playlist = str(input("<<Specify name for playlist>>: "))
            cursor.execute("SELECT * FROM playlists WHERE Name LIKE (?)", (playlist,))
            data = cursor.fetchall()
            exists = len(data)
            if exists == 0:
                input("Playlist does not exist!\n<<Press ENTER to create it!>>")
                cursor.execute("INSERT INTO playlists (Name) VALUES (?)", (playlist,))
                print("Playlist created successfully in 'Playlists' table at row #",cursor.lastrowid)
                break
            else:
                print("Playlist name already exists",exists,"time/s. Try a different name!")
                continue
        except sqlite3.Error:
            print("Database Error")
    db.commit()
    db.close()
insert()