import requests
from bs4 import BeautifulSoup
import sqlite3

# main function
def main():

    # Establish a connection to an SQLite database
    conn = sqlite3.Connection('book_database.db')
    cur = conn.cursor()

    # Set base domain for scraping
    domain = 'https://books.toscrape.com/'
    url = domain  # Initial URL to scrape from
    next_page_flag = True  # Controls pagination: keep scraping while there's a next page
    genre_list = []  # Store genres already added to the database to avoid duplicates

    GENRE_INDEX_UL= 2 # position of index for the genre in the 'ul'tag
    PRICE_INDEX = 0 # position of index for price on 'p' tag
    MIN_NUM_CHAR_DESCRIPTION = 50 # assumed minimum number of characters for a 'p' tag to contain description

    # Loop through all pages while there is a "next" page
    while next_page_flag:

        # Request the current page and parse its content with BeautifulSoup
        r = requests.get(url)
        print('Scanning page:', url)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Find all html <a> tags (which may contain links to books)
        book_url_list = []
        a_tags = soup('a')  # Extract all <a> tags
        for tag in a_tags:
            if tag.get('title') != None:  # Only consider <a> tags with a 'title' attribute (book links) - add them to a list to be scraped for info
                book_url = tag.get('href', None)  # Get the URL from the href attribute
                # If URL doesn't start with 'catalogue/', prepend it
                if book_url.startswith('catalogue/') == False:
                    book_url = 'catalogue/' + book_url
                book_url_list.append(book_url)  # Add to the list of book URLs         

        # Visit each individual book page and extract required information
        for book_url in book_url_list:
            book_page = domain + book_url  # Construct full URL for the book
            book_r = requests.get(book_page)
            book_soup = BeautifulSoup(book_r.content, 'html.parser')

            # Extract the book title
            header = book_soup.find('h1')
            title = header.text
            print(title) # print title to the CLI to keep track of which book is being scraped

            # Extract the genre (category) from breadcrumb navigation
            ul_tags_book = book_soup.find('ul')  # Get the unordered list of navigation links
            a_tags_book = ul_tags_book.find_all('a')
            genre = a_tags_book[GENRE_INDEX_UL].text  # The third <a> tag contains the genre

            # If genre is not already in the list, insert it into the Genres table
            if genre not in genre_list:
                genre_list.append(genre)
                cur.execute('''INSERT INTO Genres(Genre_Name)
                        VALUES (?)''', (genre,))
                
            # Get genre id to be inserted into the books table
            cur.execute('''SELECT GenreID FROM Genres WHERE Genre_Name = ?''', (genre,))
            genre_id = cur.fetchone()[0]

            # Extract the book's price (first <p> tag contains price)
            p_tag = book_soup.find('p')
            price = p_tag.contents[PRICE_INDEX]
            formatted_price = float(price.lstrip('£'))

            # Extract the rating from <p> tag with class "star-rating"
            p_tags = book_soup('p')
            for tag in p_tags:
                class_contents = tag.get('class')
                if class_contents != None and class_contents[0] == 'star-rating': # position[0] is 'star-rating' and [1] the actual rating
                    rating = class_contents[1]  # e.g., "Three", "Four"
                    # Convert rating from text to integer
                    if rating == 'One':
                        rating = 1
                    elif rating == 'Two':
                        rating = 2
                    elif rating == 'Three':
                        rating = 3
                    elif rating == 'Four':
                        rating = 4
                    elif rating == 'Five':
                        rating = 5

                # Extract the book description (longest <p> text is assumed to be the description   
                if len(tag.text) > MIN_NUM_CHAR_DESCRIPTION:
                    description = tag.text

            # provide a default description to prevent crash
            if description == None or len(description) < MIN_NUM_CHAR_DESCRIPTION:
                description = 'No description available' 

            # Insert the book into the Books table along with all scraped data
            cur.execute('''INSERT INTO Books (Title, GenreID, Price, Rating, Description)
                        VALUES (?,?,?,?,?)''',
                        (title, genre_id, formatted_price, rating, description))
            
        # Check if there is a "next" page and update the URL accordingly
        next_button = soup.find('li', class_ = 'next')
        if next_button:
            next_page = next_button.find('a').get('href')
            if next_page.startswith('catalogue'): # Update URL for next iteration, ensuring proper format
                url = domain + next_page
            else:
                url = domain + 'catalogue/' + next_page
            next_page_flag = True
        else:
            next_page_flag = False  # If there isn't a next page link, set flag to false to terminate while loop on next iteration 

    conn.commit()  # Commit all changes to the database

    # Close the database connection after scraping is complete
    conn.close()


# Ensure that code is run only when run directly
if __name__ == '__main__':
    main()