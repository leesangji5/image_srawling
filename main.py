from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import urllib.request
import os
import time

# 찾고 싶은 이미지 검색어, 다운로드할 이미지 개수(이미지가 부족할 수 있음)
search_term = "apple".replace(' ', '+')
count = 500
a = 0

# 이미지를 저장할 폴더 생성
if not os.path.exists("./"+search_term):
    os.mkdir("./"+search_term)
else:
    a = len(os.listdir("./"+search_term))

# 웹 드라이버 실행, 구글 이미지 검색 접속
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://www.google.com/search?sca_esv=565998106&q={}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwj-mc6izLCBAxWFl1YBHWcbAYsQ0pQJegQIDRAB&biw=1920&bih=910&dpr=1".format(search_term))

# 이미지 로딩을 위해 스크롤 내리기
thumbnail_results = []
last_height = driver.execute_script("return document.body.scrollHeight")
while len(thumbnail_results) < count:
    thumbnail_results = driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd") # 이미지 태그 찾기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3) # 로딩 시간 대기

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height: # 스크롤을 다 내려도 이미지가 없으면 스크롤 종료
        count = len(thumbnail_results) # 찾은 이미지 개수로 변경
        break
    last_height = new_height

k = 0
for img in thumbnail_results:
    try:
        k += 1 # 이미지 개수 카운트
        print("downloading image {} of {}".format(k, count), end="")
        urllib.request.urlretrieve(img.get_attribute("src"), "./"+search_term+"/"+search_term+"_"+str(k+a)+".jpg") # 이미지 다운로드
        print(" - done")

        if k == count: # 이미지 개수만큼 다운로드 받으면 종료
            break
    except: continue
driver.quit()
