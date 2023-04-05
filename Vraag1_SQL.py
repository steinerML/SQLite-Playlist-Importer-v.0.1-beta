import sqlite3

with sqlite3.connect("chinook.db") as db:
    cursor = db.cursor()
def exam_1():
    try:
        input("<<Press ENTER to view Album TOP 10 query>>: ")
        cursor.execute("""SELECT a.name AS "Artist Name", ab.Title AS "Album Title", 
                    COUNT(ab.AlbumId) AS "Beluisterd"
                    FROM artists AS a, albums AS ab, invoice_items AS i, tracks AS t
                    WHERE a.ArtistId = ab.ArtistId AND ab.AlbumId = t.AlbumId AND t.TrackId = i.TrackId
                    GROUP BY ab.AlbumId
                    ORDER BY Beluisterd DESC
                    LIMIT 10;""")
        data = cursor.fetchall()
        id,artist,album,times = 'Id',"Artist Name:","Album Title:","# Beluisterd"
        print("%-5s %-30s %-40s %20s\n" % (id,artist,album,times)) #Headers area delimiter
        for index,x in enumerate(data,1):
            print("%-5s %-30s %-40s %15s" % (index,x[0],x[1],x[2])) #Line area delimiter        
    except sqlite3.Error:
        print("Database Error")
    db.close()
exam_1()