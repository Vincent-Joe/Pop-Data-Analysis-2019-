import requests
from bs4 import BeautifulSoup
import pickle


#0101, 0108, 0115, 0122, 0129, ... , 1229까지의 월/일 텍스트 데이터를 만드는 과정
mmdd_List = []
for mm in range(1,13):
    for dd in ["01", "08", "15", "22"]:
        if mm<10:
            mmdd_List.append("0"+str(mm)+dd)
        else:
            mmdd_List.append(str(mm)+dd)

#20150101, 20150108, ... , 20181229 까지의 년/월/일 텍스트 데이터를 만드는 과정
yymmdd_List=[]
for yy in range(2005, 2019):
    for mmdd in mmdd_List:
        yymmdd_List.append(str(yy)+mmdd)

#테스트코드{
#print(yymmdd_List)
#print(len(yymmdd_List))
#}테스트코드






#각 연도의 각 주별 모든 차트 페이지 html 코드를 리스트로 만드는 과정
try:
    print("resources 폴더에 차트 웹페이지들의 html 정보가 존재하는지 여부를 확인 중...")
    loadedfile_File = open("./resources/html_of_all_chart.dat", "rb")
    print("resources 폴더에 차트 웹페이지들의 html 정보가 존재합니다.")
    charthtml_List=pickle.load(loadedfile_File)
    print("resources 폴더에 있는 차트 웹페이지들의 html정보를 불러오기 완료.")
    loadedfile_File.close()
    #테스트코드{
    #print(type(charthtml_List))
    #print(charthtml_List[0])
    #}테스트코드
except:
    input("resources 폴더에 차트 웹페이지들의 html정보가 없습니다.\n프로그램을 처음 실행하신 경우인 것 같습니다.\n(계속하려면 엔터를 눌러주세요)")
    input("2005년~2018년 가요 차트 웹페이지 html 정보의 크롤링을 시작하겠습니다.\n(계속하려면 엔터를 눌러주세요)")
    input("크롤링한 html 정보는 resources 폴더에 담깁니다. 필요한 용량은 약 270MB 입니다.\n(계속하려면 엔터를 눌러주세요)")
    input("각 년도당 48개의 차트가 있으며, 총 13년개치의 차트를 받아오기에, 지금부터 총 672개의 웹페이지의 html 정보를 받아옵니다.\n(계속하려면 엔터를 눌러주세요)")
    input("그렇기에 크롤링 과정중 시간이 다소 소요됩니다.\n크롤링을 시작하시려면 엔터를 눌러주세요.")
    charturlBase_String = "https://music.bugs.co.kr/chart/track/week/total?chartdate=" 
    #이 charturlBase_String 변수의 뒤에 mmyydd(string type)만 더해주면 실제 url 문자가 된다.

    charthtml_List=[]

    for i in yymmdd_List:
        print(i+" 당시의 가요 차트의 웹페이지 Html 을 받는 중...")
        charthtml_List.append(requests.get(charturlBase_String+i).text)
        #requests.get 함수의 input은 url 주소, string 타입이다. 잊지 말아야 한다.
        #그리고 requests.get 함수의 output은 어떤 객체인데,
        #이 객체의 .text atrribute 는, 'string 타입'의 '실제 html 코드' 이다!!

    all_html_File = open("./resources/html_of_all_chart.dat", "wb")
    pickle.dump(charthtml_List, all_html_File)
    all_html_File.close()
    print("모든 차트 웹페이지들의 html정보를 resources 폴더에 저장해뒀습니다.")
#여기까지 온 후, charthtml_List 라는 변수에는 총 672개의 html 스트링 데이터들이 List 타입으로 묶여서 담겨있게 된다.
#즉, 여기서 제일 중요한 변수는 charthtml_List 라는 변수이다.
#각 element들의 정보는 실제 html코드라는 것,
#그리고 각 element들의 data type은 'string' 이라는 것을 항상 잊으면 안된다.
#20050101 부터 20181229 까지 총 672개의 차트가 있으니,
#672개의 string data들이 이 리스트에 들어가있는 것이다.




