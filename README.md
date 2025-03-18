# project stock.

I have made this to test my django skills in websockets and celery. This project is basic real time stock price indicatir and a simple graph based visualization 
of the stocks. I haved used websockets ans celery to update the stock data in real-time.
I have used a library yfianace for getting the stock data.

* how to use ?
1. Clone this project and run it locally to use it features.
2. Now run the command "python manage.py makemigrations" and then "python manage.py migrate" this will setup your database. [I have used dbsqlite as it a practice level app.]
3. I have used redis channel layer. so you need redis on your system.
4. Now open a new terminal and run the commands to run the celery worker and celery beat.[You will grt the commands online.]
5. now just run "python manage.py runserver" and your application is good to go.
6. A url link will be provided to you. first hit the url "the provided url/stocks" which will direct you to stock page.
7. Now wait for 1 minute so data will appear automatically and will keep on until server is closed.


In this app I wrote the backend logic and html and javaScript but css is done by AI.
