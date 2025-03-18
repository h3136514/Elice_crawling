# Elice_crawling
해당 프로그램은 (주)엘리스그룹에서 2024년 디지털새싹 사업 정산 관련 업무를 진행하다가 업무의 효율화를 위해 개발한 자동화 프로그램이다.

## <배경>
현장 증빙자료 수집을 위해 디싹 카페 홈페이지에 있는 학교별 현장 사진(교구재 사진)을 자동으로 취합해야 했고 이를 파이썬에서 selenium webdriver를 이용하여 크롤링 자동화를 진행하였다.

## <동작 방식>
맨 밑에 보이는 “실행파일”에서 dist라는 폴더로 이동하면 다음과 같은 파일들이 보입니다.

![15](https://github.com/user-attachments/assets/b9e813b5-bd61-47e8-838a-88a88274cb70)
<div align="center">dist 폴더 내부</div><br>


## <주의사항>
본 실행 파일은 크롬 드라이버를 사용하기 때문에 기존 PC에 크롬이 깔려 있어야 됩니다. 
또한, 오류가 발생할 수 있으므로 최대한 크롬 드라이버의 버전을 PC에 있는 크롬 버전과 일치 하는게 좋습니다.
<br>
(크롬 드라이버 다운 주소 : https://googlechromelabs.github.io/chrome-for-testing/)
![18](https://github.com/user-attachments/assets/7a4f7e6f-f7fd-4a83-8e4e-5a7aa7334708)
<div align="center">크롬 드라이버 버전 확인</div><br>

![17](https://github.com/user-attachments/assets/d801fb12-4b73-4078-91a5-7b408911a060)
<div align="center">PC 크롬 버전 확인</div><br>

파일을 실행하기 전에 init.txt 파일을 열어서 초기설정을 해줘야 합니다.
특히 해당 크롤링은 네이버 카페에 들어가는 것이므로 미리 카페에 가입된 네이버 ID랑 PW를 해당 부분에 적어주면 됩니다.(이때, 띄어쓰기를 하면 안됩니다.)

![14](https://github.com/user-attachments/assets/cdf0de22-80b2-49c2-8d22-ed20e4bbcd94)
<div align="center">init.txt</div><br>

그 다음 “BOARD“ 같은 경우 해당 게시판의 주소를 입력해주면 된다.

![4](https://github.com/user-attachments/assets/9f648f32-61f1-4dde-9385-9ac921b3c006)



![7](https://github.com/user-attachments/assets/ed1c3d03-0cb0-4800-9080-a62c1c077544)
<div align="center">디싹 홈페이지</div><br>

### <게시판 주소가 필요한 이유 및 코드흐름>
게시판 주소가 필요한 이유는 
게시판에서 페이지를 넘길 때 상단에 있는 URL은 동일해 보이나 사실 뒤에 추가적인 주소가 있습니다.
해당 주소를 확인해 보는 방법은 PC에서 F12를 누르고 오른쪽 상단에 Network를 통해 페이지를 옮겨보다 보면 URL 주소 뒤에 추가적인 주소 정보가(&search.page='페이지 번호') 오는 걸 확인 할 수 있습니다.

![8](https://github.com/user-attachments/assets/371de0de-b0da-47f6-a72f-0a36762d5f05)
<div align="center">F12를 누르고 왼쪽 상단에 'Network' 클릭</div><br>

![10](https://github.com/user-attachments/assets/f0e1dd83-5402-44fc-b2d2-a9c9e654f81e)
<div align="center">게시판 페이지 2에 옮겼을 때의 주소</div><br>

다시 게시판 페이지 1에 옮겼을 때의 주소
페이지 수와 한 페이지 내의 게시판 수는 알맞게 대입하면 됩니다.

![6](https://github.com/user-attachments/assets/41f53d47-7f82-43c4-87cb-673017ae40c2)
<div align="center">페이지 수</div><br>

![5](https://github.com/user-attachments/assets/bee3af61-4d92-4c1d-99ef-2d153cbede6d)
<div align="center">한 페이지 내의 게시판 수(20개)</div><br>

school.txt는 크롤링할 대상 학교들을 입력해 주면 됩니다. 이 때 한 줄에 학교 하나만 입력해 주셔야 되고 디싹에서는 전국형 학교들을 대상으로 했습니다. 

![11](https://github.com/user-attachments/assets/94db09c0-d250-491c-8f95-299214d0369e)
<div align="center">school.txt(전국형 학교들)</div><br>

이제 crowling.exe 파일을 열어서 실행하면 됩니다. 실행 하면 맨 처음에 아래와 같이 아까 school.txt 입력한 학교들을 대상으로 잡을지 선택할 수 있습니다.

![12](https://github.com/user-attachments/assets/4625b001-fda2-42ae-8590-347a33cb5b80)
<div align="center">전국형 유무 확인</div><br>

대답을 입력하면 밑에 보이시는 그림과 같이 처음에는 페이지 마다 게시글 링크를 전부 수집하고 그다음 각각의 게시글에 접속하여 학교 일치 여부를 탐색합니다. 만약 일치하면 해당 게시글의 이미지를 다운 받고 파일명을 “날짜“+”제목”+ “순번“을 조합하여 저장해 줍니다.

![13](https://github.com/user-attachments/assets/3b8d220c-c16c-4215-8d1d-230e6ddff847)
<div align="center">게시글 링크 수집</div><br>

![3](https://github.com/user-attachments/assets/03085669-4c3c-468f-9fb2-66e0c448871b)
<div align="center">이미지 저장</div><br>

다 실행이 되고나면 밑에 사진과 같이 images라는 폴더가 생기고 해당 폴더에 해당 학교의 이미지들이 저장된 걸 볼 수 있습니다.

![16](https://github.com/user-attachments/assets/55ee9d81-de99-4706-836d-d23c5f45ee1c)

<div align="center">images 폴더 생성</div><br>

![1](https://github.com/user-attachments/assets/030a05fa-e621-4e94-bf2c-65f0a9c63302)

<div align="center">images 폴더 안</div><br>


(마지막 주의 사항: 해당 코드는 급하게 만들어서 사용하다 보니깐 예외에 대한 처리가 많이 미숙합니다. 사용에 참고 부탁 드립니다. )
