from matplotlib import pyplot
from matplotlib import font_manager, rc
from collections import Counter


font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
#pyplot.rcParams["font.family"] = font_name

everytrack_List=[]
for i in range(2005, 2019):
    temp_File = open("./resources/title/title_and_artist"+str(i)+".txt", "r", encoding="UTF-8")
    for tracks in temp_File.readlines():
        everytrack_List.append(tracks)
    temp_File.close()

#element strings 앞 뒤의 \n 문자들 제거하기
temp_List =[] 
for tracks in everytrack_List:
    temp_List.append(tracks.strip())
everytrack_List=temp_List[:]
#앞 뒤의 \n 문자들 제거하기 완료

#print(len(everytrack_List))

#가수들 리스트 뽑기
everyartist_List=[]
for tracks in everytrack_List:
    splitted_string_List = tracks.split('/')
    if len(splitted_string_List)!=2:
        continue
    else:
        everyartist_List.append(splitted_string_List[1])
#가수들 리스트 뽑기 완료

track_set = set(everytrack_List)
artist_set = set(everyartist_List)

print(len(track_set), len(artist_set))

track_Count = Counter(everytrack_List)
artist_Count = Counter(everyartist_List)

print(dict(track_Count.most_common(20)).keys())
print(dict(track_Count.most_common(20)).values())
print(dict(artist_Count.most_common(20)).keys())
print(dict(artist_Count.most_common(20)).values())

pyplot.barh(list(dict(artist_Count.most_common(20)).keys())[::-1], list(dict(artist_Count.most_common(20)).values())[::-1] )
pyplot.show()

pyplot.barh(list(dict(track_Count.most_common(20)).keys())[::-1], list(dict(track_Count.most_common(20)).values())[::-1] )
pyplot.show()