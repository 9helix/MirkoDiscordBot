import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import pickle
from discord import Color


class anime:
    def __init__(self, url):
        self.name = "Unknown"
        self.tag = ""
        self.episodes = "Unknown"
        self.cur_episodes = "Unknown"
        self.airing = "Unknown"
        self.broadcast = "Unknown"
        self.status = "Unknown"
        self.url = url
        self.season = "Unknown"
        self.cover_url = None
        self.countdown = ""
        self.genre = "Unknown"
        self.studio = "Unknown"

    def fetch_data(self):
        page = requests.get(self.url)

        soup = bs(page.content, 'html.parser')
        stats = soup.find_all("span", {"class": "dark_text"})
        self.name = soup.find("h1", {"class": "title-name h1_bold_none"}).text
        self.tag = self.url[30:35]
        image = soup.find("img", {"itemprop": "image"})['data-src']
        self.cover_url = image
        for i in stats:
            if i.text == "Aired:":
                airing = i.parent.text
                self.airing = airing[10:-3]
                airing_start = self.airing[:-5]
            if i.text == "Broadcast:":
                broadcast = i.parent.text
                self.broadcast = broadcast[16:-7]
                broadcast = broadcast[16:-13]

                broadcast_hour = broadcast.split()[2]

            if i.text == "Episodes:":
                episodes = i.parent.text
                self.episodes = episodes[13:-3]

            if i.text == "Status:":
                status = i.parent.text
                self.status = status[11:-3]
            if i.text == "Premiered:":
                premiered = i.parent.text
                self.season = premiered[12:-1]
            if i.text == "Studios:":
                studio = i.parent.text
                self.studio = studio[10:-1]
            if "Genre" in i.text:
                genre1 = i.findNext("span").text

                #genre2 = i.findNext("span").findNext("span").text
                #print(genre1, genre2)
                self.genre = f"{genre1}"
                #self.season = premiered[12:-1]

        if self.status == "Currently Airing":
            time = airing_start+" "+broadcast_hour
            start = datetime.strptime(time, '%b %d, %Y %H:%M')
            start = start - timedelta(hours=9)
            cur_episodes = (datetime.utcnow()-start).days//7
            self.cur_episodes = cur_episodes
            time_left = timedelta(days=(cur_episodes+1)*7) - \
                (datetime.utcnow()-start)
            countdown = "\n\nNext episode in: "
            days = time_left.days
            if days > 0:
                countdown += str(days)+" days, "
            hours = time_left.seconds//3600
            if hours > 0:
                countdown += str(hours)+" hours, "
            minutes = (time_left.seconds % 3600)//60
            if minutes > 0:
                countdown += str(minutes)+" minutes, "
            seconds = (time_left.seconds % 3600) % 60
            if seconds > 0:
                countdown += str(seconds)+" seconds"
            self.countdown = countdown+"."
            self.episodes = f"{cur_episodes}/{self.episodes}"

    def __str__(self):
        return f"Name: {self.name}\nEpisodes: {self.episodes}\nStatus: {self.status}\nAiring: {self.airing}\nSeason: {self.season}\nBroadcast: {self.broadcast}\nGenre: {self.genre}\nStudio: {self.studio}\nURL: {self.url}{self.countdown}"


#url = "https://myanimelist.net/anime/49596/Blue_Lock"
#show = anime(url)
# show.fetch_data()
genres = {"Action": Color.brand_red(), "Adventure": Color.orange(), "Comedy": Color.gold(), "Drama": Color.purple(), "Sci-Fi": Color.green(), "Fantasy": Color.brand_green(),
          "Horror": Color.darker_grey(), "Romance": Color.fuchsia(), "Mystery": Color.dark_teal(), "Sports": Color.blue(), "Supernatural": Color.dark_green(), "Slice of Life": Color.yellow()}
"""
with open('database/anime_dict.pkl', 'rb') as f:
    anime_dict = pickle.load(f)

#anime_dict[show.tag] = show.url
with open('database/anime_dict.pkl', 'wb') as f:
    pickle.dump(anime_dict, f)
for item in anime_dict:
    print(item, anime_dict[item])"""
# print(show)
