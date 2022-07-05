from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import json
import time

running_dataset = []
initial_time = 0
prev_time = 0
limit_links = 0
id_init = 696320

def main():
    global initial_time
    global prev_time
    global limit_links
    
    initial_time=time.time()
    prev_time=initial_time

    links_to_extract = get_all_links("https://www.imdb.com/search/title/?title_type=tv_series&view=simple&sort=num_votes,desc&start=51&ref_=adv_nxt")

    for link in links_to_extract:
        extract_show_data(link)
        time_taken()
        #if limit_links == 3:
        #    break
        #limit_links=limit_links+1

    write_to_file()

def time_taken():
    global prev_time
    current_time=time.time()
    new_time=current_time-prev_time
    prev_time=current_time
    print("Time taken since start/last call: ", new_time)

def total_time_taken():
    global initial_time
    global prev_time
    print("Total time taken until now: ", prev_time-initial_time)

def get_all_links(url):
    all_links = []
    tv_show_list_page = requests.get(url)
    raw_data = BeautifulSoup(tv_show_list_page.text,'html.parser')
    links = raw_data.find_all('a')

    for a_tag in links:
        if re.match('/title', a_tag['href']) != None:
            all_links.append('https://www.imdb.com/'+a_tag['href'])
    
    final_links = list(dict.fromkeys(all_links))
    return final_links

def write_to_file2(obj):
    test_file = open('test.txt', 'a')
    json_data = json.dumps(obj, indent=4)
    test_file.write(json_data)

def write_to_file():
    test_file = open('test.txt', 'a')
    json_data = json.dumps(running_dataset, indent=4)
    test_file.write(json_data)


def title_id_extractor(url):
    filtered_url = re.search('title/.*/', url)
    trunc_end_point = filtered_url.span()[1] - filtered_url.span()[0] -1
    url_id = filtered_url.group()[6:trunc_end_point]
    print(url_id)

def extract_show_data(url):
    global id_init
    
    tv_show_web_page = requests.get(url)
    raw_data = BeautifulSoup(tv_show_web_page.text,'html.parser')


    target_image_link = raw_data.find_all('img')[0]['src']
    target_title_text = raw_data.find_all('h1')[0].string
    target_release_year = raw_data.find_all('span', class_='sc-8c396aa2-2 itZqyK')[0].string[:4]
    target_actors_list = raw_data.find_all(text='Stars')[0].parent.parent.find_all('a')
    target_synopsis = raw_data.find_all('span', class_='sc-16ede01-2 gXUyNh')[0].string

    final_actors_list = []

    for a_tag in target_actors_list:
        if re.match('/name', a_tag['href']) != None:
            final_actors_list.append(a_tag.string)

    final_extracted_data = {
        '_id': format(id_init, 'x'),
        'TVShowTitle': target_title_text,
        'TVShowImage': target_image_link,
        'TVReleaseYear': target_release_year,
        'TVShowActors': final_actors_list,
        'TVShowSynopsis': target_synopsis
    }

    running_dataset.append(final_extracted_data)
    id_init+=1
    

if __name__ == '__main__':
    main()