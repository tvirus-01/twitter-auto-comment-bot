import email
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json

from time import sleep
import shutil
import os
import mysql.connector

from datetime import date

class Scraper:

    def __init__(self, headlessStatus=True):
        self.isHeadless = headlessStatus
        self.td = date.today().strftime("%d%m%Y")

        config = {
                "DB_HOST":"database-twi.c5wuc1hsxwv9.ap-southeast-1.rds.amazonaws.com",
                "DB_NAME":"twitter_bot",
                "DB_USER":"admin",
                "DB_PASSWORD":"qfmrAnuJgzeLRw6"
            }

        self.host = config["DB_HOST"]
        self.name = config["DB_NAME"]
        self.user = config["DB_USER"]
        self.password = config["DB_PASSWORD"]
        self.conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password, db =self.name)
        self.cur = self.conn.cursor()

        self.runDriver()
    
    
    def startDriver(self):
        options = Options()
        
        options.headless = self.isHeadless
        options.add_argument("--window-size=1920,1080")
        # options.add_argument(f"user-data-dir={self.profile}")
        # options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        return driver


    def getUser(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()

        return rows


    def addCount(self, count, userName):
        self.cur.execute(f"SELECT * FROM user_comment_count WHERE user_name='{userName}' AND date_var='{self.td}' ")
        rowsA = self.cur.fetchall()

        try:
            comment_countA = int(rowsA[0][3]) + count

            self.cur.execute(f"UPDATE user_comment_count SET comment_count='{comment_countA}' WHERE id={rowsA[0][0]}")
            self.conn.commit()
        except:
            pass

        self.cur.execute(f"SELECT * FROM users WHERE user_name='{userName}'")
        rowsA = self.cur.fetchall()

        try:
            comment_countA = int(rowsA[0][7]) + count

            self.cur.execute(f"UPDATE users SET total_comments='{comment_countA}' WHERE id={rowsA[0][0]}")
            self.conn.commit()
        except:
            pass
    

    def commentCount(self, userName):

        self.cur.execute(f"SELECT * FROM user_comment_count WHERE user_name='{userName}' AND date_var='{self.td}' ")
        rows = self.cur.fetchall()

        if len(rows) == 0:
            self.cur.execute(f"INSERT INTO user_comment_count VALUES (NULL, '{userName}', '{self.td}', '0')")
            self.conn.commit()

            comment_count = "0"
        else:
            comment_count = rows[0][3]

        if int(comment_count) <= 500:
            return True

        return False

    
    
    def login(self, driver, userEmail, userPass, userName):
        driver.get("https://twitter.com/login")
        sleep(5)

        try:
            driver.find_element(By.XPATH, '//input[@autocomplete="username"]').send_keys(userEmail)
            sleep(2)
            driver.find_element(By.XPATH, '//span[text()="Next"]').click()
            sleep(3)

            try:
                driver.find_element(By.XPATH, '//input[@autocomplete="on"]').send_keys(userName)
                sleep(2)
                driver.find_element(By.XPATH, '//span[text()="Next"]').click()
                sleep(3)
            except:
                pass

            driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]').send_keys(userPass)
            sleep(2)
            driver.find_element(By.XPATH, '//span[text()="Log in"]').click()
            sleep(5)

        except:
            pass

        try:
            driver.find_element(By.XPATH, f'//div[@data-testid="UserAvatar-Container-{userName}"]')
        except:
            return False

        self.cur.execute(f"UPDATE users set is_loggedin='{1}' WHERE id={self.userId} ")
        self.conn.commit()
        
        return True

    
    
    def doComment(self, driver, tweetLink, comment):
        driver.execute_script("window.open('about:blank','secondtab');")
        driver.switch_to.window(driver.window_handles[1])

        try:
            print(f"Commenting: {tweetLink}")
            driver.get(tweetLink)
            sleep(3)
            commentDiv = driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block")
            commentDiv.find_element(By.TAG_NAME, "span").send_keys(comment)
            sleep(1)
            driver.find_element(By.XPATH, '//span[text()="Reply"]').click()
            sleep(1)
            print("comment done")
        except:
            print(f"unable to do comment {tweetLink} might be loggin issue")

        driver.switch_to.window(driver.window_handles[0])

    
    
    def searchPost(self, driver, query, comment, userName):

        query = query.replace("#", "%23")

        queryUrl = f"https://twitter.com/search?q={query}&src=typed_query&f=live"
        print(queryUrl)

        driver.get(queryUrl)
        sleep(3)

        posts = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')

        i = 0
        for x in range(10):
            
            for post in posts:
                i += 1
                print(f"Post no.{i}")
                print(post.text)

                for a in post.find_elements(By.TAG_NAME, "a"):

                    if "/status" in str(a.get_attribute("href")):
                        tweetLink = a.get_attribute("href")

                        self.doComment(driver, tweetLink, comment)
                        sleep(2)

                print("\n\n")

                if i >= 10:
                    break

            if i >= 10:
                break

            sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            sleep(2)
            posts = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')
            sleep(1)

        self.addCount(i, userName)

        print(f"I--{i}")

    
    
    def runDriver(self):

        print("running the commenter")

        for row in self.getUser():
            self.userId = row[0]
            userName = row[1]
            userEmail = row[2]
            userPass = row[3]
            userComment = row[4]
            userHashtags = row[5]
            isLoggedin = row[6]

            self.profile = f"/home/shaki/pydocs/chrome-profile"

            # self.profileMain = f"profile-{userName}-main"
            # print(f"userName:{userName}, userEmail:{userEmail}, userPass:{userPass}, userComment:{userComment}, userHashtags:{userHashtags}, isLoggedin:{isLoggedin}, ")

            driver = self.startDriver()

            # try:
            Login = self.login(driver, userEmail, userPass, userName)
            if Login == False:
                print("Login Error")
                return "login_error"

            hashtags = userHashtags.split(",")

            for hashtag in hashtags:
                print(hashtag)

                isCommentCount = self.commentCount(userName)
                if isCommentCount:
                    self.searchPost(driver, hashtag, userComment, userName)

                break
            # except:
            #     pass

            # sleep(10)
            driver.quit()

            # shutil.rmtree(self.profile, ignore_errors=True)
        


# Scraper(headlessStatus=False)