import sqlite3
import re

# main function
def main():
    show_menu()

# show CLI menu
def show_menu():
    print('____________________________________________')
    print('Welcome to the bookstore database analyzer!')
    print('What would you like to do?')
    print('1 - Show 10 most expensive books')
    print('2 - Show 10 least expensive books')
    print('3 - Search books by keyword')
    print('4 - Close program')
    print()

    # check validity of user input
    while True:
        try:
            choice = int(input('Enter your choice: '))
        except:
            print('You need to input an integer')
            continue
        
        if choice == 1:
            show_most_expensive() # Show top 10 most expensive books
            break
        elif choice == 2:
            show_cheapest() # Show top 10 cheapest books
            break
        elif choice == 3:
            search_by_keyword() # Search for sentences in book descriptions that contain keywords
            break
        elif choice == 4: # Quit program
            print('Goodbye')
            break
        else:
            print('Make sure to enter an integer from 1-4')
        

#Show 10 most expensive books
def show_most_expensive():
    conn = sqlite3.Connection('book_database.db')
    cur = conn.cursor()

    # get titles, prices and genres for top 10 most expensive books 
    cur.execute('''SELECT Title, Price, Genres.Genre_Name FROM Books
                JOIN Genres ON Books.GenreID = Genres.GenreID 
                ORDER BY Price DESC
                LIMIT 10''')
    
    top_10 = cur.fetchall()
    for entry in top_10:
      print(f'Title - "{entry[0]}" | Price - {entry[1]} | Genre - {entry[2]}')

#Show 10 cheapest books
def show_cheapest():
    conn = sqlite3.Connection('book_database.db')
    cur = conn.cursor()

    # get titles, prices and genres for top 10 cheapest books 
    cur.execute('''SELECT Title, Price, Genres.Genre_Name FROM Books
                JOIN Genres ON Books.GenreID = Genres.GenreID 
                ORDER BY Price ASC
                LIMIT 10''')
    
    top_10 = cur.fetchall()
    for entry in top_10:
      print(f'Title - "{entry[0]}" | Price - {entry[1]} | Genre - {entry[2]}')

#Search books by keyword in description
def search_by_keyword():
    conn = sqlite3.Connection('book_database.db')
    cur = conn.cursor()

    keyword = input('Enter a keyword: ') # get input from user
    formated_keyword = f'%{keyword}%' # format input for prepared statement
 
    #   query for titles and descriptions that contain user input
    cur.execute('SELECT Title, Description FROM Books WHERE Description LIKE ?', (formated_keyword,))
    description_query_results = cur.fetchall()

    #   check if user input can be found in an entry, otherwise display message and quit
    if len(description_query_results) == 0:
        print('Keyword does not match an entry')
        quit()

    #   iterate over query results to print titles and sentences which contain user input
    for tuple in description_query_results:
        title = tuple[0]    #   get title
        quoted_sentence = re.search(f'[A-Z][^!.?]*?{keyword}.*?\\.', tuple[1])  #   use re to isolate the sentence that contains user input
        if quoted_sentence != None: #   check if re expression result is empty, otherwise print results
            print(f'"{title}"')
            print(f'"{quoted_sentence.group()}"')
            print()

# Ensure that code is run only when run directly
if __name__ == '__main__':
    main()