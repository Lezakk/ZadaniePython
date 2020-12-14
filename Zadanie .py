import sqlite3
import csv

conn = sqlite3.connect('TracksDB.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Music
    (performaceId INTEGER, trackId VARCHAR(255), artistName VARCHAR(255), trackName VARCHAR(255), timeSec INTEGER)''')

conn.commit()

cursor2 = conn.cursor()

cursor2.execute('''CREATE TABLE IF NOT EXISTS Triplets 
    (userId  INTEGER, trackId VARCHAR(255), listeningDate DATE)''')

conn.commit()

reader = csv.reader(
    open("unique_tracks.txt"), delimiter=";")

for row in reader:
    values = [row[0], row[1], row[2], row[3], row[4]]
    conn.execute('''INSERT INTO Music(performaceId, trackId, artistName, trackName, timeSec) VALUES (?, ?, ?, ?, ?)''',values)

reader = csv.reader(
    open("triplets_sample_20p.txt"), delimiter=";")

for row in reader:
    values = [row[0], row[1], row[2]]
    conn.execute('''INSERT INTO Triplets (userId, trackId, listeningDate) VALUES (?, ?, ?)''',values)


for row in cursor.execute('''SELECT * FROM Music LIMIT 1'''):
    print(row)

for row in cursor2.execute('''SELECT * FROM Triplets LIMIT 1'''):
    print(row)

print("\nNajpopularniejszy artysta:")
for row in cursor2.execute('''SELECT artistName, COUNT(artistName) 
    FROM Music 
    INNER JOIN Triplets ON Music.trackId = Triplets.trackId 
    GROUP BY Music.artistName
    HAVING COUNT(artistName)>1 
    ORDER BY COUNT(artistName) DESC 
    LIMIT 1'''):
    print(row)

print("\nLista 5 najpopularniejszych piosenek:")
for row in cursor.execute('''SELECT trackName, COUNT(Triplets.trackId) FROM Music INNER JOIN Triplets ON Music.trackId = Triplets.trackId GROUP BY Triplets.trackID HAVING COUNT(Triplets.trackID)>1 ORDER BY COUNT(Triplets.trackID) DESC LIMIT 5'''):
    print(row)


conn.close()





