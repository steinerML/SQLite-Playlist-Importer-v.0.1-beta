import sqlite3

with sqlite3.connect("chinook.db") as db:
    cursor = db.cursor()

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
                                    #db.commit()
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
    db.close()
import_songs()