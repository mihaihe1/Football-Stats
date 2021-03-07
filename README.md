# Football-Stats

Python app that displays current and complete Premier League table & standings for the 2020/2021 season, updated instantly after every game.

## Prerequisites(Libraries)

* BeautifulSoup
* tkinter
* ttkthemes
* requests

![menu](https://user-images.githubusercontent.com/44977942/110236198-2840cc80-7f3d-11eb-97f4-ec46a7ade177.png)

![team](https://user-images.githubusercontent.com/44977942/110236204-2f67da80-7f3d-11eb-82fc-ad98713e6662.png)

## How does it work?

* Used the tkinter library to create a GUI from scratch.
* Built a web scraper with BeautifulSoup to get the info about the teams and their players.(https://fbref.com/en/comps/9/Premier-League-Stats)
* Created a parent class: *Person* and its child classes: *Player*, *Manager*
* Implemented a filter that selects the players that have a certain position: *Goalkeeper*, *Defender*, *Midfielder* and *Attacker*. It is also possible to reset the filter.

![att](https://user-images.githubusercontent.com/44977942/110236482-bc5f6380-7f3e-11eb-8b6c-172c2804db5e.png)
