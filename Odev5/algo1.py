import sqlite3

def similarity(text1, text2):
    set1 = set(text1)
    set2 = set(text2)

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    similarity_coefficient = intersection / union

    return similarity_coefficient

def text_similarity(text1, text2):
    connection = sqlite3.connect("words.db")

    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS words(text TEXT)")

    cursor.execute("INSERT INTO words VALUES(?)", (text1,)) 
    cursor.execute("INSERT INTO words VALUES(?)", (text2,)) 

    connection.commit()

    cursor.execute("SELECT * FROM words") 

    print(cursor.fetchall()) 

    print(f"Similarity ratio between words: {similarity(text1, text2)}")

    cursor.execute("DELETE FROM words") 

    connection.commit()
    connection.close() 
    
    return similarity(text1, text2)
