from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from time import sleep

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
options.add_argument("user-data-dir=profile-1")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get("https://twitter.com/login")
sleep(5)

# driver.find_element(By.XPATH, '//input[@autocomplete="username"]').send_keys("vx373119@gmail.com")
# sleep(2)
# driver.find_element(By.XPATH, '//span[text()="Next"]').click()
# sleep(3)
# driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]').send_keys("Sa209212")
# sleep(2)
# driver.find_element(By.XPATH, '//span[text()="Log in"]').click()
# sleep(5)

driver.get("https://twitter.com/search?q=%23Messi&src=typed_query&f=live")
sleep(3)

posts = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')

i = 0
for post in posts:
    i += 1
    print(f"Post no.{i}")
    print(post.text)
    print("\n\n\n")

    if i  == len(posts):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

        posts = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')

    if i == 10:
        break

    post.find_element(By.XPATH, '//div[@data-testid="tweetText"]').click()

    sleep(3)
    commentDiv = driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block")
    commentDiv.find_element(By.TAG_NAME, "span").send_keys("Love Messi, Messi is true goat")
    sleep(1)
    driver.find_element(By.XPATH, '//span[text()="Reply"]').click()

    break

print(len(posts))