#이제 어떤 차트 웹페이지 하나의 html 하나가 주어지면,
#그 html 에서 '곡정보'버튼을 눌렀을 때
#이동하는 웹페이지(각 트랙의 가사가 담겨있는 웹페이지)의 url를 찾아내는 함수를 작성한다.
def find_trckinfoTagUrl_of_html(inputted_charthtml_String):
    #input data는 string type이어야 한다.
    mySoup=BeautifulSoup(inputted_charthtml_String, "html.parser")
    #위 코드를 통해서 html(string type data)를 beautiful soup가 parsing 할 수 있는 오브젝트 mySoup를 만든다.

    every_trackinfo_a_Tag = mySoup.find_all("a", {"class" : "trackInfo"}) 
    #위 코드를 통해서
    #웹페이지 한개의 html 에서 class 속성의 속성값이 trackInfo 인 a 태그들을, 죄다 모아서,
    #every_trackinfo_a_Tag 라는 변수에 넣는다.
    #단 위 변수는 list 형 데이터가 절대 아니다.
    #find_all, find 메서드의 사용법을 반드시 잘 알아두고 있자. 

    every_trackinfo_url_List=[]
    for i in every_trackinfo_a_Tag:
        every_trackinfo_url_List.append(i["href"])
    #위 코드를 통해서 ever_trackinfo_url_List 라는 List 변수에다가,
    #class 속성의 속성값이 trackInfo인 a 태그의 href 속성의 속성값을,
    #즉 url 주소를,
    #스트링 타입으로써 element로 넣어준다.
    
    #find_all메서드로 나온 ouput의 각 엘리먼트,
    #또는 find 메서드로 나온 output 의 뒤에다가, ["속성"] 을 인덱스로 붙이는 BeautifulSoup의 문법을 꼭 알아두고 있자.
    #굉장히 필수적인 문법인 것 같다.
    #마치 딕셔녀리 타입에서 키값으로 인덱싱하는 것과 비슷한 문법같다.


    return every_trackinfo_url_List
#이 find_trckinfoTagUrl_of_html함수의 input은 string 이다.
#string type data 인 input의 정체는 '차트 한개의 웹페이지의 실제 html 코드' 이다.
#함수의 output은 List이다.
#그리고 이 output List 의 각 element 들은 string type이라는 것도 잊지 말아야 한다.
#그 string type의 data의 정체는 각 곡의 trackinfo 페이지로 이동시켜주는 "URL link"라는 것도 잊지 말아야 한다!!
#한 차트에 총 100개의 트랙이 있으니,
#즉 100개의 '곡정보' 버튼이 있고,
#즉 100개의 '곡정보 페이지로 가는 URL'이 있다.
#그렇기에 이 함수로 나오는 output List에는 '총 100개의 element'가 존재한다.



#이제 어떤 가사정보 웹페이지 하나의 URL 주소가 주어지면,
#그 URL로 들어갔을 때 나오는 가사정보(=곡정보)(=TrackInfo) 웹페이지의 html로부터,
#실제 가사 문장을 string type data로 뽑아내는 함수를 작성한다.
def find_LyricsString_of_URL(inputted_trckinfourl_string):
    #input은 string type의 'url 코드' 이다.
    #그리고 트랙 한개의 '곡정보 웹페이지' 의 url 코드이다!
    
    trckinfo_html_String = requests.get(inputted_trckinfourl_string).text
    mysoup=BeautifulSoup(trckinfo_html_String, "html.parser")
    title_Tag = mysoup.find("title") #곡정보 페이지에서 운좋게 '제목/가수' 의 내용이 <title>태그에 있어서 그걸 그대로 가져오기만 하면 된다.
    lyrics_Tag = mysoup.find("xmp")
    #위에서 이미 BeautifulSoup모듈의 mysoup오브젝트의 .find 메서드, .find_all메서드의 사용법을 잘 배웠지?
    #BeautifulSoup 만의 특별한 tag object를 output으로 뽑아내는 매우 유용한 메서드다.
    #html을 뜯어보면 실제 가사 텍스트는 <xmp> 태그로 쌓여있다는 것을 알 수 있다.

    #테스트코드{    print(type(lyrics_Tag))    }테스트코드
    #보다시피 find 메서드로 뽑아낸 자료인 lyrics_Tag는, 출력은 이쁘게 되지만 절대 string 타입이 아닌 beautiful soup만의 특별한 tag object 라는 것을 알 수 있다.
    
    if str(lyrics_Tag) == "None": #가사가 없는 곡일 경우 이렇게 해줘야 빈 텍스트를 반환해준다. 예를들면 https://music.bugs.co.kr/track/80033927?wl_ref=list_tr_08_ab 와 같은 경우들.
        return ""
    
    title_String = title_Tag.text
    title_String = title_String [:-4]
    lyrics_String = lyrics_Tag.text
    #.find, .find_all 로 뽑아낸 tag object에서 실제 컨텐츠 내용을 'String Type으로!!!!' 뽑아내는 방법이다.
    
    return title_String+"\n\n"+lyrics_String
