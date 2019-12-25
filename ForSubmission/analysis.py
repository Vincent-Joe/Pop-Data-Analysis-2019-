from konlpy.tag import Okt 
#konlypy는 한국어와 한글에 대한 자연어 처리를 시행해주는 패키지입니다.
#https://konlpy-ko.readthedocs.io/ko/v0.4.3/install/#id2 에서 설치 방법을 확인하실 수 있습니다.
#Okt는 class _okt.py 코드 안에 작성되어있는 클래스입니다. konlpy 에서 제공하는 여러 한글 자연어 분석 라이브러리 중 한 종류입니다. 속도가 제일 빨라 사용하였습니다.
from matplotlib import pyplot
from wordcloud import WordCloud
from collections import Counter

NLpro = Okt() #Natural Language Processor 의 약어로 명칭을 정함. Okt 클래스를 상속함(konlpy 공식 매뉴얼에 나와있는 사용법을 그대로 따른 것).

lyrics_Dict = {key:[] for key in range(2005, 2019)}
#2005년의 가사 단어(스트링)가 모인 리스트: [~~~~], 2006년의 가사 단어(스트링)들이 모인 리스트: [~~~~], ... 2019년의 가사 단어(스트링)들이 모인 리스트:[~~~~]
#를 dict 타입으로 묶은 자료임.
#어차피 뒤에서 lyrics_Dict[key]='새로 만든 리스트' 와 같은 절차를 시행할 것이라서, 굳이 여기서 key: [] 일 필요는 절대 없다. 그냥 단순히 편의를 위해 빈 리스트 []를 넣어둔 것. 

for i in range(2005, 2019):
    #print(i,"년도")
    filename_String = "./resources/lyrics/lyrics"+str(i)+".txt"
    lyrics_File = open(filename_String, "r", encoding="UTF-8")
    #print("파일 엶")
    lyrics_String = lyrics_File.read()
    #print("파일 읽음")
    lyrics_File.close()
    #print("파일 닫음")

    print(str(i)+"년도 모든 차트의 모든 곡들의 가사들을 명사로 분리하는 중입니다...")
    temp_List = NLpro.nouns(lyrics_String)
    #konlpy의 공식 매뉴얼에 기본적인 사용법과 문법이 나와있습니다.
    #.nouns 함수를 이용하면 string 을 input으로 받고, input string 을 명사로 나눈 후 list로 묶습니다. 그리고 그 묶은 list를 output으로 반환합니다.
    lyrics_Dict[i] = temp_List[:]
    print("분리가 완료되었습니다!")

#이제, 모든 명사들 중 한글자 짜리 명사(나, 너, 야, 등등...)을 전부 제거하는 과정을 지금부터 시작한다.
print("한글자 짜리 명사를 제거하는 중...")
lyrics_Dict2 = {key: [] for key in range(2005, 2019)}

for i in range(2005, 2019):
    for i2 in lyrics_Dict[i]:
        if len(i2) != 1:
            lyrics_Dict2[i].append(i2)
print("제거가 완료 되었습니다!")
#한글자짜리 명사 전부 제거 완료.

#이제, 각 년도의 명사들의 빈도를 세는 과정을 지금부터 시작한다.

lyrics_Counter_Dict = {key:[] for key in range(2005, 2019)}
#2005: '2005년 가사들의 명사 빈도 통계', 2006: '2006년 가사들의 명사빈도 통계', ..., 2019: '2019년 가사들의 명사빈도 통계'
#Dict 의 각 value 들은 dict type의 자료형들이다. 

for i in range(2005, 2019):
    print(str(i)+"년도 곡들의 가사들의 명사들의 빈도를 계산하는 중...")
    lyrics_Counter_Dict[i] = dict(Counter(lyrics_Dict2[i]).most_common(200))
    #모든 명사들 중 가장 많이 나온 n 개의 명사들만 선택해서 list 로 모아주는게 .most_common(n) 메서드이다.
    print("계산이 완료되었습니다!")

#print(lyrics_Counter_Dict)

#이제 wordcloud 를 그려서 저장하는 차례이다.

wc = WordCloud(font_path="./resources/BMHANNAAir_ttf.ttf", background_color="white", width=600, height=400)
for i in range(2005, 2019):
    print(str(i)+"년도 곡들의 명사 빈도 시각자료를 생성하는 중...")
    cloud_Object = wc.generate_from_frequencies(lyrics_Counter_Dict[i])
    cloud_Object.to_file("./analysis_result/lyrics"+str(i)+".png")
    print("시각자료 생성이 완료되었습니다!")