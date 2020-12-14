import sqlite3
import csv

try:
    conn = sqlite3.connect('TracksDB.db')
except sqlite3.Error:
    print("Database connection failed.")


cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Music
    (performaceId INTEGER, trackId VARCHAR(255), artistName VARCHAR(255), trackName VARCHAR(255), timeSec INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Triplets 
    (userId  INTEGER, trackId VARCHAR(255), listeningDate DATE)''')

conn.commit()

reader = csv.reader(
    open("unique_tracks.txt"), delimiter=";")

for row in reader:
    conn.executemany('''INSERT INTO Music(performaceId, trackId, artistName, trackName, timeSec) VALUES (?, ?, ?, ?, ?)''',reader)

reader = csv.reader(
    open("triplets_sample_20p.txt"), delimiter=";")

for row in reader:
    conn.executemany('''INSERT INTO Triplets (userId, trackId, listeningDate) VALUES (?, ?, ?)''',reader)


print("\nNajpopularniejszy artysta:")
for row in cursor.execute('''SELECT artistName, COUNT(artistName) 
    FROM Music 
    INNER JOIN Triplets ON Music.trackId = Triplets.trackId 
    GROUP BY Music.artistName
    ORDER BY COUNT(artistName) DESC 
    LIMIT 1'''):
    print(row)

print("\nLista 5 najpopularniejszych piosenek:")
for row in cursor.execute('''SELECT trackName, 
    COUNT(Triplets.trackId) 
    FROM Music 
    INNER JOIN Triplets ON Music.trackId = Triplets.trackId 
    GROUP BY Triplets.trackID 
    ORDER BY COUNT(Triplets.trackID) 
    DESC LIMIT 5'''):
    print(row)


conn.close()





