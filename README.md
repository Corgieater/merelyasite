# Movie Notes


### _A movie review website for movie lovers_
_As a movie person, I was thinking about why there is no website for logging and sharing reviews in Taiwan. 
Then I saw my girl friend using a Japanese website for reviewing books and it has some basic social features.
Voila, this project was born!_


## Main fratures
1. ✏️ Logging: Write and share reviews.
2. 🗺️ Tracking: Track user's favorite reviewers.
3. 💾 Data Growing: Use python crawler to scrape movies into Movie Notes' own database.
4. 💛 Sending likes: Giving a like to your favorite movies and reviews.
5. 🔍 Searching: Searching movies and users to know more about them.
6. 👁️‍🗨️ Watchlist : Users can build a movie watchlist to remind themselves.


## Function Introduction
#### Dynamic Homepage
+ Homepage for anonymous user, showing most popular movies this week and reviews with most likes.
![image](https://user-images.githubusercontent.com/92343813/173248683-5be4c5dc-c92f-48f0-ae03-58a336346c2e.png)

+ Reviews with spoilers won't directly show.
![image](https://user-images.githubusercontent.com/92343813/173249039-b0b45371-91fb-41f3-8225-2af41d33b9ed.png)

+ Personalizing homepage after login and following other users.
![image](https://user-images.githubusercontent.com/92343813/173249109-b384f01f-83b1-4950-a909-65c36aa93a32.png)

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
![image](https://user-images.githubusercontent.com/92343813/173250402-e1f8b87e-ca8f-48eb-bcf7-5f42f10da2b4.png)

## Technique
### Front
+ HTML
+ CSS
+ Javascript

### Backend
+ Using Docker deploying website
+ RESTful API 
+ Database third normal form
+ Using AWS S3 for storing images
+ Accomplishing CDN with AWS CloudFront
+ Web secure with SSL and HTTPS
+ Using flask-bicrypt to encode users passwords
+ Recording user login statement with JWT
+ Using BeautifulSoup to scrape movies info
+ Nginx Reverse proxy


## System Architecture
![image](https://user-images.githubusercontent.com/92343813/173434370-b352ada3-c07e-49a1-8a90-ae60bba89b49.png)



## Database Structure
![image](https://user-images.githubusercontent.com/92343813/173248158-65be0dd1-e21b-4f04-a944-88cbfe4b38c4.png)


