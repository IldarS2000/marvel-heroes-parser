from selenium import webdriver
from bs4 import BeautifulSoup
import csv



def get_html(url):
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    return html


def get_links(html):
    soup = BeautifulSoup(html, 'lxml')

    divs = soup.find_all('div', class_='grid-base grid__6')
    links = divs[1].find_all('a', class_='explore__link')
    links = ['https://www.marvel.com' + link.get('href') for link in links]

    return links


def get_info(link):
    html = get_html(link)
    soup = BeautifulSoup(html, 'lxml')

    span = soup.find('span', class_='masthead__headline')
    name = span.text.strip()

    uls = soup.find_all('ul', class_='railBioLinks')
    info = [ul.text.strip() for ul in uls]

    return (name, info)


def main():
    url = 'https://www.marvel.com/characters'
    html = get_html(url)


    links = get_links(html)
    
    dataset = []
    for link in links:
        info = get_info(link)
        hero = [info[0], link] + info[1]
        print(hero)
        dataset.append(hero)


    with open('dataset.csv', 'w', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerows(dataset)





if __name__ == '__main__':
    main()

