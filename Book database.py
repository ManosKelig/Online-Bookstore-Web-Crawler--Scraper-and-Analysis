import sqlite3

# main function
def main():
    create_table()

# creates tables necessary for scraping process
def create_table():

    # establish connection to database
    conn = sqlite3.Connection('book_database.db')
    cur = conn.cursor()

    # delete tables to start with a clean database
    cur.execute('DROP TABLE IF EXISTS Books')
    cur.execute('DROP TABLE IF EXISTS Genres')

    # create Books table. link to Genres table with FOREIGN KEY GenreID
    cur.execute('''CREATE TABLE Books
                (BookID INTEGER PRIMARY KEY UNIQUE, 
                Title TEXT,
                GenreID INTEGER, 
                Price NUMERIC (5, 2),
                Rating INTEGER,
                Description TEXT,
                FOREIGN KEY(GenreID) REFERENCES Genres(GenreID))''')
    
    # Create Genres table
    cur.execute('''CREATE TABLE Genres
                (GenreID INTEGER PRIMARY KEY UNIQUE,
                Genre_Name TEXT UNIQUE)''')
        
    print("'book_database.db' has been created.")
    
    # Commit changes to database
    conn.commit()

    # Close connection
    conn.close()

# Ensure that code is run only when run directly
if __name__ == '__main__':
    main()