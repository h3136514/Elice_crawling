from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException  # 예외처리 추가
import pandas as pd
import time
import os
import requests


# 전국형 유무(분류한 학교 적용여부)
isTotalSchool = True   # 전국형(특정학교) 검색시 True로 변경
while True :
    text = input("전국형 학교(특정학교)로 검색하시겠습니까?(예, 아니요) : ")
    if(text != '예' and text != '아니요'):
        print("예, 아니요만 입력해주세요")
    else:
        if text == '아니요':
            isTotalSchool = False 
        break
    

# 이미지 저장 폴더 생성
image_folder = "images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Chrome 옵션 설정 (선택 사항)
chrome_options = Options()
# chrome_options.add_argument("--start-maximized")  # 브라우저 최대화 옵션
chrome_options.add_argument("headless") # 창 숨기는 옵션

# ChromeDriver 경로 지정 및 실행
service = Service("chromedriver.exe")  # 크롬드라이버 경로
driver = webdriver.Chrome(service=service, options=chrome_options)


# 암시적 대기 (최대 10초)
driver.implicitly_wait(10)

# 초기 설정파일에서 정보 추출
data = []
전국형 = []
with open("init.txt", "r", encoding="utf-8") as f:
    data = f.read().splitlines()
with open("school.txt", "r", encoding="utf-8") as f:
    전국형 = f.read().splitlines()
f.close()
print(전국형)

# 네이버 로그인 정보
NAVER_ID = "" + data[1][data[1].find('=')+1:]
NAVER_PW = "" + data[2][data[2].find('=')+1:]

# 게시판 주소(XPath)
BOARD = "" + data[3][data[3].find('=')+1:]

# 페이지 수
PAGE = int(data[4][data[4].find('=')+1:])
# 한페이지내 게시판 수
BOARDCNT = int(data[5][data[5].find('=')+1:])

# 네이버 로그인
driver.get('https://nid.naver.com/nidlogin.login')

# execute_script()로 아이디, 비밀번호 입력 (보안 우회)
driver.execute_script("document.getElementsByName('id')[0].value = arguments[0]", NAVER_ID)
driver.execute_script("document.getElementsByName('pw')[0].value = arguments[0]", NAVER_PW)

# 로그인 버튼 클릭
driver.find_element(By.ID, 'log.login').click()
time.sleep(1)  # 페이지 이동 간 짧은 대기

주소=[]
이미지확장자 =['jpg', 'JPG', 'png', 'PNG', 'jpeg', 'JPEG']

#전체 게시판 페이지수:(최대 20)
for page in range(1,PAGE,1) :
    try:
        #driver.get(f"https://cafe.naver.com/ArticleList.nhn?search.clubid=30977951&search.menuid=388&search.boardtype=I&search.totalCount=133&search.cafeId=30977951&search.page={page}")   # 겨울학기 계시판
        #driver.get(f"https://cafe.naver.com/ArticleList.nhn?search.clubid=30977951&search.menuid=387&search.boardtype=I&search.totalCount=201&search.cafeId=30977951&search.page={page}")  # 2학기 계시판
        driver.get(f"{BOARD}&search.page={page}")  # 게시판 주소
        driver.implicitly_wait(10)
        driver.switch_to.frame("cafe_main")
        driver.implicitly_wait(20)
        
        # 게시글 접근(한페이지에 20개만)
        for i in range(1,BOARDCNT,1):
            post_element = driver.find_element(By.XPATH, f"/html/body/div[1]/div/ul[1]/li[{i}]/a")
            post_url = post_element.get_attribute("href")
            주소.append(post_url)
            print("게시글링크 : " + post_url)
        
        # iframe 해제
        driver.switch_to.default_content()
        time.sleep(2)  # 페이지 이동 간 짧은 대기
    except NoSuchElementException:  # 해당 요소를 찾을 수 없을 때 예외발갱(페이지 끝)
        print(f"{page}페이지까지 이동 완료했습니다!")
        break
    
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        pass
    
제목=[]
시간=[]
i = 0
for url in 주소:
    driver.get(url)
    driver.switch_to.frame("cafe_main")
    
    본문내용 = driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div").text
    날짜 = driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[1]/div[2]/div[2]/div[2]/span[1]").text # 날짜부문 xpath
    제목내용 = driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[1]/div[1]/div/div/h3").text    # 제목부문 xpath
    
    # 전국형 확인(전국형 학교가 있으면 check = True)
    check = False
    for school in 전국형:
        if(제목내용.find(school) != -1) :
            check = True
            break
       
    #(전국형학교, 서울/인천학교 구분)
    if((check == False and isTotalSchool == True) or (check == True and isTotalSchool == False)):
        continue
    
    제목내용 = 제목내용.replace("/", ".")    # 잘못된 파일 이름형식 변경
    제목.append(제목내용)
    시간.append(날짜[2:10])
    
    print("제목: ", 제목[i], " 시간:", 시간[i], "\n")
    
    # 이미지 다운로드
    image_elements = driver.find_elements(By.TAG_NAME, "img")  # 모든 이미지 태그 찾기
    img_urls = [img.get_attribute("src") for img in image_elements if (img.get_attribute("src") and img.get_attribute("class") == "se-image-resource")] #이미지 주소(단, 게시글에 있는 이미지)

    img_title = 제목[i]
    image_filenames = []
    for img_idx, img_url in enumerate(img_urls):
        if img_url.startswith("http"):  # 유효한 URL인지 확인
            img_ext = img_url.split(".")[-1].split("?")[0]  # 확장자 추출 (png, jpg 등)
            
            # jpg, png 확장자인 사진만(아이콘등 부수적인 이미지 무시)
            img_ext_check = False 
            for ext in 이미지확장자:
                if(img_ext == ext):
                    img_ext_check = True
                    break
           
            if(img_ext_check == False):
                continue
            
            img_filename = f"{시간[i]}_{img_title}_{img_idx + 1}.{img_ext}"
            img_path = os.path.join(image_folder, img_filename)

            # 이미지 다운로드
            try:
                img_data = requests.get(img_url, stream=True)
                if img_data.status_code == 200:
                    with open(img_path, "wb") as f:
                        for chunk in img_data.iter_content(1024):
                            f.write(chunk)
                    image_filenames.append(img_filename)
                    print(f"✅ 이미지 저장: {img_filename}")
            except Exception as e:
                print(f"❌ 이미지 다운로드 실패: {e}")
    
    i += 1
    time.sleep(1)  # 짧은 대기 (너무 빠르면 차단될 가능성)
        

print("✅ 모든 크롤링 완료. images폴더에에 저장됨.")
driver.quit()

input("끝낼려면 Enter를 두번 입력하세요")