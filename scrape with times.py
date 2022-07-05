from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import json
import time

running_dataset = []

def main():
    
    extract_show_data("https://www.imdb.com/title/tt0903747/")
    #links_to_extract = get_all_links("https://www.imdb.com/search/title/?title_type=tv_series&view=simple&sort=num_votes,desc&start=51&ref_=adv_nxt")

    #for link in links_to_extract:
    #    extract_show_data(link)

    #write_to_file()

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

    t_0=time.time()
    
    tv_show_web_page = requests.get(url, headers={"Range": "bytes=0-1"})
    t_1=time.time()
    print("Time to get page: ", t_1-t_0)

    raw_data = BeautifulSoup(tv_show_web_page.text,'html.parser')
    t_2=time.time()
    print("Time to prase: ", t_2-t_1)

    target_image_link = raw_data.find_all('img')[0]['src']
    t_3=time.time()
    print("Time to find image: ", t_3-t_2)

    target_title_text = raw_data.find_all('h1')[0].string
    t_4=time.time()
    print("Time to find title: ", t_4-t_3)

    target_release_year = raw_data.find_all('span', class_='TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex')[0].string[:4]
    t_5=time.time()
    print("Time to find date: ", t_5-t_4)

    target_actors_list = raw_data.find_all(text='Stars')[0].parent.parent.find_all('a')
    t_6=time.time()
    print("Time to find actors: ", t_6-t_5)


    target_synopsis = raw_data.find_all('span', class_='GenresAndPlot__TextContainerBreakpointXL-sc-cum89p-2 eqbKRZ')[0].string
    t_7=time.time()
    print("Time to find actors: ", t_7-t_6)

    final_actors_list = []

    for a_tag in target_actors_list:
        if re.match('/name', a_tag['href']) != None:
            final_actors_list.append(a_tag.string)
    t_8=time.time()
    print("Time to find populate array: ", t_8-t_7)

    final_extracted_data = {
        'TVShowTitle': target_title_text,
        'TVShowImage': target_image_link,
        'TVReleaseYear': target_release_year,
        'TVShowActors': final_actors_list,
        'TVShowSynopsis': target_synopsis
    }

    running_dataset.append(final_extracted_data)
    write_to_file()
    t_9=time.time()
    print("Time to write to file: ", t_9-t_8)
    print("Total time taken: ", t_9-t_0)

if __name__ == '__main__':
    main()