#이 함수의 input은, 웹페이지 한 개의 실제 URL 주소 string type data.
#이 함수의 output은 실제 가사 string type data.


'''
#테스트코드{
print(find_LyricsString_of_URL("https://music.bugs.co.kr/track/1523734?wl_ref=list_tr_08_ar"))
# }
'''


'''
for i in range(2005, 2019):
    counter=0
    i=str(i)
    for i2 in yymmdd_List:
        if i==i2[:4]:
            counter += 1
    print(i+"년도 차트의 갯수:",counter)
input("test")
#672개의 차트는 각 년도마다 48개의 차트로 총 14년이 모여있다는 것을 확인 할 수 있다.
'''





#가사 말고 곡정보 웹페이지의 URL이 input으로 주어지면
#그 웹페이지의 html 로부터 곡의 '제목/가수' 정보를 string 타입으로 반환하는 함수도 작성해본다.
def find_TitleString_of_URL(inputted_URL_String):
    #input은 string type의 'url 코드' 이다.
    #그리고 트랙 한개의 '곡정보 웹페이지' 의 url 코드이다!
    webpage_Object = requests.get(inputted_URL_String).text
    mySoup = BeautifulSoup(webpage_Object, "html.parser")

    title_Tag = mySoup.find("title")
    title_String = title_Tag.text
    title_String = title_String[:-4] #문자열의 마지막에 붙어있는 "- 벅스" 라는 단어를 빼주는 역할

    return title_String
#이 함수의 input은, 웹페이지 한 개의 실제 URL 주소 string type data.
#이 함수의 output은 실제 곡 제목/아티스트 string type data.




'''
#다시 복습
#제일 중요한 데이터 1.charthtml_List - 리스트형 변수. 672개의 html string data 가 담겨있음.
#제일 중요한 데이터 2.find_trckinfoTagUrl_of_html() - 함수. input은 html string. output은 url string을 모아둔 list.
#제일 중요한 데이터 3.find_LyricsString_of_URL() - 함수. input은 url string. output은 실제 가사 string.
#제일 중요한 데이터 3.find_TitleString_of_URL() - 함수. input은 url string. output은 실제 제목/아티스트 string.
'''




#2005년, 2006년, 2007년, ... 2018년까지, 각 년도마다의 모든 차트의 가사를 크롤링해오는 과정
input("\n이제 각 년도의 차트들에 있는 모든 가요들의 가사들의 크롤링을 시작하겠습니다.\n(엔터를 눌러 계속해주세요)")
input("한 년도마다 48개의 차트가 있고, 한 차트에는 100개의 곡이 있습니다.\n(엔터를 눌러 계속해주세요)")
input("그렇기에 지금부터 한 년도당 4800 곡의 가사를 크롤링 하게 됩니다.\n(엔터를 눌러 계속해주세요)")
input("총 13년x4800곡='67200곡' 의 가사를 크롤링하기 때문에 시간이 다소 오래 걸립니다.\n(엔터를 눌러 계속해주세요)")
input("크롤링한 가사 텍스트 파일은 'resources/lyrics'폴더에 저장됩니다.\n(엔터를 눌러 계속해주세요)")
input("크롤링을 시작하시려면 엔터를 눌러주세요.")
for yy in range(2005, 2019):
    print(str(yy)+"년도의 차트들에 있는 모든 가요들의 가사들을 받아오는 중...")
    file_directory_String="./resources/lyrics/lyrics"+str(yy)+".txt"

    try:
        reading_File = open(file_directory_String, "r")
        print("\n"+str(yy)+"년도의 차트들에 있는 가요들의 가사는 이미 pc에 존재합니다.")
        print("./resources/lyrics 폴더의 lyrics"+str(yy)+".txt 파일을 통해서 크롤링한 가사를 확인하실 수 있습니다.")
        print("다음 년도의 가사 파일의 크롤링을 시작합니다.\n")
        reading_File.close()

    except:
        writing_File = open(file_directory_String, "a", encoding="UTF-8")
        index_Adder=(yy - 2005) *48

        for indexer_Num in range(0,48): #각 연도마다 48개의 차트 html 이 list에 담겨있으므로 range(0,48)을 해준다. 예컨대 2005년도의 차트는 charthtml_List[0]~charthtml_List[47]이고, 2006년도의 차트는 charthtml_Lit[48]~charthtml_List[95]이다.
            print(str(yy)+"년도의 "+str(indexer_Num+1)+"번째 차트의 모든 가요들의 가사들을 받아오는 중...")
            url_List = find_trckinfoTagUrl_of_html(charthtml_List[indexer_Num+index_Adder])
            for url_String in url_List:
                writing_File.write(find_LyricsString_of_URL(url_String))
                writing_File.write("\n\n\n\n")
            

        print(str(yy)+"년도의 모든 차트의 모든 가요들의 가사들을 받았습니다.\n")
        writing_File.close()

