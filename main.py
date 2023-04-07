import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
from datetime import datetime

def scrape_verge():
    # URL of the webpage to scrape
    url = 'https://www.theverge.com/'

    # Send a GET request to the webpage
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the h2 tags on the webpage
    h2_tags = soup.find_all('h2')
    print(h2_tags)
    data = []

    # Loop through each h2 tag and extract its corresponding author information
    for h2 in h2_tags:
        Headline = h2.text.strip()
        link = h2.find('a')
        if link is not None:
            URL = link['href']
        else:
            URL = print('link not found')
        author_div = h2.find_next_sibling('div', class_='relative z-10 inline-block pt-4 font-polysans text-11 uppercase leading-140 tracking-15 text-gray-31 dark:text-gray-bd')
        if author_div is not None:
            Author = author_div.find('a').text.strip()
            Date = author_div.find('span').text.strip()
        else:
            Author = "not found"
            Date = 'date not found'

        # Append the extracted information to the data list
        data.append((Headline, URL, Author, Date))

        # Print the extracted information
        print('Title:', Headline)
        print('Link:', URL)
        print('Author:', Author)
        print('Date:', Date)
        print('\n')

    return data

def save_to_csv(data):
    filename = datetime.now().strftime('%d%m%Y') + '_verge.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'Headline', 'URL', 'Author', 'Date'])
        for i, row in enumerate(data):
            writer.writerow([i+1] + list(row))


# Function to save the scraped data to an SQLite database
def save_to_database(data):
    conn = sqlite3.connect('verge.db')
    c = conn.cursor()

    # Creating the table
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                (id INTEGER PRIMARY KEY,
                Headline TEXT,
                URL TEXT,
                Author TEXT,
                Date TEXT)''')

    # Inserting the data into the table
    for row in data:
        c.execute('''INSERT OR IGNORE INTO articles (Headline, URL, Author, Date)
                    VALUES (?, ?, ?, ?)''', row)

    # Committing the changes and closing the connection
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # Scrape the data from theverge.com
    data = scrape_verge()

    # Save the data to a CSV file
    save_to_csv(data)

    # Save the data to an SQLite database
    save_to_database(data)

