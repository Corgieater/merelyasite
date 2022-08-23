# Movie Notes

### _A movie review website for movie lovers_
_As a movie person, I was thinking about why there is no website for logging and sharing reviews in Taiwan. 
Then I saw my girlfriend using a Japanese website for reviewing books and it has some basic social features.
Voila, this project was born!_
### Website Url : https://merelyasite.xyz/


## Main Features
1. ✏️ Writing and sharing logs: Write and share reviews.
2. 🗺️ Tracking: Track user's favorite reviewers.
3. 💾 Data Growing: Use python crawler with crontab scheduling and scraping movies from IMDB to database.
4. 💛 Sending likes: Giving a like to your favorite movies and reviews.
5. 🔍 Searching: Searching movies and users to know more about them.
6. 👁️‍🗨️ Watchlist : Users can build a movie watchlist to remind themselves.


## Technique
### Frontend
+ HTML
+ CSS
+ Javascript

### Backend
+ Deploying website with docker
+ Using Python/Flask environment
+ Following RESTful API 
+ Optimizing Database with third normal form
+ Using AWS S3 for storing images
+ Accomplishing CDN with AWS CloudFront
+ Securing website with SSL and HTTPS
+ Using Flask-Bcrypt to encode users passwords
+ Recording user login statement with JWT
+ Using BeautifulSoup4 to scrape movies info
+ Setting crontab to scheduling scraping and writing to database events
+ Using Selenium imitating user typing and clicking when scraping
+ Using Nginx as reverse proxy


## System Architecture
![merelyasite_with_crawler_new](https://user-images.githubusercontent.com/92343813/174992456-c4f71626-4c8d-4fbe-83b3-0dfea874d563.png)



## Database Structure
![image](https://user-images.githubusercontent.com/92343813/173248158-65be0dd1-e21b-4f04-a944-88cbfe4b38c4.png)



## Function Introduction
#### Dynamic Homepage
+ Homepage for anonymous user, showing most popular movies this week and reviews with most likes.
![image](https://user-images.githubusercontent.com/92343813/173248683-5be4c5dc-c92f-48f0-ae03-58a336346c2e.png)

#### Spoilers Alert
+ Reviews with spoilers won't directly show.
![image](https://user-images.githubusercontent.com/92343813/173249039-b0b45371-91fb-41f3-8225-2af41d33b9ed.png)

### User Watchlist
+ For remebering all the movies users want to watch. Can open a new window about the movie or removing a movie by using the icons.
![image](https://user-images.githubusercontent.com/92343813/173249626-91c8573c-f613-48ae-b0bd-a1cd111778c2.png)

### User Likes List
+ Collection of users favorite movies and reviews
![image](https://user-images.githubusercontent.com/92343813/173249937-8adab3a9-caf0-4a65-a6b7-33970ed5c3e5.png)

### Movies Reviewing
+ Log movie reviews 
![image](https://user-images.githubusercontent.com/92343813/173250047-7eb76a54-31da-49f6-8e3e-4104c229a061.png)

### Rating Movies
+ Rating movies and see how many people rate for it alone with average rate.
![image](https://user-images.githubusercontent.com/92343813/173250295-274f97a4-88f6-4552-b509-c9322a8fd725.png)

### Adding Movies
+ Adding movies to database
    + Using [Cinemagoer](https://imdbpy.readthedocs.io/en/latest/) geting IMDB movie Id and go to IMDB movie page scraping the info.

 ![image](https://user-images.githubusercontent.com/92343813/173250402-e1f8b87e-ca8f-48eb-bcf7-5f42f10da2b4.png)