print("\n\n가사 크롤링 완료!!\n")






#2005년, 2006년, 2007년, ... 2018년까지, 각 년도마다의 모든 차트의 '곡제목,아티스트'를 크롤링해오는 과정
input("\n이제 각 년도의 차트들에 있는 모든 가요들의 '곡 제목,아티스트' 목록의 크롤링을 시작하겠습니다.\n(엔터를 눌러 계속해주세요)")
input("크롤링을 시작하시려면 엔터를 눌러주세요.")
for yy in range(2005, 2019):
    print(str(yy)+"년도의 차트들에 있는 모든 가요들의 '곡 제목,아티스트' 목록을 받아오는 중...")
    file_directory_String_2="./resources/title/title_and_artist"+str(yy)+".txt"

    try:
        reading_File = open(file_directory_String_2, "r")
        print("\n"+str(yy)+"년도의 차트들에 있는 가요들의 제목과 아티스트 정보는 이미 pc에 존재합니다.")
        print("./resources/title 폴더의 title_and_artist"+str(yy)+".txt 파일을 통해서 크롤링한 정보를 확인하실 수 있습니다.")
        print("다음 년도의 '곡 제목,아티스트' 정보의 크롤링을 시작합니다.\n")
        reading_File.close()

    except:
        writing_File = open(file_directory_String_2, "a", encoding="UTF-8")
        index_Adder=(yy - 2005) *48

        for indexer_Num in range(0,48): #각 연도마다 48개의 차트 html 이 list에 담겨있으므로 range(0,48)을 해준다. 예컨대 2005년도의 차트는 charthtml_List[0]~charthtml_List[47]이고, 2006년도의 차트는 charthtml_Lit[48]~charthtml_List[95]이다.
            print(str(yy)+"년도의 "+str(indexer_Num+1)+"번째 차트의 모든 가요들의 곡 제목, 아티스트 목록을 받아오는 중...")
            url_List = find_trckinfoTagUrl_of_html(charthtml_List[indexer_Num+index_Adder])
            for url_String in url_List:
                writing_File.write(find_TitleString_of_URL(url_String))
                writing_File.write("\n")
            

        print(str(yy)+"년도의 모든 차트의 모든 가요들의 '곡 제목,아티스트' 목록을 받았습니다.\n")
        writing_File.close()

print("\n\n곡 제목, 아티스트 이름 크롤링 완료!!\n\n")

#이제 title_and_artist2005, ... , title_and_artist2018 파일들을 하나의 total.txt 파일로 묶는 과정이다.
print("다운 받은 각 년도의 모든 곡들의 '곡 제목, 아티스트' 목록 정보를 하나의 파일로 통합중...")
try:
    reading_File = open("./resources/title/total.txt", "r")
    reading_File.close()
    print("통합된 '곡 제목, 아티스트 목록' 정보가 이미 존재합니다")
    print("./resources/title 폴더의 total.txt 파일을 통해서 크롤링한 정보를 확인하실 수 있습니다.")
except:
    writing_File = open("./resources/title/total.txt", "a", encoding="UTF-8")
    for yy in range(2005, 2019):
        file_directory_String_2="./resources/title/title_and_artist"+str(yy)+".txt"
        reading_File = open(file_directory_String_2, "r", encoding="UTF-8")
        copied_String = reading_File.read()
        writing_File.write(copied_String)
        reading_File.close()
    writing_File.close()

#이제 total.txt 파일을 total_title.txt 파일과 total_artist.txt 파일로 나누는 과정이다.
total_File = open("./resources/title/total.txt", "r", encoding="UTF-8")
total_title_File = open("./resources/title/total_title.txt", "w", encoding="UTF-8")
total_artist_File = open("./resources/title/total_artist.txt", "w", encoding="UTF-8")
everyline_List = total_File.readlines()

for title_artist in everyline_List:
    title_String=title_artist.split("/")[0].strip()
    if len(title_artist.split("/"))==1:
        artist_String=""
    else:
        artist_String=title_artist.split("/")[1].strip()
    total_title_File.write(title_String+"\n")
    total_artist_File.write(artist_String+"\n")

total_File.close()
total_title_File.close()
total_artist_File.close()

print("\n\n모든 작업 완료!!!\n\n")
input("수고하셨습니다. 엔터를 눌러 프로그램을 종료해주세요.")