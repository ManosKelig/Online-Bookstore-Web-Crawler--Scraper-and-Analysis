# Online Bookstore Web Crawler, Scraper and Analysis

## Description

This project contains a series of scripts that aim to extract information related to books from the website [books.toscrape.com](https://books.toscrape.com/). 

It was created upon completion of the [Python For Everybody](https://www.coursera.org/specializations/python) specialization on [Coursera](https://www.coursera.org/) and the [Starting out with Python](https://www.amazon.com/Starting-Out-Python-Tony-Gaddis/dp/0133582736) textbook by Tony Gaddis in order to explore concepts revolving around web crawling, scraping and the implementation of sqlite3 databases.

The process starts with the creation of the database where the books will be stored along with a list of genres from the website. Then the pages of the website are accessed and the relevant information about the books is scraped and organized into the database. Finally the user can perform some simple analysis operations on the data through the Command Line Interface. 

This project was created with [Python3](https://www.python.org/) and [Sqlite3](https://sqlite.org/index.html)

## Files description

### book_database.py

This script creates the Sqlite3 database file along with the required tables (`Books`, `Genres`). The `Books` table is related to the `Genre` table through the use of a `FOREIGN KEY` (`GenreID`).

### book_scraper.py

This script performs the web-crawl and scraping part of the project. The process begins with requests to the [books.toscrape.com](https://books.toscrape.com/) website utilizing the [Requests](https://docs.python-requests.org/en/latest/index.html) library for Python. Then the contents of the pages are parsed with the use of [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/#) library. 

Each book link from the online bookstore is stored and then accessed so that the necessary data can be scraped and inserted into the database. The book data acquired from the pages consist of:
- Titles
- Genres
- Prices
- Ratings
- Descriptions

A separate list of genres is also created within this script to ensure no duplicate genres are inserted into the database. 

This script also establishes the connection between the `Books` and `Genres` tables by matching the corresponding `ID` from the `Genres` table to the `Genre_ID` of each book on the `Books` table.

The script is run as long as there is another page with books to be scraped. If no other page is found, the script is terminated after collecting the data of the books from the last page.

### book_analysis.py

This script performs some simple data analysis operations on the contents of the database. The user can choose which operation to perform by following the prompts on the Command Line Interface. 
The user can:

- See the 10 most expensive books (with a `SELECT` and `JOIN` statement)
- See the 10 cheapest books (again with a `SELECT` and `JOIN` statement)
- Look up book descriptions containing specific keywords (with the use of a `Regular Expression` pattern)
- See the number of books by `genre` (with the use of an `aggregate function`)
- See the number of books by `rating` (again with an `aggregate function`)

### example_book_database.db

This file is the result of the `book_scraper.py` script. It contains all the data that have been acquired upon completion of the crawling and scraping process in the `Books` and `Genres` tables.

The database contains the following entities:

#### Books

The `Books` table includes:

- `ID` which specifies the unique `ID` of each book as an `INTEGER`. For this reason the column has the `PRIMARY KEY` constraint applied.
- `Title` which specifies the title of each book as `TEXT`. Every entry should minimally contain a title therefore the `NOT NULL` constraint is also applied.
- `GenreID` which references the `ID` column in the `Genres` table, and thus is specified as a `FOREIGN KEY`.
- `Price` which specifies the price of each book as `NUMERIC` in order for effective sorting to be implemented.
- `Rating` which specifies the star-rating each book has on the website as `INTEGER`. The website included descriptions of the rating ('One', 'Two' etc.) which are changed to integers ('1', '2' etc.) by the `book_scraper.py` for database optimization. 
- `Descriptions` which specifies the description of each book on the website as `TEXT`.

#### Genres

The `Genres` table includes:

- `ID` which specifies the unique `ID` of each genre as an `INTEGER`. For this reason the column has the `PRIMARY KEY` constraint applied.
- `Genre_Name` which specifies the name of each genre as `TEXT`. Since no two genres should have the same name, the `UNIQUE` constraint is also applied.

### readme.md

This file contains a description of the project, the files it contains as well as instructions for installation and implementation thereof.

## How to install and run

To run this project, the user needs to have Python3 installed. 

### Copy repository

On cmd:

    git clone https://github.com/ManosKelig/Online-Bookstore-Web-Crawler--Scraper-and-Analysis

and then:

    cd Online-Bookstore-Web-Crawler--Scraper-and-Analysis

### Create virtual environment

    python -m venv venv

### Activate virtual environment

    venv\Scripts\activate

### Ιnstall dependencies

    pip install -r requirements.txt


## How to use

### Build database
The user should begin by running the `book_database.py` file first. This will create the database where book information and genres will be stored. 

    The user should not run this script again after scraping the website, since it will replace the database with an empty one. It should be used again only to restart the database.

### Scrape the website for data

After the database has been created, the `book_scraper.py` script should be run. This will start the automatic process of web-crawling the book URLs of [books.toscrape.com](https://books.toscrape.com/). The user can follow the process on the CLI where they will be able to see which page and the titles of the books being scraped. 

    If the user wants to skip the scraping process, they can use the `example_book_database.db` directly by changing its name to `book_database.db` and proceeding to the next step.

### Analyze the data

Finally, the `book_analysis.py` script should be run, whereupon the user can choose from a list of operations to perform on the data.

## License

This project is not licensed for reuse. It is publicly available for demonstration and portfolio purposes only.
