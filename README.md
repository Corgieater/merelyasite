# Movie Notes

### _A movie review website for movie lovers_
_As a movie person, I was thinking about why there is no website for logging and sharing reviews in Taiwan. 
Then I saw my girlfriend using a Japanese website for reviewing books and it has some basic social features.
Voila, this project was born!_

_為了電影愛好者而生的網站_


## Main Features
1. ✏️ Writing and sharing logs: Write and share reviews.
2. 🗺️ Tracking: Track user's favorite reviewers.
3. 💾 Data Growing: Use python crawler with Crontab scheduling and scraping movies from IMDB to database.
4. 💛 Sending likes: Giving a like to your favorite movies and reviews.
5. 🔍 Searching: Searching movies and users to know more about them.
6. 👁️‍🗨️ Watchlist : Users can build a movie watchlist to remind themselves.

_分享電影心得、追蹤其他使用者、對喜歡的評論按讚、搜尋電影或相關評論、建置自己的待看清單、成長型資料庫_


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
+ Setting Crontab to scheduling scraping and writing to database events
+ Using Selenium imitating user typing and clicking when scraping
+ Using Nginx as reverse proxy


## System Architecture
![merelyasite_with_crawler_new](https://user-images.githubusercontent.com/92343813/174992456-c4f71626-4c8d-4fbe-83b3-0dfea874d563.png)



## Database Structure
![image](https://user-images.githubusercontent.com/92343813/173248158-65be0dd1-e21b-4f04-a944-88cbfe4b38c4.png)


## Scraping Bot
### 2 bots for crawling info from IMDB and then writing into database
### 使用爬蟲程式與寫入程式將檔案寫入資料庫中
+ Crawler:
[Scheduled by Crontab, producing a "job done" file after scraping.](https://github.com/Corgieater/crawler)
+ Watcher:
[Schefuled by Crontab, scaning the file to make sure scraping procedure is done and then writing all info into database.](https://github.com/Corgieater/watcher)

## Function Introduction
#### Dynamic Homepage
#### 動態首頁
+ Homepage for anonymous user, showing most popular movies this week and reviews with most likes.
+ 匿名者顯示較熱門之電影與評論、已開始使用帳號的使用者顯示追蹤對象之發文
![image](https://user-images.githubusercontent.com/92343813/173248683-5be4c5dc-c92f-48f0-ae03-58a336346c2e.png)

#### Spoilers Alert
#### 防雷警報
+ Reviews with spoilers won't directly show.
+ 有加上爆雷標籤的評論不會直接秀出來
![image](https://user-images.githubusercontent.com/92343813/173249039-b0b45371-91fb-41f3-8225-2af41d33b9ed.png)

#### User Watchlist
#### 電影待看清單
+ For remebering all the movies users want to watch. Can open a new window about the movie or removing a movie by using the icons.
+ 可編輯待看清單提醒自己有哪些電影還沒看
![image](https://user-images.githubusercontent.com/92343813/173249626-91c8573c-f613-48ae-b0bd-a1cd111778c2.png)

#### User Likes List
#### 使用者喜愛清單
+ Collection of users favorite movies and reviews
+ 按讚後的喜好整理，讓其他人知道使用者喜歡的電影和評論
![image](https://user-images.githubusercontent.com/92343813/173249937-8adab3a9-caf0-4a65-a6b7-33970ed5c3e5.png)

#### Movies Reviewing
#### 電影評論
+ Log movie reviews
+ 記錄使用者的電影評論
![image](https://user-images.githubusercontent.com/92343813/173250047-7eb76a54-31da-49f6-8e3e-4104c229a061.png)

#### Rating Movies
#### 電影評分
+ Rating movies and see how many people rate for it alone with average rate.
+ 評分看過的電影與顯示有多少人對該電影評分
![image](https://user-images.githubusercontent.com/92343813/173250295-274f97a4-88f6-4552-b509-c9322a8fd725.png)

#### Adding Movies
#### 加入資料庫沒有的電影
+ Adding movies to database
    + Using [Cinemagoer](https://imdbpy.readthedocs.io/en/latest/) geting IMDB movie Id and go to IMDB movie page scraping the info.

 ![image](https://user-images.githubusercontent.com/92343813/173250402-e1f8b87e-ca8f-48eb-bcf7-5f42f10da2b4.png)

