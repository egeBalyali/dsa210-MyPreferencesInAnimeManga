# dsa210-MyPreferencesInAnimeManga
I read a lot of manga, and have watched numerous animes. But when I search for a new one it is always a toss-up. So in this project I will first parse My Anime List with its APİ. This site is where I record my reading list as well as my points.
I will first explore this data and create some graphs. And then I plan on creating a machine learning model to guess if I will like it.

Research Questions:
Do I have some strong preferences in manga and anime?
Can a model guess my rating for shows?


Data:
The site where I record my watch and read history has almost every anime/manga published in Japan. They include almost every information about these shows, like release date, average rating, voice actors and authors and characters and so forth.
The important attributes that I will need: {"chapter count", "how many chapters ı read", "is it finished","average score", "genres", "tags", "when was it published"}

#How To Run With Flask
First create a virtual environment with
python -m venv C:\path\to\new\virtual\environment

Then install the requirements

pip install -r .\requirements.txt

Then run 
python /app.py
