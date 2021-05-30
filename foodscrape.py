from bs4 import BeautifulSoup
import requests
import re
import csv
import os.path
import time

url = 'https://www.yelp.com/search?cflt=restaurants&find_loc=Melbourne%2C+Melbourne+Victoria%2C+Australia'
not_page_one = 'https://www.yelp.com/search?cflt=restaurants&find_loc=Melbourne%2C%20Melbourne%20Victoria%2C%20Australia&start='


def find_div_links(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a', {"class": "css-166la90"})
    divs = soup.find_all('div', {
        "class": "border-color--default__09f24__1eOdn text-align--center__09f24__1P1jK"})
    return [divs, links]


def find_last_page(divs):
    for div in divs:
        text = (div.find('span').text)
        page_numbers = int(re.search("[^ ][0-9].*", text).group())
        return page_numbers


def find_links_names(links):
    names_links_list = []
    for link in links:
        if link['name'] != '':
            names_links_list.append({
                'name': link['name'],
                'link': link['href'],
            })
    return names_links_list


def write_to_csv(rows):
    fields = ['name', 'link']
    if os.path.isfile('yelp_name_links.csv'):
        with open('yelp_name_links.csv', 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fields)
            for row in rows:
                print(f"writing row name:{row['name']} link:{row['link']}")
                writer.writerow(row)
    else:
        with open('yelp_name_links.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fields)
            for row in rows:
                print(f"writing row name:{row['name']} link:{row['link']}")
                writer.writerow(row)


def yelp_main_scrape():
    pages = 0
    page = 10
    run = True
    while run:
        if pages == 0:
            url = 'https://www.yelp.com/search?cflt=restaurants&find_loc=Melbourne%2C+Melbourne+Victoria%2C+Australia'
            try:
                [div, links] = find_div_links(url)
                pages = find_last_page(div) * 10 - 10
                print(pages)
                names_links = find_links_names(links)
                write_to_csv(names_links)
            except:
                print("cannot execute")
                print("exitting")
                run = False

        else:
            while page < pages:
                try:
                    not_page_one = f"https://www.yelp.com/search?cflt=restaurants&find_loc=Melbourne%2C%20Melbourne%20Victoria%2C%20Australia&start={page}"
                    [div, links] = find_div_links(not_page_one)
                    names_links = find_link_name(links)
                    write_to_csv(names_links)
                    page += 10
                    if page != pages:
                        print('sleeping.....')
                        time.sleep(60)
                    else:
                        print("this is the last page")
                except:
                    print('cannot execute')
                    print("exitting")
                    run = False
            run = False


def main():
    yelp_main_scrape()


if __name__ == "__main__":
    main()
