# Movie Notes


本專案參考Letterboxd製作，其主功能如下：
1. 心得系統：撰寫並發佈個人心得
2. 追蹤系統：追蹤其他使用者並達到首頁個人化

#### This project is a fan project of Letterboxd. Here are the main features:
1. ✏️ Logging: Write and share reviews.
2. 🗺️ Tracking: Track user's favorite reviewers.
3. 💾 Data Growing: Use python crawler to scrape movies into Movie Notes' own database.
4. 💛 Sending likes: Giving a like to your favorite movies and reviews.
5. 🔍 Searching: Searching movies and users to know more about them.
6. 👁️‍🗨️ Watchlist : Users can build a movie watchlist to remind themselves.


## Backend Skills
1. Using Docker deploying website
2. RESTful API 
3. Database third normal form
4. Using AWS S3 for storing images
5. Accomplishing CDN with AWS CloudFront
5. Web secure with SSL and HTTPS
6. Using flask-bicrypt to encode users passwords
7. Recording user login statement with JWT
8. Using BeautifulSoup to scrape movies info
9. Nginx Reverse proxy


## System Architecture
![image](https://user-images.githubusercontent.com/92343813/173247964-cb09d217-73de-4ede-a08d-e80544ace1f0.png)


## Database Structure
![image](https://user-images.githubusercontent.com/92343813/173248158-65be0dd1-e21b-4f04-a944-88cbfe4b38c4.png)

## Function Introduction

#### Dynamic Homepage
+ Homepage for anonymous user, showing most popular movies this week and reviews with most likes.
![image](https://user-images.githubusercontent.com/92343813/173248683-5be4c5dc-c92f-48f0-ae03-58a336346c2e.png)

+ Reviews with spoilers won't directly show.
![image](https://user-images.githubusercontent.com/92343813/173249039-b0b45371-91fb-41f3-8225-2af41d33b9ed.png)

+ Personalizing homepage after login and following other users.
![image](https://user-images.githubusercontent.com/92343813/173249109-b384f01f-83b1-4950-a909-65c36aa93a32.png)


