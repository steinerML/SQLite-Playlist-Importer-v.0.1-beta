import sqlite3
import os

with sqlite3.connect("chinook.db") as db:
    cursor = db.cursor()

#All function calls are commented because I decided to work on the functions separately and then join everything!
#READ FILE -Enter .TXT filename and check whether exists or not-.
def read_file():
    file_name = str(input("<<Please enter filename (.TXT extension not needed)>>: "))
    filenameraw = file_name + ".txt"
    try:
        with open (filenameraw) as f:
            contents = f.readlines()
            file_size = os.path.getsize(filenameraw)
        with open (filenameraw) as f:
            lines = len(f.readlines())
            print("<<File read successfully!>>")
            view_content = input("Want to know the number of songs it contains(y/n)? ")
            if view_content == 'y':             
                print("Here the song/s in the file:\n")
                for index, song in enumerate(contents,1):
                    print(index,song)               
                print("\n<<Number of songs in file:",lines,"song/s.>>")
                print("<<File size is",file_size,"bytes>>\n")              
            elif view_content == 'n':
                print("\n<<No worries, we'll show you the songs before importing.>>")
            else:
                print("<<Invalid Input! Input must be either YES(y) or NO(n)>>")
    except FileNotFoundError:
        print("<<Sorry we couldn't find " + filenameraw + " may not exist or typo error>>")
#read_file()

#CREATE playlist name into DB and check whether exists or not. (playlists table)

def insert_pl():
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
    #db.close()
#insert_pl()


#3 Import songs into Playlist

def import_songs():
    try:
        file_name = str(input("<<Please enter filename (.TXT extension not needed)>>: "))
        filenameraw = file_name + ".txt"
        #print("These are the keywords we will search for:\n")        
        with open (filenameraw) as f:
            content = f.read().splitlines()
            print(content)
            for index, track in enumerate(content,1):
                print("\nKeyword#",index,track)
                #Search Engine @ _tracks table. For simplicity I just want to know if a TrackId exists for every keyword/line in TXT file!
                cursor.execute("""SELECT t.TrackId FROM tracks AS t INNER JOIN albums AS ab
                                    ON ab.ArtistId = a.ArtistId INNER JOIN artists AS a
                                    ON ab.AlbumId = t.AlbumId WHERE t.name LIKE ? ;""",(track + "%",))
                dataset = cursor.fetchall()
                exists = len(dataset)
                if exists == 0:
                    print("<<Nothing found for", track,">>")
                    input("<<Press ENTER to continue!>>")
                elif exists == 1:
                    print("<<Track will be imported automatically. Track found",exists,"time.>>")
                    input("Press ENTER to import song into Playlist! ")
                    cursor.execute("""INSERT INTO playlist_track SELECT (SELECT PlaylistId
                                    FROM playlists ORDER BY PlaylistId DESC LIMIT 1),
                                    (SELECT TrackId FROM tracks AS t WHERE t.name LIKE ? );""",(track + "%",))
                    db.commit()
                else:
                    print("Keyword returned ",exists, "results.")
                    input("<<Press ENTER to see drop-down menu and select song>>\n")
                    cursor.execute("""SELECT t.name AS "Track Name",a.name AS "Artist Name"
                    FROM tracks AS t INNER JOIN albums AS ab ON ab.ArtistId = a.ArtistId
                    LEFT JOIN artists AS a ON ab.AlbumId = t.AlbumId 
                    WHERE t.name LIKE ? ;""",(track + "%",))
                    several = cursor.fetchall()
                    for index,track in enumerate(several,1):
                        print(index,*track)
                    
                    def track_import():
                        while True:
                            try:
                                selection = int(input("\n<<Please make your selection>>: "))
                                if selection >= 1:
                                    full_selection = several[selection-1][0]
                                    print("Your selection:",selection,"'", full_selection,"'")
                                    input("<<Press ENTER to import selected song into playlist!>>")
                                    cursor.execute("""INSERT INTO playlist_track SELECT (SELECT PlaylistId
                                            FROM playlists ORDER BY PlaylistId DESC LIMIT 1),
                                            (SELECT TrackId FROM tracks AS t WHERE t.name LIKE ? );""",(full_selection + "%",))
                                    print("Song imported successfully!")
                                    break
                                else:
                                    print("Invalid input! No negatives, zeroes or text allowed, only integers starting at 1!")
                                    continue                    
                            except sqlite3.Error:
                                print("Database Error")
                            except ValueError:
                                print("Enter only integers not characters!")
                        db.commit()
                    track_import()                       
    except FileNotFoundError:
        print("<<Sorry we couldn't find the .TXT file>>")
    except sqlite3.Error:
        print("Database Error")   
    db.commit()
    #db.close()
#import_songs()

#4 Update Playlist name.

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
    #db.close()
#update_pl_name()

#5 View Playlist Content.

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
            print(index,*song,"\n")
    except sqlite3.Error:
        print("Database Error")
    db.commit()
    #db.close()
#view_playlist_content()

#6 Delete last created Playlist

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
    #db.close()
#delete_playlist()

def menu():
    again = True
    while again:
        try:
            print(""""--- Playlist Importer v.0.1 beta ---
Welcome to the .TXT to SQLite Importer App, where a .TXT file is read
and songs are added to a playlist from the Chinook DB.

Please, choose one of the options below:

1) Read .TXT file & content preview (.TXT extension not needed)
2) Create Playlist.
3) Import Songs into Playlist.
4) Update Playlist Name.
5) View Playlist Content.
6) Delete Playlist.
7) Exit.""")
            selection = int(input("Please make your selection: "))
            print(f"You have selected option {selection}")
            if selection == 1:
                read_file()
            elif selection == 2:
                insert_pl()
            elif selection == 3:
                import_songs()
            elif selection == 4:
                update_pl_name()
            elif selection == 5:
                view_playlist_content()
            elif selection == 6:
                delete_playlist()
            elif selection == 7:
                print("Thank you and Good bye!")
                again = False
            else:
                print("Incorrect menu selection, please try again.")
        except ValueError:
            print("No characters! Only integers!")
menu()
db.close()
