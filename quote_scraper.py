import requests
from bs4 import BeautifulSoup


def find_quotes(url='https://hazbinhotel.fandom.com/wiki/Alastor/Quotes'):
    temp = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            quote_divs = soup.find_all('div', class_='quote')
            for quote_div in quote_divs:
                italic_text = quote_div.find('i')
                if italic_text:
                    temp.append(italic_text.get_text())
        else:
            print(f"Failed to retrieve URL: {url}")
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")\

    return temp
