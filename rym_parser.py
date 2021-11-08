from bs4 import BeautifulSoup
import os
import csv


def get_genre(list):
    genre_string = ''
    for x in list:
        if x.endswith("</a"):
            genre_string += x.replace("</a", ':')
    return genre_string


def get_desc(list):
    descriptor_string = ''
    list.pop(0)
    list[0] = list[0].split('>')[1]
    list[len(list) - 1] = list[len(list) - 1].split('<')[0]
    for x in list:
        if x.endswith(','):
            descriptor_string += x.rsplit(',')[0]
            descriptor_string += ':'
    return descriptor_string



def get_album_length(list):
    try:
        return list.split('>')[1].rstrip('</span').lstrip('Total length: ')
    except:
        return None


def write_to_csv(list, filename):
    try:
        with open (filename, 'a', encoding='utf-8', newline='') as fopen:
            csv_writer = csv.writer(fopen)
            csv_writer.writerow(list)
    except:
        return False


def scraped_obs(soup):
    obs = []

    artist_name = str(soup.find('a', class_="artist")).split(sep='>')[1].split(sep='<')[0]  # Artist Name
    artist_album = str(soup.find('meta', itemprop="name")).split(sep='"')[1]  # Album Title
    release_date = str(soup.find("div", class_="issue_info_bottom")).split("=")[3].rsplit(">")[0] .lstrip('"').rstrip('"')
    release_year = release_date[len(release_date)-4:]
    # Release Date
    avg_rating = float((soup.find("span", class_="avg_rating").contents[0].strip()))  # Average Rating
    num_ratings = int(soup.find("span", class_="num_ratings").find("span").contents[0].replace(',', ''))
    # Num of Rating
    primary_genres = get_genre(str(soup.find('span', class_="release_pri_genres")).split('>'))  # primary genres
    secondary_genres = get_genre(str(soup.find('span', class_="release_sec_genres")).split('>'))  # secondary genres
    list_descriptors = get_desc(str(soup.find("span", class_="release_pri_descriptors")).split())  # Descriptors
    total_length = get_album_length(str(soup.find("span", class_="tracklist_total")))

    obs.append(artist_name)
    obs.append(artist_album)
    obs.append(release_year)
    obs.append(avg_rating)
    obs.append(num_ratings)
    obs.append(primary_genres)
    obs.append(secondary_genres)
    obs.append(list_descriptors)
    obs.append(total_length)
    return obs


# Get current working directory
directory = os.getcwd()

# for all the files present in that directory
for filename in os.listdir(directory):
    # check whether the file is having the extension as html and it can be done with endswith function
    if filename.endswith('.html'):
        # os.path.join() method in Python join one or more path components which helps to exactly get the file
        fname = os.path.join(directory, filename)
        print("Current file name ..", os.path.abspath(fname))

        # open the file
        with open(fname, 'r') as file:
            with open(fname, encoding="utf-8", errors='replace') as f:
                page = f.read()
            soup = BeautifulSoup(page, 'html.parser')
            # parse the html as you wish
            write_to_csv(scraped_obs(soup), "Popular All Time Sample.csv")
