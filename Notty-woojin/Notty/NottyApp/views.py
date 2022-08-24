from tracemalloc import start
from urllib import response
from xml.dom.minidom import Attr
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from .forms import RouteForm
from .models import Route
import json
import datetime
import pytz
import time
import schedule

from django.http.request import HttpHeaders
from django.http import HttpResponse


key_num = '6f4d796a726a6f77353772777a4e48'
path_key = '646f7a76646a6f7733317842746455'


'''
화면에 표시 할 자료
sht_line : 처음 탄 지하철의 호선 (최단 시간)
min_line : 처음 탄 지하철의 호선 (최소 환승)
sht_path_list : 최단 시간 경로
min_path_list : 최소 환승 경로
trans_line : 1회 환승 한 이후 지하철의 호선(최단시간)
trans_station : 1회 환승 한 환승역(최단시간)
joined_path_station_list : 출발지부터 1회 환승 전 까지의 경로(최단시간)
after_trans_path_list : 1회 환승 이후 지하철 경로(최단시간)
---------------------------------------------------
trans_line2 : 2회 환승 한 이후 지하철의 호선(최단시간)
trans_station2 : 2회 환승 한 지하철역(최단시간)
joined_path_station_list2 : 1회 환승 역에서 2회 환승 전 까지의 경로(최단시간)
after_trans_path_list2 : 2회 환승 이후 지하철 경로(최단시간)
---------------------------------------------------
trans_line3 : 3회 환승 한 이후 지하철의 호선(최단시간)
trans_station3 : 3회 환승 한 지하철역(최단시간)
joined_path_station_list3 : 2회 환승 역에서 3회 환승 전 까지의 경로(최단시간)
after_trans_path_list3 : 3회 환승 이후 지하철 경로(최단시간)
---------------------------------------------------
min_trans_line : 1회 환승 한 이후 지하철의 호선(최소환승)
min_trans_station : 1회 환승 한 환승역(최소환승)
min_joined_path_station_list : 출발지부터 1회 환승 전 까지의 경로(최소환승)
min_after_trans_path_list : 1회 환승 이후 지하철 경로(최소환승)
---------------------------------------------------
min_trans_line2 : 2회 환승 한 이후 지하철의 호선(최소환승)
min_trans_station2 : 2회 환승 한 지하철역(최소환승)
min_joined_path_station_list2 : 1회 환승 역에서 2회 환승 전 까지의 경로(최소환승)
min_after_trans_path_list2 : 2회 환승 이후 지하철 경로(최소환승)
---------------------------------------------------
min_trans_line3 : 3회 환승 한 이후 지하철의 호선(최단시간)
min_trans_station3 : 3회 환승 한 지하철역(최단시간)
min_joined_path_station_list3 : 2회 환승 역에서 3회 환승 전 까지의 경로(최단시간)
min_after_trans_path_list3 : 3회 환승 이후 지하철 경로(최단시간)
'''

trans_line = ''
min_trans_line = ''
after_trans_path_list = ''
after_trans_path_list3 = ''
min_after_path_list = ''
min_joined_path_station_list = ''
joined_path_station_list = ''
joined_path_station_list2 = ''
trans_line2 = ''
trans_line3 = ''
trans_station2 = ''
after_trans_path_list2 = ''
min_line = ''
min_trans_line2 = ''
min_trans_station2 = ''
min_joined_path_station_list2 = ''
min_after_trans_path_list2 = ''
joined_path_station_list3 = ''
sht_joined_station_code_list3 = ''
min_joined_path_station_list3 = ''
min_after_trans_path_list3 = ''
min_joined_station_code_list3 = ''
sht_joined_station_code_list2 = ''
min_joined_station_code_list2 = ''
sht_joined_station_code_list1 = ''
min_joined_station_code_list1 = ''
real_time_position = ''
real_time_position1 = ''
sht_joined_time_table_list = ''
sht_joined_time_table_list1 = ''
sht_joined_time_table_list2 = ''
sht_joined_time_table_list3 = ''
sht_path_trans_cnt = ''
sht_line = ''
line_obj = ''
obj = ''
sht_path_msg = ''
path_time = ''
trans_path_time = ''
sht_path_list = ''
dest_obj = ''
path_obj = ''
context = {}
temp_line = ''
sht_joined_train_num_list = ''
sht_joined_train_num_list1 = ''
sht_joined_train_num_list2 = ''
sht_joined_train_num_list3 = ''
min_after_trans_path_list = ''
destword = ''
real_time_line = ''
real_time_line1 = ''
sht_real_path_list = ''
real_next_station = ''
real_next_station1 = ''
arrive_tag = ''
arrive_tag1 = ''
left_tag = ''
left_tag1 = ''
last_time = ''
found = ''
time_tag = 0
time_tag1 = 0
min_path_time = ''
min_path_trans_cnt = ''
min_path_msg = ''
min_joined_train_num_list = ''
min_path_list = ''
min_joined_time_table_list = ''
user_token = ''
resgistration = []
notification_cnt = 0
found_cnt = 0

# Create your views here.


def home(request):
    global destword
    global user_token
    if request.method == 'POST':
        print('POST 요청 홈에서')
        form = RouteForm(request.POST)
        searchword = request.POST.get('start')
        destword = request.POST.get('fin')

        if searchword == '역삼역':
            searchword = '역삼'
        elif destword == '역삼역':
            searchword = '역삼'

        if searchword.endswith('역'):
            searchword = searchword.replace('역', '')
        if destword.endswith('역'):
            destword = destword.replace('역', '')

        user_token = request.POST.get('user_token')

        if form.is_valid():
            # 데이터 저장
            rt = Route()
            rt.start = request.POST['start']
            rt.fin = request.POST['fin']
            rt.save()

            global dest_obj
            global sht_joined_time_table_list
            global sht_joined_time_table_list1
            global sht_joined_time_table_list2
            global sht_joined_time_table_list3
            global min_trans_line
            global after_trans_path_list
            global after_trans_path_list3
            global min_after_trans_path_list
            global min_joined_path_station_list
            global joined_path_station_list
            global joined_path_station_list2
            global joined_path_station_list3
            global sht_path_list
            global trans_line
            global path_obj
            global obj
            global trans_line2
            global trans_line3
            global trans_station2
            global after_trans_path_list2
            global min_line
            global min_trans_line2
            global min_trans_station2
            global min_joined_path_station_list2
            global min_after_trans_path_list2
            global sht_path_msg
            global time_set
            global path_time
            global trans_path_time
            global sht_joined_station_code_list3
            global min_joined_path_station_list3
            global min_after_trans_path_list3
            global min_joined_station_code_list3
            global sht_joined_station_code_list2
            global min_joined_station_code_list2
            global sht_joined_station_code_list1
            global min_joined_station_code_list1
            global real_time_position
            global real_time_position1
            global sht_path_trans_cnt
            global line_obj
            global temp_line
            global sht_line
            global sht_joined_train_num_list
            global sht_joined_train_num_list1
            global sht_joined_train_num_list2
            global sht_joined_train_num_list3
            global last_time
            global min_joined_train_num_list
            global min_path_list
            global min_joined_time_table_list
            global min_path_trans_cnt
            global min_path_msg
            global notification_cnt
            notification_cnt = 0
            print("--->>>", request.POST.get('answers'))

            answer = request.POST.get('answers')
            print(answer)

            # 시간 구하기
            KST = pytz.timezone('Asia/Seoul')

            now = datetime.datetime.now(KST)
            print(now.year)
            print(now.month)
            print(now.day)
            print(now.hour)
            print(now.minute)
            print(now.second)
            print(now.microsecond)
            print(now.weekday())
            if now.weekday() < 5:
                week_tag = '1'
                print('평일임')
            elif now.weekday() == 5:
                week_tag = '2'
                print('토요일임')
            elif now.weekday() == 6:
                week_tag = '3'
                print('일요일임')

            str_day = now.strftime('%Y%m%d')
            str_time = now.strftime('%H:%M:%S')
            print(str_day)
            print(str_time)
            test_time = ('12:00:01')

            holidate = holiday(now.year)
            print(holidate)

            for item in holidate:
                if str_day == item:
                    week_tag = '3'
                    print('공휴일임')

            ######################################
            # 카카오 REST API KEY = 3ccf2a2e8eef7ee20af37e425477d818
            # 출발 위치 좌표 잡기
            headers = {
                'Authorization': 'KakaoAK 3ccf2a2e8eef7ee20af37e425477d818',
            }

            params = {
                'page': '1',
                'size': '1',
                'sort': 'accuracy',
                'query': searchword+'역',
            }

            st_gps_response = requests.get(
                'https://dapi.kakao.com/v2/local/search/keyword.json', params=params, headers=headers)
            st_gps_resdata = st_gps_response.text
            st_gps_obj = json.loads(st_gps_resdata)
            st_gps_obj = st_gps_obj['documents']

            for item in st_gps_obj:
                st_gps_x = item.get('x')

            for item in st_gps_obj:
                st_gps_y = item.get('y')

            # 도착 위치 좌표 잡기
            params = {
                'page': '1',
                'size': '1',
                'sort': 'accuracy',
                'query': destword+'역',
            }

            dest_gps_response = requests.get(
                'https://dapi.kakao.com/v2/local/search/keyword.json', params=params, headers=headers)
            dest_gps_resdata = dest_gps_response.text
            dest_gps_obj = json.loads(dest_gps_resdata)
            dest_gps_obj = dest_gps_obj['documents']

            for item in dest_gps_obj:
                dest_gps_x = item.get('x')

            for item in dest_gps_obj:
                dest_gps_y = item.get('y')

            '''
            #서울특별시_대중교통환승경로 조회 서비스 https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000414
            trans_path_key = '1WiWiadJdsEUw9VTAe8%2BpAs4K39k6ulLAGzN%2BBDvLuUedlyrTLO%2FwKXqkXW%2FEuTRT%2FLepS1etUJeBAyOvq9xVg%3D%3D'
            trans_path_api_url = 'http://ws.bus.go.kr/api/rest/pathinfo/getPathInfoBySubway?ServiceKey='+trans_path_key+'&startX='+st_gps_x+'&startY='+st_gps_y+'&endX='+dest_gps_x+'&endY='+dest_gps_y+'&resultType=json'
            trans_path_response = requests.get(trans_path_api_url)
            trans_path_resdata = trans_path_response.text
            trans_path_obj1 = json.loads(trans_path_resdata)
            trans_path_obj = trans_path_obj1['msgBody']
            trans_path_obj = trans_path_obj['itemList']
            trans_path_list = []
            for item in trans_path_obj:
                trans_path_list = item.get('pathList')
            
            print(trans_path_list)
            print('\n\n\n')
            print('테스트텟트\n')
            print(trans_path_obj1)
            '''

            real_time_position = searchword

            # 지하철 경로 조회 서비스 (최단 시간) https://devming.tistory.com/214 |http://swopenAPI.seoul.go.kr/api/subway/인증Key값/요청데이터형식/OpenAPI 이름(서비스명)/요청 데이터 행 시작번호/요청 데이터 행 끝번호/출발역명/도착역명
            path_api_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
                key_num+'/json/shortestRoute/0/10/'+searchword+'/'+destword
            path_response = requests.get(path_api_url)
            path_resdata = path_response.text
            path_obj = json.loads(path_resdata)
            try:
                path_obj = path_obj['shortestRouteList']
            except KeyError:
                print("keyerror")

            # 최단 시간 찾기
            path_time = [9999, 9999, 9999, 9999,
                         9999, 9999, 9999, 9999, 9999, 9999]

            i = 0
            try:
                for time_set in path_obj:
                    path_time[i] = int(time_set.get('shtTravelTm'))
                    i = i+1
            except AttributeError:
                print("AttributeError")
            min_sht_path_time = min(path_time)
            for item in path_obj:
                sht_path_list = item.get('shtStatnNm')
                sht_path_msg = item.get('shtTravelMsg')
                sht_path_trans_cnt = item.get('shtTransferCnt')
                sht_path_time = item.get('shtTravelTm')
                if min_sht_path_time == int(item.get('shtTravelTm')):
                    break

            sht_path_list = sht_path_list.replace(" ", "")
            sht_path_list = sht_path_list.split(',')

            print(sht_path_list)

            # 최소 환승 경로 찾기
            min_path_time = [9999, 9999, 9999, 9999,
                             9999, 9999, 9999, 9999, 9999, 9999]
            min_trans_cnt = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
            i = 0
            try:
                for item in path_obj:
                    if int(item.get('minTravelTm')) < 500:  # 쓰래기값 제거하기
                        min_path_time[i] = int(item.get('minTravelTm'))
                        min_trans_cnt[i] = int(item.get('minTransferCnt'))
                    i = i+1
            except AttributeError:
                print('AttributeError')

            min_trans = 999
            # min_min_trans_cnt = min(min_trans_cnt) # 환승 횟수의 최솟값을 변수에 저장
            min_min_path_time = min(min_path_time)  # 시간의 최솟값을 변수에 저장
            for item in path_obj:

                if int(item.get('minTransferCnt')) < min_trans:  # 환승 횟수가 최소면,
                    t = int(item.get('minTravelTm'))
                    min_trans = int(item.get('minTransferCnt'))

                    min_path_list = item.get('minStatnNm')
                    min_path_msg = item.get('minTravelMsg')
                    min_path_trans_cnt = item.get('minTransferCnt')

                elif int(item.get('minTransferCnt')) == min_trans:
                    if int(item.get('minTravelTm')) < t:
                        min_path_list = item.get('minStatnNm')
                        min_path_msg = item.get('minTravelMsg')
                        min_path_trans_cnt = item.get('minTransferCnt')

            min_path_list = min_path_list.replace(" ", "")

            min_path_list = min_path_list.split(',')

            # shtTransferCnt <-- 환승 횟수 카운터
            # minTransferCnt

            # 서울시 지하철역 정보 검색 (역명) https://data.seoul.go.kr/dataList/OA-121/S/1/datasetView.do
            # 출발역 찾기
            if searchword == '서울':
                searchword = '서울역'
            api_url1 = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                '/json/SearchInfoBySubwayNameService/1/5/'+searchword
            response = requests.get(api_url1)
            resdata = response.text
            obj = json.loads(resdata)
            try:
                obj = obj['SearchInfoBySubwayNameService']
                obj = obj['row']
            except KeyError:
                print("keyerror")

            if sht_path_list[1] == '서울':
                sht_path_list[1] = '서울역'
            # 출발역 다음역 찾기 (호선 찾기 위함) (최단시간)
            sht_next_api_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                '/json/SearchInfoBySubwayNameService/1/5/'+sht_path_list[1]
            sht_next_response = requests.get(sht_next_api_url)
            sht_next_resdata = sht_next_response.text
            sht_next_obj = json.loads(sht_next_resdata)
            try:
                sht_next_obj = sht_next_obj['SearchInfoBySubwayNameService']
                sht_next_obj = sht_next_obj['row']
            except KeyError:
                print("keyerror")

            # 출발역 다음역 찾기 (호선 찾기 위함) (최소환승)
            if min_path_list[1] == '서울':
                min_path_list[1] = '서울역'
            min_next_api_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                '/json/SearchInfoBySubwayNameService/1/5/'+min_path_list[1]
            min_next_response = requests.get(min_next_api_url)
            min_next_resdata = min_next_response.text
            min_next_obj = json.loads(min_next_resdata)
            try:
                min_next_obj = min_next_obj['SearchInfoBySubwayNameService']
                min_next_obj = min_next_obj['row']
            except KeyError:
                print("keyerror")

            # 도착역 찾기
            if destword == '서울':
                destword = '서울역'
            dest_api_url1 = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                '/json/SearchInfoBySubwayNameService/1/5/'+destword
            dest_response = requests.get(dest_api_url1)
            dest_resdata = dest_response.text
            dest_obj = json.loads(dest_resdata)
            try:
                dest_obj = dest_obj['SearchInfoBySubwayNameService']
                dest_obj = dest_obj['row']
            except KeyError:
                print("keyerror")

            # 출발 지점 호선 찾기
            line_list = []
            for item in obj:
                line_list += item.get('LINE_NUM')
                line_list += ','
            joined_line_list = " ".join(line_list)
            joined_line_list = joined_line_list.replace(" ", "")
            joined_line_list = joined_line_list.split(',')
            joined_line_list = [v for v in joined_line_list if v]

            # 출발 다음 지점 호선 찾기 (최단시간)
            next_line_list = []
            for item in sht_next_obj:
                next_line_list += item.get('LINE_NUM')
                next_line_list += ','
            joined_next_line_list = " ".join(next_line_list)
            joined_next_line_list = joined_next_line_list.replace(" ", "")
            joined_next_line_list = joined_next_line_list.split(',')
            joined_next_line_list = [v for v in joined_next_line_list if v]

            # 출발 다음 지점 호선 찾기 (최소환승)
            min_next_line_list = []
            for item in min_next_obj:
                min_next_line_list += item.get('LINE_NUM')
                min_next_line_list += ','
            min_joined_next_line_list = " ".join(min_next_line_list)
            min_joined_next_line_list = min_joined_next_line_list.replace(
                " ", "")
            min_joined_next_line_list = min_joined_next_line_list.split(',')
            min_joined_next_line_list = [
                v for v in min_joined_next_line_list if v]

            # 노선 찾기
            sht_line = ''
            for item in joined_line_list:
                for jtem in joined_next_line_list:
                    if item == jtem:
                        sht_line = jtem
                        break
            print(sht_line)
            min_line = ''
            for item in joined_line_list:
                for jtem in min_joined_next_line_list:
                    if item == jtem:
                        min_line = jtem
                        break
            print(min_line)

            '''
            if sht_line = '01호선':
                min_code = 
            elif sht_line ='02호선':
            
            elif sht_line = '03호선':
            
            elif sht_line = '04호선':
            
            elif sht_line = '05호선':
            
            elif sht_line = '06호선':
            
            elif sht_line = '07호선':
            
            elif sht_line = '08호선':
            
            elif sht_line = '09호선':
            
            elif sht_line = '경의선':
            
            elif sht_line = '수인분당선':
            
            elif sht_line = '경춘선'
'''

            # 출발 호선 기준으로 호선 내 지하철 역 찾기 (최단시간)
            # 서울교통공사 노선별 지하철역 정보  http://data.seoul.go.kr/dataList/OA-15442/S/1/datasetView.do

            line_api_url = 'http://openapi.seoul.go.kr:8088/'+key_num + \
                '/json/SearchSTNBySubwayLineInfo/1/200/ / /'+sht_line
            line_response = requests.get(line_api_url)
            line_resdata = line_response.text
            line_obj = json.loads(line_resdata)

            line_obj = line_obj['SearchSTNBySubwayLineInfo']
            line_obj = line_obj['row']
            station_list = []
            for item in line_obj:
                station_list += item.get('STATION_NM')
                station_list += ','
            joined_station_list = " ".join(station_list)
            joined_station_list = joined_station_list.replace(" ", "")
            joined_station_list = joined_station_list.split(',')
            joined_station_list = [v for v in joined_station_list if v]

            if sht_line == '1' or sht_line == '01호선':
                temp_index = 0
                temp_index = joined_station_list.index('서울역')
                joined_station_list[temp_index] = '서울'

            # 출발 호선 기준으로 호선 내 지하철 역 찾기 (최소환승)
            # 서울교통공사 노선별 지하철역 정보  http://data.seoul.go.kr/dataList/OA-15442/S/1/datasetView.do

            min_line_api_url = 'http://openapi.seoul.go.kr:8088/'+key_num + \
                '/json/SearchSTNBySubwayLineInfo/1/200/ / /'+min_line
            min_line_response = requests.get(min_line_api_url)
            min_line_resdata = min_line_response.text
            min_line_obj = json.loads(min_line_resdata)

            min_line_obj = min_line_obj['SearchSTNBySubwayLineInfo']
            min_line_obj = min_line_obj['row']
            min_station_list = []
            min_station_code_list = []
            for item in min_line_obj:
                min_station_list += item.get('STATION_NM')
                min_station_list += ','
                min_station_code_list += item.get('STATION_CD')
                min_station_code_list += ','
            min_joined_station_list = " ".join(min_station_list)
            min_joined_station_list = min_joined_station_list.replace(" ", "")
            min_joined_station_list = min_joined_station_list.split(',')
            min_joined_station_list = [v for v in min_joined_station_list if v]

            min_joined_station_code_list = " ".join(min_station_code_list)
            min_joined_station_code_list = min_joined_station_code_list.replace(
                " ", "")
            min_joined_station_code_list = min_joined_station_code_list.split(
                ',')
            min_joined_station_code_list = [
                v for v in min_joined_station_code_list if v]

            print(min_joined_station_list)
            print(min_joined_station_code_list)

            if min_line == '1' or min_line == '01호선':
                temp_index = 0
                temp_index = min_joined_station_list.index('서울역')
                min_joined_station_list[temp_index] = '서울'

            if answer == 'sht_path':
                print('sht')

                # 최단 시간 경로 역코드 딕셔너리 만들기 0회 환승 시!

                sht_path_code_url = 'http://openAPI.seoul.go.kr:8088/' + \
                    key_num+'/json/SearchInfoBySubwayNameService/1/800/'
                sht_path_code_response = requests.get(sht_path_code_url)
                sht_path_code_resdata = sht_path_code_response.text
                sht_path_code_obj = json.loads(sht_path_code_resdata)
                sht_path_code_obj = sht_path_code_obj['SearchInfoBySubwayNameService']
                sht_path_code_obj = sht_path_code_obj['row']

                sht_station_code_list = []
                for item in sht_path_list:
                    for jtem in sht_path_code_obj:

                        if jtem.get('STATION_NM') == item:
                            if sht_line == jtem.get('LINE_NUM'):
                                sht_station_code_list += jtem.get('STATION_CD')
                                sht_station_code_list += ','
                sht_joined_station_code_list = " ".join(sht_station_code_list)
                sht_joined_station_code_list = sht_joined_station_code_list.replace(
                    " ", "")
                sht_joined_station_code_list = sht_joined_station_code_list.split(
                    ',')
                sht_joined_station_code_list = [
                    v for v in sht_joined_station_code_list if v]

                print('환승 0 회 최단 시간')
                print(sht_path_list)
                print(sht_joined_station_code_list)

                #############################

                sht_start_code = sht_joined_station_code_list[0]
                sht_next_code = sht_joined_station_code_list[1]

                print(sht_start_code)
                # 최단시간 상행 하행 여부
                if sht_line == '03호선' or sht_line == '04호선' or sht_line == '07호선' or sht_line == '08호선' or sht_line == '05호선':
                    if int(sht_start_code) - int(sht_next_code) > 0:
                        up_down_tag = '1'
                    else:
                        up_down_tag = '2'
                elif sht_line == '01호선' or sht_line == '02호선' or sht_line == '06호선' or sht_line == '09호선':
                    if int(sht_start_code) - int(sht_next_code) > 0:
                        up_down_tag = '2'
                    else:
                        up_down_tag = '1'

                #########################################
                print(week_tag)
                print(up_down_tag)

                # 서울시 역코드로 지하철역별 열차 시간표 정보 검색 https://data.seoul.go.kr/dataList/OA-101/A/1/datasetView.do
                time_table_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                    '/json/SearchSTNTimeTableByIDService/1/300/' + \
                    sht_start_code+'/'+week_tag+'/'+up_down_tag
                time_table_response = requests.get((time_table_url))
                time_table_resdata = time_table_response.text
                time_table_obj = json.loads(time_table_resdata)
                time_table_obj = time_table_obj['SearchSTNTimeTableByIDService']
                time_table_obj = time_table_obj['row']

                print('시간표시간표시간표')
                break_index = 0
                time_table_list = []
                train_num_list = []
                last_time = []
                for item in time_table_obj:

                    if str_time > item.get('ARRIVETIME'):
                        last_time = item.get('ARRIVETIME')

                    elif str_time <= item.get('ARRIVETIME'):
                        time_table_list += item.get('ARRIVETIME')
                        time_table_list += ','
                        train_num_list += item.get('TRAIN_NO')
                        train_num_list += ','

                        break_index += 1
                        if break_index == 3:
                            break

                sht_joined_time_table_list = " ".join(time_table_list)
                sht_joined_time_table_list = sht_joined_time_table_list.replace(
                    " ", "")
                sht_joined_time_table_list = sht_joined_time_table_list.split(
                    ',')
                sht_joined_time_table_list = [
                    v for v in sht_joined_time_table_list if v]

                print(last_time)
                print(sht_joined_time_table_list)

                sht_joined_train_num_list = " ".join(train_num_list)
                sht_joined_train_num_list = sht_joined_train_num_list.replace(
                    " ", "")
                sht_joined_train_num_list = sht_joined_train_num_list.split(
                    ',')
                sht_joined_train_num_list = [
                    v for v in sht_joined_train_num_list if v]

                print(sht_joined_train_num_list)

                # 실시간 지하철 실시간 열차위치정보 http://data.seoul.go.kr/dataList/OA-12601/A/1/datasetView.do

                # 호선 명 처리
                if sht_line == '01호선':
                    temp_line = '1호선'
                elif sht_line == '02호선':
                    temp_line = '2호선'
                elif sht_line == '03호선':
                    temp_line = '3호선'
                elif sht_line == '04호선':
                    temp_line = '4호선'
                elif sht_line == '05호선':
                    temp_line = '5호선'
                elif sht_line == '06호선':
                    temp_line = '6호선'
                elif sht_line == '07호선':
                    temp_line = '7호선'
                elif sht_line == '08호선':
                    temp_line = '8호선'
                elif sht_line == '09호선':
                    temp_line = '9호선'

# return render(request,'sht_path.html',{'real_time_position':real_time_position,'sht_joined_time_table_list':sht_joined_time_table_list,'trans_line3':trans_line3,'joined_path_station_list3':joined_path_station_list3,'after_trans_path_list3':after_trans_path_list3,'sht_path_trans_cnt':sht_path_trans_cnt,'joined_path_station_list2':joined_path_station_list2,'trans_line2':trans_line2,'trans_station2':trans_station2,'after_trans_path_list2':after_trans_path_list2,'trans_line':trans_line,'after_trans_path_list':after_trans_path_list,'joined_path_station_list':joined_path_station_list,'line_obj':line_obj,'sht_line':sht_line,'obj' : obj,'sht_path_msg':sht_path_msg,'path_time':path_time,'sht_path_list':sht_path_list,'path_obj':path_obj,'dest_obj':dest_obj })

                # schedule.every(10).seconds.do(RealTimeFunc)

                # while 1:
                #    schedule.run_pending()
                #    time.sleep(1)
                #    if real_time_position == destword:
                #        break

                # schedule.every(30).seconds.do(redirect('sht_path'))
                # ------------------------------------@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                # 아래 코드 실행  (환승을 한다면,) 최단 시간

                if sht_path_trans_cnt == '1' or sht_path_trans_cnt == '2' or sht_path_trans_cnt == '3':

                    print('\n\n최단 시간 경로 - 환승을 하는 경로입니다.')

                    # 최소 시간 경로 환승경로 지정하기
                    # sht_path_list
                    path_station_list = []
                    for item in sht_path_list:
                        for jtem in joined_station_list:
                            if item == jtem:
                                path_station_list += jtem
                                path_station_list += ','
                                break

                    joined_path_station_list = " ".join(path_station_list)
                    joined_path_station_list = joined_path_station_list.replace(
                        " ", "")
                    joined_path_station_list = joined_path_station_list.split(
                        ',')
                    # trans_station <--- 환승역임
                    trans_station = joined_path_station_list[-2]

                    index = sht_path_list.index(trans_station)

                    # 환승역 다음 역
                    next_trans_station = sht_path_list[index+1]

                    # 환승역 기준 다시 도착역 까지 경로
                    # 1회 환승 이후 노선 찾기

                    # 서울 입력시 서울 -> 서울역 변경
                    if trans_station == '서울':
                        trans_station = '서울역'
                    # 환승역 노선 찾기

                    trans_api_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                        '/json/SearchInfoBySubwayNameService/1/5/'+trans_station
                    trans_response = requests.get(trans_api_url)
                    trans_resdata = trans_response.text
                    trans_obj = json.loads(trans_resdata)
                    try:
                        trans_obj = trans_obj['SearchInfoBySubwayNameService']
                        trans_obj = trans_obj['row']
                    except KeyError:
                        print("keyerror")

                    trans_line_list = []
                    for item in trans_obj:
                        trans_line_list += item.get('LINE_NUM')
                        trans_line_list += ','

                    joined_trans_line_list = " ".join(trans_line_list)
                    joined_trans_line_list = joined_trans_line_list.replace(
                        " ", "")
                    joined_trans_line_list = joined_trans_line_list.split(',')
                    joined_trans_line_list = [
                        v for v in joined_trans_line_list if v]

                    print('\n\n\nSEOUL')
                    print(joined_trans_line_list)

                    if next_trans_station == '서울':
                        next_trans_station = '서울역'

                    print(next_trans_station)
                    # 환승역 다음역 노선 찾기
                    next_trans_api_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                        '/json/SearchInfoBySubwayNameService/1/5/'+next_trans_station
                    next_trans_response = requests.get(next_trans_api_url)
                    next_trans_resdata = next_trans_response.text
                    next_trans_obj = json.loads(next_trans_resdata)
                    try:
                        next_trans_obj = next_trans_obj['SearchInfoBySubwayNameService']
                        next_trans_obj = next_trans_obj['row']
                    except KeyError:
                        print("keyerror")

                    next_trans_line_list = []
                    for item in next_trans_obj:
                        next_trans_line_list += item.get('LINE_NUM')
                        next_trans_line_list += ','
                    next_joined_trans_line_list = " ".join(
                        next_trans_line_list)
                    next_joined_trans_line_list = next_joined_trans_line_list.replace(
                        " ", "")
                    next_joined_trans_line_list = next_joined_trans_line_list.split(
                        ',')
                    next_joined_trans_line_list = [
                        v for v in next_joined_trans_line_list if v]

                    # 환승 이후 노선 찾기

                    for item in joined_trans_line_list:
                        for jtem in next_joined_trans_line_list:
                            if item == jtem:
                                trans_line = jtem
                                break

                    # 환승 이후 경로
                    after_trans_path_list = sht_path_list[index:-1]

                    # 최단 시간 경로 역코드 딕셔너리 만들기 1회 환승 이후!
                    sht_station_code_list = []
                    for item in after_trans_path_list:
                        for jtem in sht_path_code_obj:

                            if jtem.get('STATION_NM') == item:
                                if trans_line == jtem.get('LINE_NUM'):

                                    sht_station_code_list += jtem.get(
                                        'STATION_CD')
                                    sht_station_code_list += ','

                    sht_joined_station_code_list1 = " ".join(
                        sht_station_code_list)
                    sht_joined_station_code_list1 = sht_joined_station_code_list1.replace(
                        " ", "")
                    sht_joined_station_code_list1 = sht_joined_station_code_list1.split(
                        ',')
                    sht_joined_station_code_list1 = [
                        v for v in sht_joined_station_code_list1 if v]

                    trans_station_code = sht_joined_station_code_list1[0]
                    trans_next_station_code = sht_joined_station_code_list1[1]

                    print('환승 1 회 이후 최단 시간')
                    print(after_trans_path_list)
                    print(sht_joined_station_code_list1)

                    # 실시간 열차 출발시간 정보(환승1회시 환승역 출발시간)
                    if trans_line == '03호선' or trans_line == '04호선' or trans_line == '05호선' or trans_line == '07호선' or trans_line == '08호선':
                        if int(trans_station_code) - int(trans_next_station_code) > 0:
                            sht_up_down_tag = '1'
                        else:
                            sht_up_down_tag = '2'
                    elif trans_line == '01호선' or trans_line == '02호선' or trans_line == '06호선' or trans_line == '09호선':
                        if int(trans_station_code) - int(trans_next_station_code) > 0:
                            sht_up_down_tag = '2'
                        else:
                            sht_up_down_tag = '1'

                    time_table_trans_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                        '/json/SearchSTNTimeTableByIDService/1/300/' + \
                        trans_station_code+'/'+week_tag+'/'+sht_up_down_tag
                    time_table_trans_response = requests.get(
                        (time_table_trans_url))
                    time_table_trans_resdata = time_table_trans_response.text
                    time_table_trans_obj = json.loads(time_table_trans_resdata)
                    time_table_trans_obj = time_table_trans_obj['SearchSTNTimeTableByIDService']
                    time_table_trans_obj = time_table_trans_obj['row']

                    trans_path_api_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
                        path_key+'/json/shortestRoute/0/10/'+searchword+'/'+trans_station
                    trans_path_response = requests.get(trans_path_api_url)
                    trans_path_resdata = trans_path_response.text
                    trans_path_obj = json.loads(trans_path_resdata)
                    try:
                        trans_path_obj = trans_path_obj['shortestRouteList']
                    except KeyError:
                        print("keyerror")

                    for item in trans_path_obj:
                        trans_path_time = item.get('shtTravelTm')

                    print(trans_path_time)

                    trans_first_time1 = sht_joined_time_table_list[0]

                    trans_first_time1_min = int(
                        trans_first_time1[3:5]) + int(trans_path_time[0:])
                    if trans_first_time1_min < 60:
                        trans_first_time1_min = int(
                            trans_first_time1[3:5]) + int(trans_path_time[0:])
                        trans_arrival_time1 = trans_first_time1[:2] + ':' + \
                            str(trans_first_time1_min) + \
                            ':' + trans_first_time1[6:]
                    if trans_first_time1_min >= 60:
                        trans_first_time1_min = int(
                            trans_first_time1[3:5]) + int(trans_path_time[0:]) - 60
                        trans_first_time1_hour = int(trans_first_time1[:2]) + 1
                        if int(trans_first_time1_min) < 10:
                            trans_arrival_time1 = str(
                                trans_first_time1_hour) + ':0' + str(trans_first_time1_min) + ':' + trans_first_time1[6:]
                        else:
                            trans_arrival_time1 = str(trans_first_time1_hour) + ':' + \
                                str(trans_first_time1_min) + \
                                ':' + trans_first_time1[6:]

                    print(trans_arrival_time1)

                    print('환승역(1) 시간표')
                    break_index1 = 0
                    time_table_list1 = []
                    train_num_list1 = []
                    last_time1 = []
                    for item in time_table_trans_obj:

                        if trans_arrival_time1 > item.get('ARRIVETIME'):
                            last_time1 = item.get('ARRIVETIME')

                        elif trans_arrival_time1 < item.get('ARRIVETIME'):
                            time_table_list1 += item.get('ARRIVETIME')
                            time_table_list1 += ','
                            train_num_list1 += item.get('TRAIN_NO')
                            train_num_list1 += ','

                            break_index1 += 1
                            if break_index1 == 3:
                                break

                    sht_joined_time_table_list1 = " ".join(time_table_list1)
                    sht_joined_time_table_list1 = sht_joined_time_table_list1.replace(
                        " ", "")
                    sht_joined_time_table_list1 = sht_joined_time_table_list1.split(
                        ',')
                    sht_joined_time_table_list1 = [
                        v for v in sht_joined_time_table_list1 if v]

                    print(last_time1)
                    print(sht_joined_time_table_list1)

                    sht_joined_train_num_list1 = " ".join(train_num_list1)
                    sht_joined_train_num_list1 = sht_joined_train_num_list1.replace(
                        " ", "")
                    sht_joined_train_num_list1 = sht_joined_train_num_list1.split(
                        ',')
                    sht_joined_train_num_list1 = [
                        v for v in sht_joined_train_num_list1 if v]

                    print(sht_joined_train_num_list1)

                    # --------------------------------------------------------

                    if sht_path_trans_cnt == '2' or sht_path_trans_cnt == '3':
                        print('환승 횟수가 2회 이상입니다.')
                        # 환승 횟수 2회일 때의 코드 작성
                        # trans_station << 환승역이 출발역으로,
                        # after_trans_path_list << 환승 이후의 경로가 경로로 사용
                        # trans_line << 환승 이후 노선을 노선으로 사용
                        # 환승 호선 기준으로 호선 내 지하철 역 찾기 (최단시간)
                        # 서울교통공사 노선별 지하철역 정보  http://data.seoul.go.kr/dataList/OA-15442/S/1/datasetView.do

                        trans_line_api_url = 'http://openapi.seoul.go.kr:8088/'+key_num + \
                            '/json/SearchSTNBySubwayLineInfo/1/200/ / /'+trans_line
                        trans_line_response = requests.get(trans_line_api_url)
                        trans_line_resdata = trans_line_response.text
                        trans_line_obj = json.loads(trans_line_resdata)

                        trans_line_obj = trans_line_obj['SearchSTNBySubwayLineInfo']
                        trans_line_obj = trans_line_obj['row']
                        trans_station_list = []
                        for item in trans_line_obj:
                            trans_station_list += item.get('STATION_NM')
                            trans_station_list += ','
                        joined_trans_station_list = " ".join(
                            trans_station_list)
                        joined_trans_station_list = joined_trans_station_list.replace(
                            " ", "")
                        joined_trans_station_list = joined_trans_station_list.split(
                            ',')
                        joined_trans_station_list = [
                            v for v in joined_trans_station_list if v]

                        temp_index = 0
                        print(trans_line)
                        if trans_line == '1' or trans_line == '01호선':
                            temp_index = 0
                            temp_index = joined_trans_station_list.index('서울역')
                            joined_trans_station_list[temp_index] = '서울'
                            print(temp_index)

                        # 최소 시간 경로 환승경로 지정하기

                        trans_path_station_list = []
                        for item in after_trans_path_list:
                            for jtem in joined_trans_station_list:
                                if item == jtem:
                                    trans_path_station_list += jtem
                                    trans_path_station_list += ','
                                    break

                        joined_path_station_list2 = " ".join(
                            trans_path_station_list)
                        joined_path_station_list2 = joined_path_station_list2.replace(
                            " ", "")
                        joined_path_station_list2 = joined_path_station_list2.split(
                            ',')

                        # trans_station <--- 환승역임
                        trans_station2 = joined_path_station_list2[-2]

                        index2 = after_trans_path_list.index(trans_station2)

                        # 환승역 다음 역
                        next_trans_station2 = after_trans_path_list[index2+1]
                        # 환승역 기준 다시 도착역 까지 경로
                        # 1회 환승 이후 노선 찾기

                        if trans_station2 == '서울':
                            trans_station2 = '서울역'
                        # 환승역 노선 찾기
                        trans_api_url2 = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                            '/json/SearchInfoBySubwayNameService/1/5/'+trans_station2
                        trans_response2 = requests.get(trans_api_url2)
                        trans_resdata2 = trans_response2.text
                        trans_obj2 = json.loads(trans_resdata2)
                        try:
                            trans_obj2 = trans_obj2['SearchInfoBySubwayNameService']
                            trans_obj2 = trans_obj2['row']
                        except KeyError:
                            print("keyerror")

                        trans_line_list2 = []
                        for item in trans_obj2:
                            trans_line_list2 += item.get('LINE_NUM')
                            trans_line_list2 += ','
                        joined_trans_line_list2 = " ".join(trans_line_list2)
                        joined_trans_line_list2 = joined_trans_line_list2.replace(
                            " ", "")
                        joined_trans_line_list2 = joined_trans_line_list2.split(
                            ',')
                        joined_trans_line_list2 = [
                            v for v in joined_trans_line_list2 if v]

                        if next_trans_station2 == '서울':
                            next_trans_station2 = '서울역'

                        # 환승역 다음역 노선 찾기
                        next_trans_api_url2 = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                            '/json/SearchInfoBySubwayNameService/1/5/'+next_trans_station2
                        next_trans_response2 = requests.get(
                            next_trans_api_url2)
                        next_trans_resdata2 = next_trans_response2.text
                        next_trans_obj2 = json.loads(next_trans_resdata2)
                        try:
                            next_trans_obj2 = next_trans_obj2['SearchInfoBySubwayNameService']
                            next_trans_obj2 = next_trans_obj2['row']
                        except KeyError:
                            print("keyerror")

                        next_trans_line_list2 = []
                        for item in next_trans_obj2:
                            next_trans_line_list2 += item.get('LINE_NUM')
                            next_trans_line_list2 += ','
                        next_joined_trans_line_list2 = " ".join(
                            next_trans_line_list2)
                        next_joined_trans_line_list2 = next_joined_trans_line_list2.replace(
                            " ", "")
                        next_joined_trans_line_list2 = next_joined_trans_line_list2.split(
                            ',')
                        next_joined_trans_line_list2 = [
                            v for v in next_joined_trans_line_list2 if v]

                        # 환승 이후 노선 찾기

                        for item in joined_trans_line_list2:
                            for jtem in next_joined_trans_line_list2:
                                if item == jtem:
                                    trans_line2 = jtem
                                    break

                        # 환승 이후 경로
                        after_trans_path_list2 = after_trans_path_list[index2:]

                        # 최단 시간 경로 역코드 딕셔너리 만들기 2회 환승 이후!
                        sht_station_code_list = []
                        for item in after_trans_path_list2:
                            for jtem in sht_path_code_obj:

                                if jtem.get('STATION_NM') == item:
                                    if trans_line2 == jtem.get('LINE_NUM'):
                                        sht_station_code_list += jtem.get(
                                            'STATION_CD')
                                        sht_station_code_list += ','

                        sht_joined_station_code_list2 = " ".join(
                            sht_station_code_list)
                        sht_joined_station_code_list2 = sht_joined_station_code_list2.replace(
                            " ", "")
                        sht_joined_station_code_list2 = sht_joined_station_code_list2.split(
                            ',')
                        sht_joined_station_code_list2 = [
                            v for v in sht_joined_station_code_list2 if v]
                        print('환승 2 회 이후 최단 시간')
                        print(after_trans_path_list2)
                        print(sht_joined_station_code_list2)

                        trans_station_code2 = sht_joined_station_code_list2[0]
                        trans_next_station_code2 = sht_joined_station_code_list2[1]

                        # 실시간 열차 출발 정보(환승2회시 환승역 출발시간)
                        if trans_line2 == '03호선' or trans_line2 == '04호선' or trans_line2 == '05호선' or trans_line2 == '07호선' or trans_line2 == '08호선' or trans_line2 == '수인분당선' or trans_line2 == '신분당선' or trans_line2 == '공항철도':
                            if int(trans_station_code2) - int(trans_next_station_code2) > 0:
                                sht_up_down_tag2 = '1'
                            else:
                                sht_up_down_tag2 = '2'
                        elif trans_line2 == '01호선' or trans_line2 == '02호선' or trans_line2 == '06호선' or trans_line2 == '09호선':
                            if int(trans_station_code2) - int(trans_next_station_code2) > 0:
                                sht_up_down_tag2 = '2'
                            else:
                                sht_up_down_tag2 = '1'

                        time_table_trans2_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                            '/json/SearchSTNTimeTableByIDService/1/300/' + \
                            trans_station_code2+'/'+week_tag+'/'+sht_up_down_tag2
                        time_table_trans2_response = requests.get(
                            (time_table_trans2_url))
                        time_table_trans2_resdata = time_table_trans2_response.text
                        time_table_trans2_obj = json.loads(
                            time_table_trans2_resdata)
                        time_table_trans2_obj = time_table_trans2_obj['SearchSTNTimeTableByIDService']
                        time_table_trans2_obj = time_table_trans2_obj['row']

                        trans_path2_api_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
                            path_key+'/json/shortestRoute/0/5/'+trans_station+'/'+trans_station2
                        trans_path2_response = requests.get(
                            trans_path2_api_url)
                        trans_path2_resdata = trans_path2_response.text
                        trans_path2_obj = json.loads(trans_path2_resdata)
                        try:
                            trans_path2_obj = trans_path2_obj['shortestRouteList']
                        except KeyError:
                            print("keyerror")

                        for item in trans_path2_obj:
                            trans_path2_time = item.get('shtTravelTm')

                        print(trans_path2_time)

                        trans_first_time2 = sht_joined_time_table_list1[0]

                        trans_first_time2_min = int(
                            trans_first_time2[3:5]) + int(trans_path2_time[0:])
                        if trans_first_time2_min < 60:
                            trans_first_time2_min = int(
                                trans_first_time2[3:5]) + int(trans_path2_time[0:])
                            trans_arrival_time2 = trans_first_time2[:2] + ':' + \
                                str(trans_first_time2_min) + \
                                ':' + trans_first_time2[6:]
                        if trans_first_time2_min >= 60:
                            trans_first_time2_min = int(
                                trans_first_time2[3:5]) + int(trans_path2_time[0:]) - 60
                            trans_first_time2_hour = int(
                                trans_first_time2[:2]) + 1
                            if int(trans_first_time2_min) < 10:
                                trans_arrival_time2 = str(
                                    trans_first_time2_hour) + ':0' + str(trans_first_time2_min) + ':' + trans_first_time2[6:]
                            else:
                                trans_arrival_time2 = str(trans_first_time2_hour) + ':' + \
                                    str(trans_first_time2_min) + \
                                    ':' + trans_first_time2[6:]

                        print(trans_arrival_time2)

                        print('환승역(2) 시간표')
                        break_index2 = 0
                        time_table_list2 = []
                        train_num_list2 = []
                        last_time2 = []
                        for item in time_table_trans2_obj:

                            if trans_arrival_time2 > item.get('ARRIVETIME'):
                                last_time2 = item.get('ARRIVETIME')

                            elif trans_arrival_time2 < item.get('ARRIVETIME'):
                                time_table_list2 += item.get('ARRIVETIME')
                                time_table_list2 += ','
                                train_num_list2 += item.get('TRAIN_NO')
                                train_num_list2 += ','

                                break_index2 += 1
                                if break_index2 == 3:
                                    break

                        sht_joined_time_table_list2 = " ".join(
                            time_table_list2)
                        sht_joined_time_table_list2 = sht_joined_time_table_list2.replace(
                            " ", "")
                        sht_joined_time_table_list2 = sht_joined_time_table_list2.split(
                            ',')
                        sht_joined_time_table_list2 = [
                            v for v in sht_joined_time_table_list2 if v]

                        print(last_time2)
                        print(sht_joined_time_table_list2)

                        sht_joined_train_num_list2 = " ".join(train_num_list2)
                        sht_joined_train_num_list2 = sht_joined_train_num_list2.replace(
                            " ", "")
                        sht_joined_train_num_list2 = sht_joined_train_num_list2.split(
                            ',')
                        sht_joined_train_num_list2 = [
                            v for v in sht_joined_train_num_list2 if v]

                        print(sht_joined_train_num_list2)

                        if sht_path_trans_cnt == '3':
                            print('환승 횟수가 3회 입니다.')
                            # 환승 횟수 3회 일 때의 코드 작성

                            '''
                            trans_line2 : 2회 환승 한 이후 지하철의 호선(최단시간)
                            trans_station2 : 2회 환승 한 지하철역(최단시간)
                            joined_path_station_list2 : 1회 환승 역에서 2회 환승 전 까지의 경로(최단시간)
                            after_trans_path_list2 : 2회 환승 이후 지하철 경로(최단시간)
                            '''
                            # 환승 호선 기준으로 호선 내 지하철 역 찾기 (최단시간)
                            # 서울교통공사 노선별 지하철역 정보  http://data.seoul.go.kr/dataList/OA-15442/S/1/datasetView.do

                            trans_line_api_url3 = 'http://openapi.seoul.go.kr:8088/'+key_num + \
                                '/json/SearchSTNBySubwayLineInfo/1/200/ / /'+trans_line2
                            trans_line_response3 = requests.get(
                                trans_line_api_url3)
                            trans_line_resdata3 = trans_line_response3.text
                            trans_line_obj3 = json.loads(trans_line_resdata3)

                            trans_line_obj3 = trans_line_obj3['SearchSTNBySubwayLineInfo']
                            trans_line_obj3 = trans_line_obj3['row']
                            trans_station_list3 = []
                            for item in trans_line_obj3:
                                trans_station_list3 += item.get('STATION_NM')
                                trans_station_list3 += ','
                            joined_trans_station_list3 = " ".join(
                                trans_station_list3)
                            joined_trans_station_list3 = joined_trans_station_list3.replace(
                                " ", "")
                            joined_trans_station_list3 = joined_trans_station_list3.split(
                                ',')
                            joined_trans_station_list3 = [
                                v for v in joined_trans_station_list3 if v]

                            if trans_line2 == '1' or trans_line2 == '01호선':
                                temp_index = joined_trans_station_list3.index(
                                    '서울역')
                                joined_trans_station_list3[temp_index] = '서울'

                            # 최소 시간 경로 환승경로 지정하기

                            trans_path_station_list3 = []
                            for item in after_trans_path_list2:
                                for jtem in joined_trans_station_list3:
                                    if item == jtem:
                                        trans_path_station_list3 += jtem
                                        trans_path_station_list3 += ','
                                        break

                            joined_path_station_list3 = " ".join(
                                trans_path_station_list3)
                            joined_path_station_list3 = joined_path_station_list3.replace(
                                " ", "")
                            joined_path_station_list3 = joined_path_station_list3.split(
                                ',')

                            # trans_station <--- 환승역임
                            trans_station3 = joined_path_station_list3[-2]

                            index3 = after_trans_path_list2.index(
                                trans_station3)

                            # 환승역 다음 역
                            next_trans_station3 = after_trans_path_list2[index3+1]
                            # 환승역 기준 다시 도착역 까지 경로
                            # 1회 환승 이후 노선 찾기
                            if trans_station3 == '서울':
                                trans_station3 = '서울역'

                            # 환승역 노선 찾기
                            trans_api_url3 = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                                '/json/SearchInfoBySubwayNameService/1/5/'+trans_station3
                            trans_response3 = requests.get(trans_api_url3)
                            trans_resdata3 = trans_response3.text
                            trans_obj3 = json.loads(trans_resdata3)
                            try:
                                trans_obj3 = trans_obj3['SearchInfoBySubwayNameService']
                                trans_obj3 = trans_obj3['row']
                            except KeyError:
                                print("keyerror")

                            trans_line_list3 = []
                            for item in trans_obj3:
                                trans_line_list3 += item.get('LINE_NUM')
                                trans_line_list3 += ','
                            joined_trans_line_list3 = " ".join(
                                trans_line_list3)
                            joined_trans_line_list3 = joined_trans_line_list3.replace(
                                " ", "")
                            joined_trans_line_list3 = joined_trans_line_list3.split(
                                ',')
                            joined_trans_line_list3 = [
                                v for v in joined_trans_line_list3 if v]

                            if next_trans_station3 == '서울':
                                next_trans_station3 = '서울역'
                            # 환승역 다음역 노선 찾기
                            next_trans_api_url3 = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                                '/json/SearchInfoBySubwayNameService/1/5/'+next_trans_station3
                            next_trans_response3 = requests.get(
                                next_trans_api_url3)
                            next_trans_resdata3 = next_trans_response3.text
                            next_trans_obj3 = json.loads(next_trans_resdata3)
                            try:
                                next_trans_obj3 = next_trans_obj3['SearchInfoBySubwayNameService']
                                next_trans_obj3 = next_trans_obj3['row']
                            except KeyError:
                                print("keyerror")

                            next_trans_line_list3 = []
                            for item in next_trans_obj3:
                                next_trans_line_list3 += item.get('LINE_NUM')
                                next_trans_line_list3 += ','
                            next_joined_trans_line_list3 = " ".join(
                                next_trans_line_list3)
                            next_joined_trans_line_list3 = next_joined_trans_line_list3.replace(
                                " ", "")
                            next_joined_trans_line_list3 = next_joined_trans_line_list3.split(
                                ',')
                            next_joined_trans_line_list3 = [
                                v for v in next_joined_trans_line_list3 if v]

                            # 환승 이후 노선 찾기

                            for item in joined_trans_line_list3:
                                for jtem in next_joined_trans_line_list3:
                                    if item == jtem:
                                        trans_line3 = jtem
                                        break

                            # 환승 이후 경로
                            after_trans_path_list3 = after_trans_path_list2[index3:]

                            # 최단 시간 경로 역코드 딕셔너리 만들기 3회 환승 이후!
                            sht_station_code_list = []
                            for item in after_trans_path_list3:
                                for jtem in sht_path_code_obj:

                                    if jtem.get('STATION_NM') == item:
                                        if trans_line3 == jtem.get('LINE_NUM'):
                                            sht_station_code_list += jtem.get(
                                                'STATION_CD')
                                            sht_station_code_list += ','

                            sht_joined_station_code_list3 = " ".join(
                                sht_station_code_list)
                            sht_joined_station_code_list3 = sht_joined_station_code_list3.replace(
                                " ", "")
                            sht_joined_station_code_list3 = sht_joined_station_code_list3.split(
                                ',')
                            sht_joined_station_code_list3 = [
                                v for v in sht_joined_station_code_list3 if v]
                            print('환승 3 회 이후 최단 시간')
                            print(after_trans_path_list3)
                            print(sht_joined_station_code_list3)

                            trans_station_code3 = sht_joined_station_code_list3[0]
                            trans_next_station_code3 = sht_joined_station_code_list3[1]

                            # 실시간 열차 도착 정보(환승3회시 환승역 열차 도착 정보)

                            if trans_line3 == '03호선' or trans_line3 == '04호선' or trans_line3 == '05호선' or trans_line3 == '07호선' or trans_line3 == '08호선' or trans_line3 == '수인분당선' or trans_line3 == '신분당선' or trans_line3 == '공항철도':
                                if int(trans_station_code3) - int(trans_next_station_code3) > 0:
                                    sht_up_down_tag3 = '1'
                                else:
                                    sht_up_down_tag3 = '2'
                            elif trans_line3 == '01호선' or trans_line3 == '02호선' or trans_line3 == '06호선' or trans_line3 == '09호선':
                                if int(trans_station_code3) - int(trans_next_station_code3) > 0:
                                    sht_up_down_tag3 = '2'
                                else:
                                    sht_up_down_tag3 = '1'

                            time_table_trans3_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                                '/json/SearchSTNTimeTableByIDService/1/300/' + \
                                trans_station_code3+'/'+week_tag+'/'+sht_up_down_tag3
                            time_table_trans3_response = requests.get(
                                (time_table_trans3_url))
                            time_table_trans3_resdata = time_table_trans3_response.text
                            time_table_trans3_obj = json.loads(
                                time_table_trans3_resdata)
                            time_table_trans3_obj = time_table_trans3_obj['SearchSTNTimeTableByIDService']
                            time_table_trans3_obj = time_table_trans3_obj['row']

                            trans_path3_api_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
                                path_key+'/json/shortestRoute/0/5/'+trans_station2+'/'+trans_station3
                            trans_path3_response = requests.get(
                                trans_path3_api_url)
                            trans_path3_resdata = trans_path3_response.text
                            trans_path3_obj = json.loads(trans_path3_resdata)
                            try:
                                trans_path3_obj = trans_path3_obj['shortestRouteList']
                            except KeyError:
                                print("keyerror")

                            for item in trans_path3_obj:
                                trans_path3_time = item.get('shtTravelTm')

                            print(trans_path3_time)

                            trans_first_time3 = sht_joined_time_table_list2[0]

                            trans_first_time3_min = int(
                                trans_first_time3[3:5]) + int(trans_path3_time[0:])
                            if trans_first_time3_min < 60:
                                trans_first_time3_min = int(
                                    trans_first_time3[3:5]) + int(trans_path3_time[0:])
                                trans_arrival_time3 = trans_first_time3[:3] + ':' + \
                                    str(trans_first_time3_min) + \
                                    ':' + trans_first_time3[6:]
                            if trans_first_time3_min >= 60:
                                trans_first_time3_min = int(
                                    trans_first_time3[3:5]) + int(trans_path3_time[0:]) - 60
                                trans_first_time3_hour = int(
                                    trans_first_time3[:2]) + 1
                                if int(trans_first_time3_min) < 10:
                                    trans_arrival_time3 = str(
                                        trans_first_time3_hour) + ':0' + str(trans_first_time3_min) + ':' + trans_first_time3[6:]
                                else:
                                    trans_arrival_time3 = str(trans_first_time3_hour) + ':' + \
                                        str(trans_first_time3_min) + \
                                        ':' + trans_first_time3[6:]

                            print(trans_arrival_time3)

                            print('환승역(3) 시간표')
                            break_index3 = 0
                            time_table_list3 = []
                            train_num_list3 = []
                            last_time3 = []
                            for item in time_table_trans3_obj:

                                if trans_arrival_time3 > item.get('ARRIVETIME'):
                                    last_time3 = item.get('ARRIVETIME')

                                elif trans_arrival_time3 < item.get('ARRIVETIME'):
                                    time_table_list3 += item.get('ARRIVETIME')
                                    time_table_list3 += ','
                                    train_num_list3 += item.get('TRAIN_NO')
                                    train_num_list3 += ','

                                    break_index3 += 1
                                    if break_index3 == 3:
                                        break

                            sht_joined_time_table_list3 = " ".join(
                                time_table_list3)
                            sht_joined_time_table_list3 = sht_joined_time_table_list3.replace(
                                " ", "")
                            sht_joined_time_table_list3 = sht_joined_time_table_list3.split(
                                ',')
                            sht_joined_time_table_list3 = [
                                v for v in sht_joined_time_table_list3 if v]

                            print(last_time3)
                            print(sht_joined_time_table_list3)

                            sht_joined_train_num_list3 = " ".join(
                                train_num_list3)
                            sht_joined_train_num_list3 = sht_joined_train_num_list3.replace(
                                " ", "")
                            sht_joined_train_num_list3 = sht_joined_train_num_list3.split(
                                ',')
                            sht_joined_train_num_list3 = [
                                v for v in sht_joined_train_num_list3 if v]

                            print(sht_joined_train_num_list3)

                        else:
                            print("환승 횟수가 0회이기 때문에, 환승 코드를 실행하지 않습니다.")

                        '''
                        #서울교통공사 실시간 지하철 위치 정보 https://data.seoul.go.kr/dataList/OA-12601/A/1/datasetView.do
                        realtime_lc_url = 'http://swopenAPI.seoul.go.kr/api/subway/'+key_num,'/json/realtimePosition/0/5/'+sht_line
                        realtime_lc_response = requests.get(realtime_lc_url)
                        realtime_lc_data = realtime_lc_response.text
                        realtime_lc_obj = json.loads(realtime_lc_data)
                        try:
                            realtime_lc_obj = realtime_lc_obj["realtimePosition"]
                        except KeyError:
                            print('keyerror_realtime')
                            '''

                ### DEBUG ###
                print('\n\n\n ### DEBUG ### \n\n\n')
                print(joined_path_station_list)
                print(sht_joined_station_code_list)
                print(joined_path_station_list2)
                print(sht_joined_station_code_list1)
                print(joined_path_station_list3)
                print(sht_joined_station_code_list2)
                print(after_trans_path_list3)
                print(sht_joined_station_code_list3)

                return render(request, 'flash.html', {'real_time_position': real_time_position, 'sht_joined_time_table_list': sht_joined_time_table_list, 'trans_line3': trans_line3, 'joined_path_station_list3': joined_path_station_list3, 'after_trans_path_list3': after_trans_path_list3, 'sht_path_trans_cnt': sht_path_trans_cnt, 'joined_path_station_list2': joined_path_station_list2, 'trans_line2': trans_line2, 'trans_station2': trans_station2, 'after_trans_path_list2': after_trans_path_list2, 'trans_line': trans_line, 'after_trans_path_list': after_trans_path_list, 'joined_path_station_list': joined_path_station_list, 'line_obj': line_obj, 'sht_line': sht_line, 'obj': obj, 'sht_path_msg': sht_path_msg, 'path_time': path_time, 'sht_path_list': sht_path_list, 'path_obj': path_obj, 'dest_obj': dest_obj})

            elif answer == 'min_path':
                print('min')

                # 최소 환승 경로 역코드 딕셔너리 만들기 0회 환승 시!

                min_path_code_url = 'http://openAPI.seoul.go.kr:8088/' + \
                    key_num+'/json/SearchInfoBySubwayNameService/1/800/'
                min_path_code_response = requests.get(min_path_code_url)
                min_path_code_resdata = min_path_code_response.text
                min_path_code_obj = json.loads(min_path_code_resdata)
                min_path_code_obj = min_path_code_obj['SearchInfoBySubwayNameService']
                min_path_code_obj = min_path_code_obj['row']

                min_station_code_list = []
                for item in min_path_list:
                    for jtem in min_path_code_obj:

                        if jtem.get('STATION_NM') == item:
                            if min_line == jtem.get('LINE_NUM'):
                                min_station_code_list += jtem.get('STATION_CD')
                                min_station_code_list += ','
                min_joined_station_code_list = " ".join(min_station_code_list)
                min_joined_station_code_list = min_joined_station_code_list.replace(
                    " ", "")
                min_joined_station_code_list = min_joined_station_code_list.split(
                    ',')
                min_joined_station_code_list = [
                    v for v in min_joined_station_code_list if v]

                print('환승 0 회 최소환승')
                print(min_joined_station_code_list)

                ##############################################################

                # 최소 환승

                #############################

                min_start_code = min_joined_station_code_list[0]
                min_next_code = min_joined_station_code_list[1]

                print(min_start_code)
                # 최단시간 상행 하행 여부
                if int(min_start_code) - int(min_next_code) > 0:
                    up_down_tag = '1'
                else:
                    up_down_tag = '2'

                #########################################
                # 서울시 역코드로 지하철역별 열차 시간표 정보 검색 https://data.seoul.go.kr/dataList/OA-101/A/1/datasetView.do
                time_table_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                    '/json/SearchSTNTimeTableByIDService/1/300/' + \
                    min_start_code+'/'+week_tag+'/'+up_down_tag
                time_table_response = requests.get((time_table_url))
                time_table_resdata = time_table_response.text
                time_table_obj = json.loads(time_table_resdata)
                time_table_obj = time_table_obj['SearchSTNTimeTableByIDService']
                time_table_obj = time_table_obj['row']

                print('시간표시간표시간표')
                break_index = 0
                time_table_list = []
                train_num_list = []
                last_time = []
                for item in time_table_obj:

                    if str_time > item.get('ARRIVETIME'):
                        last_time = item.get('ARRIVETIME')

                    elif str_time <= item.get('ARRIVETIME'):
                        time_table_list += item.get('ARRIVETIME')
                        time_table_list += ','
                        train_num_list += item.get('TRAIN_NO')
                        train_num_list += ','

                        break_index += 1
                        if break_index == 3:
                            break

                min_joined_time_table_list = " ".join(time_table_list)
                min_joined_time_table_list = min_joined_time_table_list.replace(
                    " ", "")
                min_joined_time_table_list = min_joined_time_table_list.split(
                    ',')
                min_joined_time_table_list = [
                    v for v in min_joined_time_table_list if v]

                print(min_joined_time_table_list)

                min_joined_train_num_list = " ".join(train_num_list)
                min_joined_train_num_list = min_joined_train_num_list.replace(
                    " ", "")
                min_joined_train_num_list = min_joined_train_num_list.split(
                    ',')
                min_joined_train_num_list = [
                    v for v in min_joined_train_num_list if v]

                # 실시간 지하철 실시간 열차위치정보 http://data.seoul.go.kr/dataList/OA-12601/A/1/datasetView.do

                # 호선 명 처리
                if min_line == '01호선':
                    temp_line = '1호선'
                elif min_line == '02호선':
                    temp_line = '2호선'
                elif min_line == '03호선':
                    temp_line = '3호선'
                elif min_line == '04호선':
                    temp_line = '4호선'
                elif min_line == '05호선':
                    temp_line = '5호선'
                elif min_line == '06호선':
                    temp_line = '6호선'
                elif min_line == '07호선':
                    temp_line = '7호선'
                elif min_line == '08호선':
                    temp_line = '8호선'
                elif min_line == '09호선':
                    temp_line = '9호선'

                if min_path_trans_cnt == '1' or min_path_trans_cnt == '2' or min_path_trans_cnt == '3':

                    # 최소 환승 경로 환승경로 지정하기
                    min_path_station_list = []
                    for item in min_path_list:
                        for jtem in min_joined_station_list:
                            if item == jtem:
                                min_path_station_list += jtem
                                min_path_station_list += ','
                                break

                    min_joined_path_station_list = " ".join(
                        min_path_station_list)
                    min_joined_path_station_list = min_joined_path_station_list.replace(
                        " ", "")
                    min_joined_path_station_list = min_joined_path_station_list.split(
                        ',')

                    # trans_station <--- 환승역임
                    min_trans_station = min_joined_path_station_list[-2]

                    index = min_path_list.index(min_trans_station)

                    # 환승역 다음 역
                    next_trans_station = min_path_list[index+1]

                    # 환승역 기준 다시 도착역 까지 경로
                    # 1회 환승 이후 노선 찾기
                    if min_trans_station == '서울':
                        min_trans_station = '서울역'
                    # 환승역 노선 찾기
                    trans_api_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                        '/json/SearchInfoBySubwayNameService/1/5/'+min_trans_station
                    trans_response = requests.get(trans_api_url)
                    trans_resdata = trans_response.text
                    trans_obj = json.loads(trans_resdata)
                    try:
                        trans_obj = trans_obj['SearchInfoBySubwayNameService']
                        trans_obj = trans_obj['row']
                    except KeyError:
                        print("keyerror")

                    trans_line_list = []
                    for item in trans_obj:
                        trans_line_list += item.get('LINE_NUM')
                        trans_line_list += ','
                    joined_trans_line_list = " ".join(trans_line_list)
                    joined_trans_line_list = joined_trans_line_list.replace(
                        " ", "")
                    joined_trans_line_list = joined_trans_line_list.split(',')
                    joined_trans_line_list = [
                        v for v in joined_trans_line_list if v]

                    if next_trans_station == '서울':
                        next_trans_station = '서울역'
                    # 환승역 다음역 노선 찾기
                    next_trans_api_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                        '/json/SearchInfoBySubwayNameService/1/5/'+next_trans_station
                    next_trans_response = requests.get(next_trans_api_url)
                    next_trans_resdata = next_trans_response.text
                    next_trans_obj = json.loads(next_trans_resdata)
                    try:
                        next_trans_obj = next_trans_obj['SearchInfoBySubwayNameService']
                        next_trans_obj = next_trans_obj['row']
                    except KeyError:
                        print("keyerror")

                    next_trans_line_list = []
                    for item in next_trans_obj:
                        next_trans_line_list += item.get('LINE_NUM')
                        next_trans_line_list += ','
                    next_joined_trans_line_list = " ".join(
                        next_trans_line_list)
                    next_joined_trans_line_list = next_joined_trans_line_list.replace(
                        " ", "")
                    next_joined_trans_line_list = next_joined_trans_line_list.split(
                        ',')
                    next_joined_trans_line_list = [
                        v for v in next_joined_trans_line_list if v]

                    # 환승 이후 노선 찾기

                    for item in joined_trans_line_list:
                        for jtem in next_joined_trans_line_list:
                            if item == jtem:
                                min_trans_line = jtem
                                break

                    # 환승 이후 경로
                    min_after_trans_path_list = min_path_list[index:-1]

                    # 최소 환승 경로 역코드 딕셔너리 만들기 1회 환승 이후!
                    min_station_code_list = []
                    for item in min_after_trans_path_list:
                        for jtem in min_path_code_obj:

                            if jtem.get('STATION_NM') == item:
                                if min_trans_line == jtem.get('LINE_NUM'):
                                    min_station_code_list += jtem.get(
                                        'STATION_CD')
                                    min_station_code_list += ','
                    min_joined_station_code_list1 = " ".join(
                        min_station_code_list)
                    min_joined_station_code_list1 = min_joined_station_code_list1.replace(
                        " ", "")
                    min_joined_station_code_list1 = min_joined_station_code_list1.split(
                        ',')
                    min_joined_station_code_list1 = [
                        v for v in min_joined_station_code_list1 if v]

                    print('환승 1 회 최소환승')
                    print(min_joined_station_code_list1)

                    min_trans_start_code = min_joined_station_code_list1[0]
                    min_trans_next_code = min_joined_station_code_list1[1]

                    # 최소 환승 1회시 환승역 열차 도착시간 구하기

                    if min_trans_line == '03호선' or min_trans_line == '04호선' or min_trans_line == '05호선' or min_trans_line == '07호선' or min_trans_line == '08호선' or min_trans_line == '수인분당선' or min_trans_line == '신분당선' or min_trans_line == '공항철도':
                        if int(min_trans_start_code) - int(min_trans_next_code) > 0:
                            min_trans_up_down_tag = '1'
                        else:
                            min_trans_up_down_tag = '2'
                    elif min_trans_line == '01호선' or min_trans_line == '02호선' or min_trans_line == '06호선' or min_trans_line == '09호선':
                        if int(min_trans_start_code) - int(min_trans_next_code) > 0:
                            min_trans_up_down_tag = '2'
                        else:
                            min_trans_up_down_tag = '1'

                    min_time_table_trans_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                        '/json/SearchSTNTimeTableByIDService/1/300/' + \
                        min_trans_start_code+'/'+week_tag+'/'+min_trans_up_down_tag
                    min_time_table_trans_response = requests.get(
                        (min_time_table_trans_url))
                    min_time_table_trans_resdata = min_time_table_trans_response.text
                    min_time_table_trans_obj = json.loads(
                        min_time_table_trans_resdata)
                    min_time_table_trans_obj = min_time_table_trans_obj['SearchSTNTimeTableByIDService']
                    min_time_table_trans_obj = min_time_table_trans_obj['row']

                    min_trans_path_api_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
                        path_key+'/json/shortestRoute/0/5/'+searchword+'/'+min_trans_station
                    min_trans_path_response = requests.get(
                        min_trans_path_api_url)
                    min_trans_path_resdata = min_trans_path_response.text
                    min_trans_path_obj = json.loads(min_trans_path_resdata)
                    try:
                        min_trans_path_obj = min_trans_path_obj['shortestRouteList']
                    except KeyError:
                        print("keyerror")

                    for item in min_trans_path_obj:
                        min_trans_path_time = item.get('shtTravelTm')

                    print(min_trans_path_time)

                    min_trans_first_time1 = min_joined_time_table_list[0]

                    min_trans_first_time1_min = int(
                        min_trans_first_time1[3:5]) + int(min_trans_path_time[0:])
                    if min_trans_first_time1_min < 60:
                        min_trans_first_time1_min = int(
                            min_trans_first_time1[3:5]) + int(min_trans_path_time[0:])
                        min_trans_arrival_time1 = min_trans_first_time1[:2] + ':' + \
                            str(min_trans_first_time1_min) + \
                            ':' + min_trans_first_time1[6:]
                    if min_trans_first_time1_min >= 60:
                        min_trans_first_time1_min = int(
                            min_trans_first_time1[3:5]) + int(min_trans_path_time[0:]) - 60
                        min_trans_first_time1_hour = int(
                            min_trans_first_time1[:2]) + 1
                        if int(min_trans_first_time1_min) < 10:
                            min_trans_arrival_time1 = str(
                                min_trans_first_time1_hour) + ':0' + str(min_trans_first_time1_min) + ':' + min_trans_first_time1[6:]
                        else:
                            min_trans_arrival_time1 = str(min_trans_first_time1_hour) + ':' + \
                                str(min_trans_first_time1_min) + \
                                ':' + min_trans_first_time1[6:]

                    print(min_trans_arrival_time1)

                    print('환승역(1) 시간표')
                    break_index_index1 = 0
                    min_time_table_list1 = []
                    min_train_num_list1 = []
                    last_time = []
                    for item in min_time_table_trans_obj:

                        if min_trans_arrival_time1 > item.get('ARRIVETIME'):
                            last_time = item.get('ARRIVETIME')

                        elif min_trans_arrival_time1 < item.get('ARRIVETIME'):
                            min_time_table_list1 += item.get('ARRIVETIME')
                            min_time_table_list1 += ','
                            min_train_num_list1 += item.get('TRAIN_NO')
                            min_train_num_list1 += ','

                            break_index_index1 += 1
                            if break_index_index1 == 3:
                                break

                    min_joined_time_table_list1 = " ".join(
                        min_time_table_list1)
                    min_joined_time_table_list1 = min_joined_time_table_list1.replace(
                        " ", "")
                    min_joined_time_table_list1 = min_joined_time_table_list1.split(
                        ',')
                    min_joined_time_table_list1 = [
                        v for v in min_joined_time_table_list1 if v]

                    print(min_joined_time_table_list1)

                    min_joined_train_num_list1 = " ".join(min_train_num_list1)
                    min_joined_train_num_list1 = min_joined_train_num_list1.replace(
                        " ", "")
                    min_joined_train_num_list1 = min_joined_train_num_list1.split(
                        ',')
                    min_joined_train_num_list1 = [
                        v for v in min_joined_train_num_list1 if v]

                    # ----------------------------------------------------------------------------------------------------------------------------
                    if min_path_trans_cnt == '2' or min_path_trans_cnt == '3':
                        print('최소환승 경로 환승 횟수가 2 회 ')

                        # 환승 호선 기준으로 호선 내 지하철 역 찾기 (최소환승)
                        # 서울교통공사 노선별 지하철역 정보  http://data.seoul.go.kr/dataList/OA-15442/S/1/datasetView.do

                        min_trans_line_api_url = 'http://openapi.seoul.go.kr:8088/'+key_num + \
                            '/json/SearchSTNBySubwayLineInfo/1/200/ / /'+min_trans_line
                        min_trans_line_response = requests.get(
                            min_trans_line_api_url)
                        min_trans_line_resdata = min_trans_line_response.text
                        min_trans_line_obj = json.loads(min_trans_line_resdata)

                        min_trans_line_obj = min_trans_line_obj['SearchSTNBySubwayLineInfo']
                        min_trans_line_obj = min_trans_line_obj['row']
                        min_trans_station_list = []
                        for item in min_trans_line_obj:
                            min_trans_station_list += item.get('STATION_NM')
                            min_trans_station_list += ','
                        min_joined_trans_station_list = " ".join(
                            min_trans_station_list)
                        min_joined_trans_station_list = min_joined_trans_station_list.replace(
                            " ", "")
                        min_joined_trans_station_list = min_joined_trans_station_list.split(
                            ',')
                        min_joined_trans_station_list = [
                            v for v in min_joined_trans_station_list if v]

                        if min_trans_line == '1' or min_trans_line == '01호선':
                            temp_index = min_joined_trans_station_list.index(
                                '서울역')
                            min_joined_trans_station_list[temp_index] = '서울'

                        # 최소 시간 경로 환승경로 지정하기

                        min_joined_station_list2 = []
                        for item in min_after_trans_path_list:
                            for jtem in min_joined_trans_station_list:
                                if item == jtem:
                                    min_joined_station_list2 += jtem
                                    min_joined_station_list2 += ','
                                    break

                        min_joined_path_station_list2 = " ".join(
                            min_joined_station_list2)
                        min_joined_path_station_list2 = min_joined_path_station_list2.replace(
                            " ", "")
                        min_joined_path_station_list2 = min_joined_path_station_list2.split(
                            ',')

                        # trans_station <--- 환승역임
                        min_trans_station2 = min_joined_path_station_list2[-2]

                        min_index2 = min_after_trans_path_list.index(
                            min_trans_station2)

                        # 환승역 다음 역
                        min_next_trans_station2 = min_after_trans_path_list[min_index2+2]

                        # 환승역 기준 다시 도착역 까지 경로
                        # 1회 환승 이후 노선 찾기

                        if min_trans_station2 == '서울':
                            min_trans_station2 = '서울역'
                        # 환승역 노선 찾기
                        min_trans_api_url2 = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                            '/json/SearchInfoBySubwayNameService/1/5/'+min_trans_station2
                        min_trans_response2 = requests.get(min_trans_api_url2)
                        min_trans_resdata2 = min_trans_response2.text
                        min_trans_obj2 = json.loads(min_trans_resdata2)
                        try:
                            min_trans_obj2 = min_trans_obj2['SearchInfoBySubwayNameService']
                            min_trans_obj2 = min_trans_obj2['row']
                        except KeyError:
                            print("keyerror")

                        min_trans_line_list2 = []
                        for item in min_trans_obj2:
                            min_trans_line_list2 += item.get('LINE_NUM')
                            min_trans_line_list2 += ','
                        min_joined_trans_line_list2 = " ".join(
                            min_trans_line_list2)
                        min_joined_trans_line_list2 = min_joined_trans_line_list2.replace(
                            " ", "")
                        min_joined_trans_line_list2 = min_joined_trans_line_list2.split(
                            ',')
                        min_joined_trans_line_list2 = [
                            v for v in min_joined_trans_line_list2 if v]

                        if min_next_trans_station2 == '서울':
                            min_next_trans_station2 = '서울역'

                        # 환승역 다음역 노선 찾기
                        min_next_trans_api_url2 = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                            '/json/SearchInfoBySubwayNameService/1/5/'+min_next_trans_station2
                        min_next_trans_response2 = requests.get(
                            min_next_trans_api_url2)
                        min_next_trans_resdata2 = min_next_trans_response2.text
                        min_next_trans_obj2 = json.loads(
                            min_next_trans_resdata2)
                        try:
                            min_next_trans_obj2 = min_next_trans_obj2['SearchInfoBySubwayNameService']
                            min_next_trans_obj2 = min_next_trans_obj2['row']
                        except KeyError:
                            print("keyerror")

                        min_next_trans_line_list2 = []
                        for item in min_next_trans_obj2:
                            min_next_trans_line_list2 += item.get('LINE_NUM')
                            min_next_trans_line_list2 += ','
                        min_next_joined_trans_line_list2 = " ".join(
                            min_next_trans_line_list2)
                        min_next_joined_trans_line_list2 = min_next_joined_trans_line_list2.replace(
                            " ", "")
                        min_next_joined_trans_line_list2 = min_next_joined_trans_line_list2.split(
                            ',')
                        min_next_joined_trans_line_list2 = [
                            v for v in min_next_joined_trans_line_list2 if v]

                        # 환승 이후 노선 찾기

                        for item in min_joined_trans_line_list2:
                            for jtem in min_next_joined_trans_line_list2:
                                if item == jtem:
                                    min_trans_line2 = jtem
                                    break

                        # 환승 이후 경로
                        min_after_trans_path_list2 = min_after_trans_path_list[min_index2:]

                        # 최소 환승 경로 역코드 딕셔너리 만들기 2회 환승 이후!
                        min_station_code_list = []
                        for item in min_after_trans_path_list2:
                            for jtem in min_path_code_obj:

                                if jtem.get('STATION_NM') == item:
                                    if min_trans_line2 == jtem.get('LINE_NUM'):
                                        min_station_code_list += jtem.get(
                                            'STATION_CD')
                                        min_station_code_list += ','
                        min_joined_station_code_list2 = " ".join(
                            min_station_code_list)
                        min_joined_station_code_list2 = min_joined_station_code_list2.replace(
                            " ", "")
                        min_joined_station_code_list2 = min_joined_station_code_list2.split(
                            ',')
                        min_joined_station_code_list2 = [
                            v for v in min_joined_station_code_list2 if v]

                        print('환승 2 회 최소환승')
                        print(min_joined_station_code_list2)

                        min_trans_start_code2 = min_joined_station_code_list2[0]
                        min_trans_next_code2 = min_joined_station_code_list2[1]

                        # 환승 2번 했을 시 환승역 출발시간(최소환승시)
                        if min_trans_line2 == '03호선' or min_trans_line2 == '04호선' or min_trans_line2 == '05호선' or min_trans_line2 == '07호선' or min_trans_line2 == '08호선' or min_trans_line2 == '수인분당선' or min_trans_line2 == '신분당선' or min_trans_line2 == '공항철도':
                            if int(min_trans_start_code2) - int(min_trans_next_code2) > 0:
                                min_trans_up_down_tag2 = '1'
                            else:
                                min_trans_up_down_tag2 = '2'
                        elif min_trans_line2 == '01호선' or min_trans_line2 == '02호선' or min_trans_line2 == '06호선' or min_trans_line2 == '09호선':
                            if int(min_trans_start_code2) - int(min_trans_next_code2) > 0:
                                min_trans_up_down_tag2 = '2'
                            else:
                                min_trans_up_down_tag2 = '1'

                        min_time_table_trans2_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                            '/json/SearchSTNTimeTableByIDService/1/300/' + \
                            min_trans_start_code2+'/'+week_tag+'/'+min_trans_up_down_tag2
                        min_time_table_trans2_response = requests.get(
                            (min_time_table_trans2_url))
                        min_time_table_trans2_resdata = min_time_table_trans2_response.text
                        min_time_table_trans2_obj = json.loads(
                            min_time_table_trans2_resdata)
                        min_time_table_trans2_obj = min_time_table_trans2_obj[
                            'SearchSTNTimeTableByIDService']
                        min_time_table_trans2_obj = min_time_table_trans2_obj['row']

                        min_trans_path2_api_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
                            path_key+'/json/shortestRoute/0/5/'+min_trans_station+'/'+min_trans_station2
                        min_trans_path2_response = requests.get(
                            min_trans_path2_api_url)
                        min_trans_path2_resdata = min_trans_path2_response.text
                        min_trans_path2_obj = json.loads(
                            min_trans_path2_resdata)
                        try:
                            min_trans_path2_obj = min_trans_path2_obj['shortestRouteList']
                        except KeyError:
                            print("keyerror")

                        for item in min_trans_path2_obj:
                            min_trans_path_time2 = item.get('shtTravelTm')

                        print(min_trans_path_time2)

                        min_trans_first_time2 = min_joined_time_table_list1[0]

                        min_trans_first_time2_min = int(
                            min_trans_first_time2[3:5]) + int(min_trans_path_time2[0:])
                        if min_trans_first_time2_min < 60:
                            min_trans_first_time2_min = int(
                                min_trans_first_time2[3:5]) + int(min_trans_path_time2[0:])
                            min_trans_arrival_time2 = min_trans_first_time2[:2] + ':' + \
                                str(min_trans_first_time2_min) + \
                                ':' + min_trans_first_time2[6:]
                        if min_trans_first_time2_min >= 60:
                            min_trans_first_time2_min = int(
                                min_trans_first_time2[3:5]) + int(min_trans_path_time2[0:]) - 60
                            min_trans_first_time2_hour = int(
                                min_trans_first_time2[:2]) + 1
                            if int(min_trans_first_time2_min) < 10:
                                min_trans_arrival_time2 = str(
                                    min_trans_first_time2_hour) + ':0' + str(min_trans_first_time2_min) + ':' + min_trans_first_time2[6:]
                            else:
                                min_trans_arrival_time2 = str(min_trans_first_time2_hour) + ':' + \
                                    str(min_trans_first_time2_min) + \
                                    ':' + min_trans_first_time2[6:]

                        print(min_trans_arrival_time2)

                        print('환승역(2) 시간표')
                        break_index_index2 = 0
                        min_time_table_list2 = []
                        min_train_num_list2 = []
                        last_time = []
                        for item in min_time_table_trans2_obj:

                            if min_trans_arrival_time2 > item.get('ARRIVETIME'):
                                last_time = item.get('ARRIVETIME')

                            elif min_trans_arrival_time2 < item.get('ARRIVETIME'):
                                min_time_table_list2 += item.get('ARRIVETIME')
                                min_time_table_list2 += ','
                                min_train_num_list2 += item.get('TRAIN_NO')
                                min_train_num_list2 += ','

                                break_index_index2 += 1
                                if break_index_index2 == 3:
                                    break

                        min_joined_time_table_list2 = " ".join(
                            min_time_table_list2)
                        min_joined_time_table_list2 = min_joined_time_table_list2.replace(
                            " ", "")
                        min_joined_time_table_list2 = min_joined_time_table_list2.split(
                            ',')
                        min_joined_time_table_list2 = [
                            v for v in min_joined_time_table_list2 if v]

                        print(min_joined_time_table_list2)

                        min_joined_train_num_list2 = " ".join(
                            min_train_num_list2)
                        min_joined_train_num_list2 = min_joined_train_num_list2.replace(
                            " ", "")
                        min_joined_train_num_list2 = min_joined_train_num_list2.split(
                            ',')
                        min_joined_train_num_list2 = [
                            v for v in min_joined_train_num_list2 if v]

                        if min_path_trans_cnt == '3':
                            print('최소환승 경로 환승 횟수가 3 회 ')
                            # 환승 횟수 3회 일 때의 코드 작성

                            # 환승 호선 기준으로 호선 내 지하철 역 찾기 (최단시간)
                            # 서울교통공사 노선별 지하철역 정보  http://data.seoul.go.kr/dataList/OA-15442/S/1/datasetView.do

                            min_trans_line_api_url3 = 'http://openapi.seoul.go.kr:8088/'+key_num + \
                                '/json/SearchSTNBySubwayLineInfo/1/200/ / /'+min_trans_line2
                            min_trans_line_response3 = requests.get(
                                min_trans_line_api_url3)
                            min_trans_line_resdata3 = min_trans_line_response3.text
                            min_trans_line_obj3 = json.loads(
                                min_trans_line_resdata3)

                            min_trans_line_obj3 = min_trans_line_obj3['SearchSTNBySubwayLineInfo']
                            min_trans_line_obj3 = min_trans_line_obj3['row']
                            min_trans_station_list3 = []
                            for item in min_trans_line_obj3:
                                min_trans_station_list3 += item.get(
                                    'STATION_NM')
                                min_trans_station_list3 += ','
                            min_joined_trans_station_list3 = " ".join(
                                min_trans_station_list3)
                            min_joined_trans_station_list3 = min_joined_trans_station_list3.replace(
                                " ", "")
                            min_joined_trans_station_list3 = min_joined_trans_station_list3.split(
                                ',')
                            min_joined_trans_station_list3 = [
                                v for v in min_joined_trans_station_list3 if v]

                            if min_trans_line2 == '1' or min_trans_line2 == '01호선':
                                temp_index = min_joined_trans_station_list3.index(
                                    '서울역')
                                min_joined_trans_station_list3[temp_index] = '서울'

                            # 최소 시간 경로 환승경로 지정하기

                            min_trans_path_station_list3 = []
                            for item in min_after_trans_path_list2:
                                for jtem in min_joined_trans_station_list3:
                                    if item == jtem:
                                        min_trans_path_station_list3 += jtem
                                        min_trans_path_station_list3 += ','
                                        break

                            min_joined_path_station_list3 = " ".join(
                                min_trans_path_station_list3)
                            min_joined_path_station_list3 = min_joined_path_station_list3.replace(
                                " ", "")
                            min_joined_path_station_list3 = min_joined_path_station_list3.split(
                                ',')

                            # trans_station <--- 환승역임
                            min_trans_station3 = min_joined_path_station_list3[-2]

                            min_index3 = min_after_trans_path_list2.index(
                                min_trans_station3)

                            # 환승역 다음 역
                            min_next_trans_station3 = min_after_trans_path_list2[index3+1]
                            # 환승역 기준 다시 도착역 까지 경로
                            # 1회 환승 이후 노선 찾기

                            if min_trans_station3 == '서울':
                                min_trans_station3 = '서울역'

                            # 환승역 노선 찾기
                            min_trans_api_url3 = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                                '/json/SearchInfoBySubwayNameService/1/5/'+min_trans_station3
                            min_trans_response3 = requests.get(
                                min_trans_api_url3)
                            min_trans_resdata3 = min_trans_response3.text
                            min_trans_obj3 = json.loads(min_trans_resdata3)
                            try:
                                min_trans_obj3 = min_trans_obj3['SearchInfoBySubwayNameService']
                                min_trans_obj3 = min_trans_obj3['row']
                            except KeyError:
                                print("keyerror")

                            min_trans_line_list3 = []
                            for item in min_trans_obj3:
                                min_trans_line_list3 += item.get('LINE_NUM')
                                min_trans_line_list3 += ','
                            min_joined_trans_line_list3 = " ".join(
                                min_trans_line_list3)
                            min_joined_trans_line_list3 = min_joined_trans_line_list3.replace(
                                " ", "")
                            min_joined_trans_line_list3 = min_joined_trans_line_list3.split(
                                ',')
                            min_joined_trans_line_list3 = [
                                v for v in min_joined_trans_line_list3 if v]

                            if min_next_trans_station3 == '서울':
                                min_next_trans_station3 = '서울역'
                            # 환승역 다음역 노선 찾기
                            min_next_trans_api_url3 = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                                '/json/SearchInfoBySubwayNameService/1/5/'+min_next_trans_station3
                            min_next_trans_response3 = requests.get(
                                min_next_trans_api_url3)
                            min_next_trans_resdata3 = min_next_trans_response3.text
                            min_next_trans_obj3 = json.loads(
                                min_next_trans_resdata3)
                            try:
                                min_next_trans_obj3 = min_next_trans_obj3['SearchInfoBySubwayNameService']
                                min_next_trans_obj3 = min_next_trans_obj3['row']
                            except KeyError:
                                print("keyerror")

                            min_next_trans_line_list3 = []
                            for item in min_next_trans_obj3:
                                min_next_trans_line_list3 += item.get(
                                    'LINE_NUM')
                                min_next_trans_line_list3 += ','
                            min_next_joined_trans_line_list3 = " ".join(
                                min_next_trans_line_list3)
                            min_next_joined_trans_line_list3 = min_next_joined_trans_line_list3.replace(
                                " ", "")
                            min_next_joined_trans_line_list3 = min_next_joined_trans_line_list3.split(
                                ',')
                            min_next_joined_trans_line_list3 = [
                                v for v in min_next_joined_trans_line_list3 if v]

                            # 환승 이후 노선 찾기

                            for item in min_joined_trans_line_list3:
                                for jtem in min_next_joined_trans_line_list3:
                                    if item == jtem:
                                        min_trans_line3 = jtem
                                        break

                            # 환승 이후 경로
                            min_after_trans_path_list3 = min_after_trans_path_list2[min_index3:]

                            # 최소 환승 경로 역코드 딕셔너리 만들기 3회 환승 이후!
                            min_station_code_list = []
                            for item in min_after_trans_path_list3:
                                for jtem in min_path_code_obj:

                                    if jtem.get('STATION_NM') == item:
                                        if min_trans_line3 == jtem.get('LINE_NUM'):
                                            min_station_code_list += jtem.get(
                                                'STATION_CD')
                                            min_station_code_list += ','
                            min_joined_station_code_list3 = " ".join(
                                min_station_code_list)
                            min_joined_station_code_list3 = min_joined_station_code_list3.replace(
                                " ", "")
                            min_joined_station_code_list3 = min_joined_station_code_list3.split(
                                ',')
                            min_joined_station_code_list3 = [
                                v for v in min_joined_station_code_list3 if v]

                            print('환승 0 회 최소환승')
                            print(min_joined_station_code_list3)

                            min_trans_start_code3 = min_joined_station_code_list3[0]
                            min_trans_next_code3 = min_joined_station_code_list3[1]

                            # 환승 3번 했을 시 환승역 출발시간(최소환승시)
                            if min_trans_line3 == '03호선' or min_trans_line3 == '04호선' or min_trans_line3 == '05호선' or min_trans_line3 == '07호선' or min_trans_line3 == '08호선' or min_trans_line3 == '수인분당선' or min_trans_line3 == '신분당선' or min_trans_line3 == '공항철도':
                                if int(min_trans_start_code3) - int(min_trans_next_code3) > 0:
                                    min_trans_up_down_tag3 = '1'
                                else:
                                    min_trans_up_down_tag3 = '2'
                            elif min_trans_line3 == '01호선' or min_trans_line3 == '02호선' or min_trans_line3 == '06호선' or min_trans_line3 == '09호선':
                                if int(min_trans_start_code3) - int(min_trans_next_code3) > 0:
                                    min_trans_up_down_tag3 = '2'
                                else:
                                    min_trans_up_down_tag3 = '1'

                            min_time_table_trans3_url = 'http://openAPI.seoul.go.kr:8088/'+key_num + \
                                '/json/SearchSTNTimeTableByIDService/1/300/' + \
                                min_trans_start_code3+'/'+week_tag+'/'+min_trans_up_down_tag3
                            min_time_table_trans3_response = requests.get(
                                (min_time_table_trans3_url))
                            min_time_table_trans3_resdata = min_time_table_trans3_response.text
                            min_time_table_trans3_obj = json.loads(
                                min_time_table_trans3_resdata)
                            min_time_table_trans3_obj = min_time_table_trans3_obj[
                                'SearchSTNTimeTableByIDService']
                            min_time_table_trans3_obj = min_time_table_trans3_obj['row']

                            min_trans_path3_api_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
                                path_key+'/json/shortestRoute/0/5/'+min_trans_station2+'/'+min_trans_station3
                            min_trans_path3_response = requests.get(
                                min_trans_path3_api_url)
                            min_trans_path3_resdata = min_trans_path3_response.text
                            min_trans_path3_obj = json.loads(
                                min_trans_path3_resdata)
                            try:
                                min_trans_path3_obj = min_trans_path3_obj['shortestRouteList']
                            except KeyError:
                                print("keyerror")

                            for item in min_trans_path3_obj:
                                min_trans_path_time3 = item.get('shtTravelTm')

                            print(min_trans_path_time3)

                            min_trans_first_time3 = min_joined_time_table_list2[0]

                            min_trans_first_time3_min = int(
                                min_trans_first_time3[3:5]) + int(min_trans_path_time3[0:])
                            if min_trans_first_time3_min < 60:
                                min_trans_first_time3_min = int(
                                    min_trans_first_time3[3:5]) + int(min_trans_path_time3[0:])
                                min_trans_arrival_time3 = min_trans_first_time3[:2] + ':' + \
                                    str(min_trans_first_time3_min) + \
                                    ':' + min_trans_first_time3[6:]
                            if min_trans_first_time3_min >= 60:
                                min_trans_first_time3_min = int(
                                    min_trans_first_time3[3:5]) + int(min_trans_path_time3[0:]) - 60
                                min_trans_first_time3_hour = int(
                                    min_trans_first_time3[:2]) + 1
                                if int(min_trans_first_time3_min) < 10:
                                    min_trans_arrival_time3 = str(
                                        min_trans_first_time3_hour) + ':0' + str(min_trans_first_time3_min) + ':' + min_trans_first_time3[6:]
                                else:
                                    min_trans_arrival_time3 = str(min_trans_first_time3_hour) + ':' + \
                                        str(min_trans_first_time3_min) + \
                                        ':' + min_trans_first_time3[6:]

                            print(min_trans_arrival_time3)

                            print('환승역(3) 시간표')
                            break_index_index3 = 0
                            min_time_table_list3 = []
                            min_train_num_list3 = []
                            last_time = []
                            for item in min_time_table_trans3_obj:

                                if min_trans_arrival_time3 > item.get('ARRIVETIME'):
                                    last_time = item.get('ARRIVETIME')

                                elif min_trans_arrival_time3 < item.get('ARRIVETIME'):
                                    min_time_table_list3 += item.get(
                                        'ARRIVETIME')
                                    min_time_table_list3 += ','
                                    min_train_num_list3 += item.get('TRAIN_NO')
                                    min_train_num_list3 += ','

                                    break_index_index3 += 1
                                    if break_index_index3 == 3:
                                        break

                            min_joined_time_table_list3 = " ".join(
                                min_time_table_list3)
                            min_joined_time_table_list3 = min_joined_time_table_list3.replace(
                                " ", "")
                            min_joined_time_table_list3 = min_joined_time_table_list3.split(
                                ',')
                            min_joined_time_table_list3 = [
                                v for v in min_joined_time_table_list3 if v]

                            print(min_joined_time_table_list3)

                            min_joined_train_num_list3 = " ".join(
                                min_train_num_list3)
                            min_joined_train_num_list3 = min_joined_train_num_list3.replace(
                                " ", "")
                            min_joined_train_num_list3 = min_joined_train_num_list3.split(
                                ',')
                            min_joined_train_num_list3 = [
                                v for v in min_joined_train_num_list3 if v]

                else:
                    print('환승 횟수 0 회 ')

                ### DEBUG ###
                print('\n\n\n ### DEBUG ### \n\n\n')
                print(min_joined_path_station_list)
                print(min_joined_station_code_list)
                print(min_joined_path_station_list2)
                print(min_joined_station_code_list1)
                print(min_joined_path_station_list3)
                print(min_joined_station_code_list2)
                print(min_after_trans_path_list3)
                print(min_joined_station_code_list3)

                return render(request, 'min_flash.html', {'min_joined_time_table_list': min_joined_time_table_list, 'trans_line3': trans_line3, 'joined_path_station_list3': joined_path_station_list3, 'after_trans_path_list3': after_trans_path_list3, 'min_after_trans_path_list2': min_after_trans_path_list2, 'min_joined_path_station_list2': min_joined_path_station_list2, 'min_trans_station2': min_trans_station2, 'min_trans_line2': min_trans_line2, 'min_path_trans_cnt': min_path_trans_cnt, 'sht_path_trans_cnt': sht_path_trans_cnt, 'joined_path_station_list2': joined_path_station_list2, 'trans_line2': trans_line2, 'trans_station2': trans_station2, 'after_trans_path_list2': after_trans_path_list2, 'min_line': min_line, 'min_trans_line': min_trans_line, 'min_joined_path_station_list': min_joined_path_station_list, 'min_after_trans_path_list': min_after_trans_path_list, 'trans_line': trans_line, 'after_trans_path_list': after_trans_path_list, 'joined_path_station_list': joined_path_station_list, 'line_obj': line_obj, 'sht_line': sht_line, 'min_min_path_time': min_min_path_time, 'min_path_time': min_path_time, 'obj': obj, 'min_path_list': min_path_list, 'min_path_msg': min_path_msg, 'sht_path_msg': sht_path_msg, 'min_sht_path_time': min_sht_path_time, 'path_time': path_time, 'sht_path_list': sht_path_list, 'path_obj': path_obj, 'dest_obj': dest_obj})

            # 서울교통공사_서울 도시철도 목적지 경로정보 https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15097640
            ''' -> API 오류 HTTP ERROR
            key = 'oTsloDJ6xmHymJiItQxmn1GEp2HiiX+8fA+H6PRKbCUp3XWPNEAViCpeWOir0YPCRpFHH3XQ6i6PlYwNdEg4dQ=='
            
            api_url4 = 'http://apis.data.go.kr/B553766/smt-path/path'
            params ={'serviceKey' : key, 'pageNo' : '1', 'numOfRows' : '10', 'dept_station_code' : '2728', 'dest_station_code' : '0214', 'week' : 'DAY', 'search_type' : 'FASTEST', 'first_last' : '', 'dept_time' : '120001', 'train_seq' : '' }
            path_response = requests.get(api_url4, params=params)
            path_resdata = path_response.text
            path_obj = json.loads(path_resdata)
            path_obj = path_obj['data']
            '''
            # http://apis.data.go.kr/B553766/smt-path/path?serviceKey=oTsloDJ6xmHymJiItQxmn1GEp2HiiX%2B8fA%2BH6PRKbCUp3XWPNEAViCpeWOir0YPCRpFHH3XQ6i6PlYwNdEg4dQ%3D%3D&numOfRows=10&pageNo=1&dept_station_code=0222&dest_station_code=4117&week=DAY

            # 서울교통공사 실시간 도착 정보
            '''api_url3 = 'http://swopenAPI.seoul.go.kr/api/subway/'+key_num+'/json/realtimeStationArrival/0/1/'+destword
            response2 = requests.get(api_url3)
            findata = response2.text
            finobj = json.loads(findata)
            try:
                finobj = finobj["realtimeArrivalList"]
            except KeyError:
                print('keyerror_realtime')'''
            #############################################
            # try:
            # except UnboundLocalError:
            # print("UnboundLocalError")

            # return render(request,'detail.html',{'time_table_obj':time_table_obj,'trans_line3':trans_line3,'joined_path_station_list3':joined_path_station_list3,'after_trans_path_list3':after_trans_path_list3,'min_after_trans_path_list2':min_after_trans_path_list2,'min_joined_path_station_list2':min_joined_path_station_list2,'min_trans_station2':min_trans_station2,'min_trans_line2':min_trans_line2,'min_path_trans_cnt':min_path_trans_cnt,'sht_path_trans_cnt':sht_path_trans_cnt,'joined_path_station_list2':joined_path_station_list2,'trans_line2':trans_line2,'trans_station2':trans_station2,'after_trans_path_list2':after_trans_path_list2,'min_line':min_line,'min_trans_line':min_trans_line,'min_joined_path_station_list':min_joined_path_station_list,'min_after_trans_path_list':min_after_trans_path_list,'trans_line':trans_line,'after_trans_path_list':after_trans_path_list,'joined_path_station_list':joined_path_station_list,'line_obj':line_obj,'sht_line':sht_line,'min_min_path_time':min_min_path_time,'min_path_time':min_path_time,'obj' : obj,'min_path_list':min_path_list,'min_path_msg':min_path_msg,'sht_path_msg':sht_path_msg,'min_sht_path_time':min_sht_path_time,'path_time':path_time,'sht_path_list':sht_path_list,'path_obj':path_obj,'dest_obj':dest_obj , 'finobj' : finobj})

    else:
        form = RouteForm()

        print('홈에서 get요청?')
        print(request.GET.get('data'))

        # return render(request,'sht_path.html',{'real_time_position':real_time_position,'sht_joined_time_table_list':sht_joined_time_table_list,'trans_line3':trans_line3,'joined_path_station_list3':joined_path_station_list3,'after_trans_path_list3':after_trans_path_list3,'sht_path_trans_cnt':sht_path_trans_cnt,'joined_path_station_list2':joined_path_station_list2,'trans_line2':trans_line2,'trans_station2':trans_station2,'after_trans_path_list2':after_trans_path_list2,'trans_line':trans_line,'after_trans_path_list':after_trans_path_list,'joined_path_station_list':joined_path_station_list,'line_obj':line_obj,'sht_line':sht_line,'obj' : obj,'sht_path_msg':sht_path_msg,'path_time':path_time,'sht_path_list':sht_path_list,'path_obj':path_obj,'dest_obj':dest_obj })

    return render(request, 'home.html', {'form': form})


def setting(request):
    return render(request, 'setting.html')


def favorite(request):
    return render(request, 'favorite.html')


def detail(request):
    return render(request, 'detail.html')


def sht_path(request):
    if request.method == 'POST':
        print('POST 요청 sht_path에서')
    return render(request, 'sht_path.html')


def min_detail(request):
    if request.method == 'POST':
        print('post')
    else:

        print('get요청? in min_detail')

        form = RouteForm()

        # 1호선 K 로 시작하는 열차번호 처리
        for item in min_joined_train_num_list:
            if item.startswith('K'):
                item.replace('K', '0')

        real_time_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
            path_key+'/json/realtimePosition/0/100/'+temp_line
        real_time_response = requests.get(real_time_url)
        real_time_resdata = real_time_response.text
        real_time_obj = json.loads(real_time_resdata)
        try:
            real_time_obj = real_time_obj['realtimePositionList']
        except KeyError:
            print('KEY ERROR')

        # print(real_time_obj)

        global real_time_position
        global time_tag
        global min_real_path_list
        global min_path_msg
        global real_time_line
        try:
            for item in real_time_obj:
                if min_joined_train_num_list[0+time_tag] == item.get('trainNo'):
                    print(item.get('trainNo'))

                    real_time_position = item.get('statnNm')
                    print(real_time_position)

        except AttributeError:
            print('AttributeError')
        except IndexError:
            print('IndexError')

    return render(request, 'min_detail.html', {'real_time_line': real_time_line, 'min_real_path_list': min_real_path_list, 'real_time_position': real_time_position, 'min_joined_time_table_list': min_joined_time_table_list, 'trans_line3': trans_line3, 'min_joined_path_station_list3': min_joined_path_station_list3, 'min_after_trans_path_list3': min_after_trans_path_list3, 'min_path_trans_cnt': min_path_trans_cnt, 'min_joined_path_station_list2': min_joined_path_station_list2, 'min_trans_line2': min_trans_line2, 'min_trans_station2': min_trans_station2, 'min_after_trans_path_list2': min_after_trans_path_list2, 'min_trans_line': min_trans_line, 'min_after_trans_path_list': min_after_trans_path_list, 'min_joined_path_station_list': min_joined_path_station_list, 'line_obj': line_obj, 'min_line': min_line, 'obj': obj, 'min_path_msg': min_path_msg, 'path_time': path_time, 'min_path_list': min_path_list, 'path_obj': path_obj, 'dest_obj': dest_obj})


def flash(request):
    return render(request, 'flash.html')


def sht_detail(request):
    if request.method == 'POST':
        print('post')
    else:

        print('get요청? in sht_detail')

        form = RouteForm()

        # 1호선 K 로 시작하는 열차번호 처리
        for item in sht_joined_train_num_list:
            if item.startswith('K'):
                item.replace('K', '0')

        real_time_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
            path_key+'/json/realtimePosition/0/100/'+temp_line
        real_time_response = requests.get(real_time_url)
        real_time_resdata = real_time_response.text
        real_time_obj = json.loads(real_time_resdata)
        try:
            real_time_obj = real_time_obj['realtimePositionList']
        except KeyError:
            print('KEY ERROR')

        # print(real_time_obj)

        global real_time_position
        global time_tag
        global sht_real_path_list
        global real_time_line
        try:
            for item in real_time_obj:
                if sht_joined_train_num_list[0+time_tag] == item.get('trainNo'):
                    print(item.get('trainNo'))

                    real_time_position = item.get('statnNm')
                    print(real_time_position)

        except AttributeError:
            print('AttributeError')
        except IndexError:
            print('IndexError')

    return render(request, 'sht_detail.html', {'real_time_line': real_time_line, 'sht_real_path_list': sht_real_path_list, 'real_time_position': real_time_position, 'sht_joined_time_table_list': sht_joined_time_table_list, 'trans_line3': trans_line3, 'joined_path_station_list3': joined_path_station_list3, 'after_trans_path_list3': after_trans_path_list3, 'sht_path_trans_cnt': sht_path_trans_cnt, 'joined_path_station_list2': joined_path_station_list2, 'trans_line2': trans_line2, 'trans_station2': trans_station2, 'after_trans_path_list2': after_trans_path_list2, 'trans_line': trans_line, 'after_trans_path_list': after_trans_path_list, 'joined_path_station_list': joined_path_station_list, 'line_obj': line_obj, 'sht_line': sht_line, 'obj': obj, 'sht_path_msg': sht_path_msg, 'path_time': path_time, 'sht_path_list': sht_path_list, 'path_obj': path_obj, 'dest_obj': dest_obj})


def sht(request):
    if request.method == 'POST':
        print('post')
    else:
        global real_time_position
        global real_time_position1
        global destword
        global real_time_line
        global real_time_line1
        global sht_path_list
        global sht_real_path_list
        global real_next_station
        global real_next_station1
        global sht_path_trans_cnt
        global sht_path_msg
        global arrive_tag
        global arrive_tag1
        global left_tag
        global left_tag1
        global last_time
        global found
        global found1
        global time_tag
        global time_tag1
        global user_token
        global resgistration
        global found_cnt
        global found_cnt1
        arrive_tag = 0
        arrive_tag1 = 0
        time_tag = 0
        time_tag1 = 0
        left_tag = 0
        left_tag1 = 0
        print('get요청? in sht')

        form = RouteForm()

        # 1호선 K 로 시작하는 열차번호 처리
        for item in sht_joined_train_num_list:
            if item.startswith('K'):
                item.replace('K', '0')

        # 서울시 지하철 실시간 열차 위치정보 http://data.seoul.go.kr/dataList/OA-12601/A/1/datasetView.do

        # 선택 시간 받아오기 GET 요청
        selected_time = request.GET.get('time_drop_list')
        print('선택된 시간', selected_time)
        if selected_time == 'first':
            time_tag = 0
            print('first selected')
        elif selected_time == 'second':
            time_tag = 1
        elif selected_time == 'third':
            time_tag = 2
        # elif selected_time == 'last':
        #    time_tag = -1

        real_time_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
            path_key+'/json/realtimePosition/0/100/'+temp_line
        real_time_response = requests.get(real_time_url)
        real_time_resdata = real_time_response.text
        real_time_obj = json.loads(real_time_resdata)
        try:
            real_time_obj = real_time_obj['realtimePositionList']
        except KeyError:
            print('KEY ERROR')
            return render(request, 'sht.html', {'left_tag': left_tag, 'last_time': last_time, 'arrive_tag': arrive_tag, 'real_next_station': real_next_station, 'real_time_line': real_time_line, 'sht_joined_time_table_list': sht_joined_time_table_list, 'real_time_position': real_time_position, 'destword': destword})

        # print(real_time_obj)

        print(sht_joined_train_num_list)
        try:
            for item in real_time_obj:

                if sht_joined_train_num_list[0+time_tag] == item.get('trainNo'):
                    print(item.get('trainNo'))
                    real_time_line = item.get('subwayNm')
                    real_time_position = item.get('statnNm')
                    print(real_time_position)

        except AttributeError:
            print('AttributeError')
        except IndexError:
            print('IndexError')

        if real_time_position == '공릉(서울산업대입구)':
            real_time_position = '공릉'
        if real_time_position == '군자(능동)':
            real_time_position = '군자'
        if real_time_position == '어린이대공원(세종대)':
            real_time_position = '어린이대공원'

        print(real_time_position)
        print(destword)

        # 현재 역 다음 역 찾기.
        # 지하철 경로 조회 서비스 https://devming.tistory.com/214 |http://swopenAPI.seoul.go.kr/api/subway/인증Key값/요청데이터형식/OpenAPI 이름(서비스명)/요청 데이터 행 시작번호/요청 데이터 행 끝번호/출발역명/도착역명

        path_api_url = 'http://swopenAPI.seoul.go.kr/api/subway/'+key_num + \
            '/json/shortestRoute/0/5/'+real_time_position+'/'+destword
        path_response = requests.get(path_api_url)
        path_resdata = path_response.text
        path_obj = json.loads(path_resdata)
        try:
            path_obj = path_obj['shortestRouteList']
        except KeyError:
            print("keyerror")
            send_notification(resgistration, 'Notty 알림', '목적지에 도착했습니다.')
            return render(request, 'arrive.html', {'left_tag': left_tag, 'last_time': last_time, 'arrive_tag': arrive_tag, 'real_next_station': real_next_station, 'real_time_line': real_time_line, 'sht_joined_time_table_list': sht_joined_time_table_list, 'real_time_position': real_time_position, 'destword': destword})

        # 최단 시간 찾기
        path_time = [9999, 9999, 9999, 9999,
                     9999, 9999, 9999, 9999, 9999, 9999]

        i = 0
        try:
            for time_set in path_obj:
                path_time[i] = int(time_set.get('shtTravelTm'))
                i = i+1
        except AttributeError:
            print("AttributeError")
        min_sht_path_time = min(path_time)

        try:
            for item in path_obj:
                sht_real_path_list = item.get('shtStatnNm')
                # sht_path_msg = item.get('shtTravelMsg') 실시간 기반 소요 시간 환승 횟수 메시지
                sht_path_trans_cnt = item.get('shtTransferCnt')
                # sht_path_time = item.get('shtTravelTm') 실시간 기반 소요 시간
                if min_sht_path_time == int(item.get('shtTravelTm')):
                    break
        except AttributeError:
            print('AttributeError')
        print(sht_real_path_list)

        try:
            sht_real_path_list = sht_real_path_list.replace(" ", "")
            sht_real_path_list = sht_real_path_list.split(',')
        except AttributeError:
            print('Attribute Error')
        try:
            found = sht_real_path_list.index(sht_path_list[0])
        except ValueError:
            print('valueError')
            found = 0

        if found_cnt == 0:
            if real_time_position == sht_real_path_list[found]:
                left_tag = 1
                found_cnt = 1
            elif real_time_position == sht_real_path_list[found-1]:
                left_tag = 2
            elif real_time_position == sht_real_path_list[found-2]:
                left_tag = 3
            elif real_time_position == sht_real_path_list[found-3]:
                left_tag = 4
            else:
                print('출발 태그 예외')
                left_tag = 99
        else:
            print('출발 태그 예외')
            left_tag = 99

            global notification_cnt
            resgistration = [user_token]

            print(found)
            print(sht_real_path_list)
            print(real_time_position)

            print('tag')
            print(left_tag)
            print(arrive_tag)
            print(notification_cnt)
            if real_time_position == sht_real_path_list[-2]:
                arrive_tag = 1
                if notification_cnt == 2:
                    send_notification(
                        resgistration, 'Notty 알림', '목적지에 도착했습니다.')
                print('도착역 도착')

            elif real_time_position == sht_real_path_list[-3]:
                arrive_tag = 2
                print('도착역 전 역 도착')
                if notification_cnt == 1:
                    send_notification(resgistration, 'Notty 알림',
                                      '전 역에 도착했습니다. 내릴 준비 해주세요.')
                    notification_cnt += 1

            elif real_time_position == sht_real_path_list[-4]:
                arrive_tag = 3
                print('도착역 전전역 도착')
                if notification_cnt == 0:
                    send_notification(resgistration, 'Notty 알림',
                                      '전전 역에 도착했습니다. 내릴 준비 해주세요.')
                    notification_cnt += 1
            else:
                print("도착 태그 예외")

        if arrive_tag == 1:
            print('도착')
            return render(request, 'arrive.html')

        # 실시간 다음역 지정
        real_next_station = sht_real_path_list[1]

        # 환승 1회시 실시간 열차 정보

        if real_time_line1 == trans_line:
            if sht_path_trans_cnt == '1' or sht_path_trans_cnt == '2' or sht_path_trans_cnt == '3':

                for item in sht_joined_train_num_list1:
                    if item.startswith('K'):
                        item.replace('K', '0')

                selected_time1 = request.GET.get('time_drop_list')
                print('선택된 시간', selected_time1)
                if selected_time1 == 'first':
                    time_tag1 = 0
                    print('first selected')
                elif selected_time1 == 'second':
                    time_tag1 = 1
                elif selected_time1 == 'third':
                    time_tag1 = 2
                # elif selected_time == 'last':
                #    time_tag = -1

                real_time1_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
                    path_key+'/json/realtimePosition/0/100/'+trans_line
                real_time1_response = requests.get(real_time1_url)
                real_time1_resdata = real_time1_response.text
                real_time1_obj = json.loads(real_time1_resdata)
                try:
                    real_time1_obj = real_time1_obj['realtimePositionList']
                except KeyError:
                    print('KEY ERROR')
                    return render(request, 'sht.html', {'left_tag1': left_tag1, 'last_time': last_time, 'arrive_tag1': arrive_tag1, 'real_next_station1': real_next_station1, 'real_time_line1': real_time_line1, 'sht_joined_time_table_list1': sht_joined_time_table_list1, 'real_time_position1': real_time_position1, 'destword': destword})

                # print(real_time_obj)

                print(sht_joined_train_num_list1)
                try:
                    for item in real_time1_obj:

                        if sht_joined_train_num_list1[0+time_tag1] == item.get('trainNo'):
                            print(item.get('trainNo'))
                            real_time_line1 = item.get('subwayNm')
                            real_time_position1 = item.get('statnNm')
                            print(real_time_position1)

                except AttributeError:
                    print('AttributeError')
                except IndexError:
                    print('IndexError')

                if real_time_position1 == '공릉(서울산업대입구)':
                    real_time_position1 = '공릉'
                if real_time_position1 == '군자(능동)':
                    real_time_position1 = '군자'
                if real_time_position1 == '어린이대공원(세종대)':
                    real_time_position1 = '어린이대공원'

                print(real_time_position1)
                print(destword)

                # 현재 역 다음 역 찾기.
                # 지하철 경로 조회 서비스 https://devming.tistory.com/214 |http://swopenAPI.seoul.go.kr/api/subway/인증Key값/요청데이터형식/OpenAPI 이름(서비스명)/요청 데이터 행 시작번호/요청 데이터 행 끝번호/출발역명/도착역명

                path1_api_url = 'http://swopenAPI.seoul.go.kr/api/subway/'+key_num + \
                    '/json/shortestRoute/0/5/'+real_time_position1+'/'+destword
                path1_response = requests.get(path1_api_url)
                path1_resdata = path1_response.text
                path1_obj = json.loads(path1_resdata)
                try:
                    path1_obj = path1_obj['shortestRouteList']
                except KeyError:
                    print("keyerror")
                    send_notification(
                        resgistration, 'Notty 알림', '목적지에 도착했습니다.')
                    return render(request, 'arrive.html', {'left_tag1': left_tag1, 'last_time': last_time, 'arrive_tag1': arrive_tag1, 'real_next_station1': real_next_station1, 'real_time_line1': real_time_line1, 'sht_joined_time_table_list1': sht_joined_time_table_list1, 'real_time_position1': real_time_position1, 'destword': destword})

                # 최단 시간 찾기
                path_time1 = [9999, 9999, 9999, 9999,
                              9999, 9999, 9999, 9999, 9999, 9999]

                i_1 = 0
                try:
                    for time_set1 in path1_obj:
                        path_time1[i_1] = int(time_set1.get('shtTravelTm'))
                        i_1 = i_1+1
                except AttributeError:
                    print("AttributeError")
                min_sht_path_time1 = min(path_time1)

                try:
                    for item in path1_obj:
                        sht_real_path_list1 = item.get('shtStatnNm')
                        # sht_path_msg = item.get('shtTravelMsg') 실시간 기반 소요 시간 환승 횟수 메시지
                        #sht_path_trans_cnt = item.get('shtTransferCnt')
                        # sht_path_time = item.get('shtTravelTm') 실시간 기반 소요 시간
                        if min_sht_path_time1 == int(item.get('shtTravelTm')):
                            break
                except AttributeError:
                    print('AttributeError')
                print(sht_real_path_list1)

                try:
                    sht_real_path_list1 = sht_real_path_list1.replace(" ", "")
                    sht_real_path_list1 = sht_real_path_list1.split(',')
                except AttributeError:
                    print('Attribute Error')
                try:
                    found1 = sht_real_path_list1.index(
                        after_trans_path_list[0])
                except ValueError:
                    print('valueError')
                    found1 = 0

                if found1_cnt == 0:
                    if real_time_position1 == sht_real_path_list1[found1]:
                        left_tag1 = 1
                        found1_cnt = 1
                    elif real_time_position1 == sht_real_path_list1[found1-1]:
                        left_tag1 = 2
                    elif real_time_position1 == sht_real_path_list1[found1-2]:
                        left_tag1 = 3
                    elif real_time_position1 == sht_real_path_list1[found1-3]:
                        left_tag1 = 4
                    else:
                        print('출발 태그 예외')
                        left_tag1 = 99
                else:
                    print('출발 태그 예외')
                    left_tag1 = 99

                    global notification_cnt1
                    resgistration = [user_token]

                    print(found1)
                    print(sht_real_path_list1)
                    print(real_time_position1)

                    print('tag')
                    print(left_tag1)
                    print(arrive_tag1)
                    print(notification_cnt1)
                    if real_time_position1 == sht_real_path_list1[-2]:
                        arrive_tag1 = 1
                        if notification_cnt1 == 2:
                            send_notification(
                                resgistration, 'Notty 알림', '목적지에 도착했습니다.')
                        print('도착역 도착')

                    elif real_time_position1 == sht_real_path_list1[-3]:
                        arrive_tag1 = 2
                        print('도착역 전 역 도착')
                        if notification_cnt1 == 1:
                            send_notification(resgistration, 'Notty 알림',
                                              '전 역에 도착했습니다. 내릴 준비 해주세요.')
                            notification_cnt1 += 1

                    elif real_time_position1 == sht_real_path_list1[-4]:
                        arrive_tag1 = 3
                        print('도착역 전전역 도착')
                        if notification_cnt1 == 0:
                            send_notification(resgistration, 'Notty 알림',
                                              '전전 역에 도착했습니다. 내릴 준비 해주세요.')
                            notification_cnt1 += 1
                    else:
                        print("도착 태그 예외")

                if arrive_tag1 == 1:
                    print('도착')
                    return render(request, 'arrive.html')

                # 실시간 다음 열차 위치 정보
                real_next_station1 = sht_real_path_list1[1]

    return render(request, 'sht.html', {'left_tag': left_tag, 'left_tag1': left_tag1, 'last_time': last_time, 'arrive_tag': arrive_tag, 'arrive_tag1': arrive_tag1, 'real_next_station': real_next_station, 'real_next_station1': real_next_station1, 'real_time_line': real_time_line, 'real_time_line1': real_time_line1, 'sht_joined_time_table_list': sht_joined_time_table_list, 'sht_joined_time_table_list1': sht_joined_time_table_list1, 'real_time_position': real_time_position, 'real_time_position1': real_time_position1, 'destword': destword})


def real_min(request):
    if request.method == 'POST':
        print('post')
    else:
        global real_time_position
        global real_time_position
        global destword
        global real_time_line
        global real_time_line1
        global min_path_time
        global min_real_path_list
        global real_next_station
        global real_next_station1
        global min_path_trans_cnt
        global min_path_msg
        global arrive_tag
        global left_tag
        global last_time
        global found
        global found1
        global time_tag
        global min_joined_train_num_list
        global min_path_list
        global min_joined_time_table_list
        arrive_tag = 0
        time_tag = 0
        left_tag = 0
        global found_cnt
        print('get요청? in min')

        form = RouteForm()

        # 1호선 K 로 시작하는 열차번호 처리
        for item in min_joined_train_num_list:
            if item.startswith('K'):
                item.replace('K', '0')

        # 서울시 지하철 실시간 열차 위치정보 http://data.seoul.go.kr/dataList/OA-12601/A/1/datasetView.do

        # 선택 시간 받아오기 GET 요청
        selected_time = request.GET.get('time_drop_list')
        print('선택된 시간', selected_time)
        if selected_time == 'first':
            time_tag = 0
            print('first selected')
        elif selected_time == 'second':
            time_tag = 1
        elif selected_time == 'third':
            time_tag = 2
        # elif selected_time == 'last':
        #    time_tag = -1

        real_time_url = 'http://swopenAPI.seoul.go.kr/api/subway/' + \
            path_key+'/json/realtimePosition/0/100/'+temp_line
        real_time_response = requests.get(real_time_url)
        real_time_resdata = real_time_response.text
        real_time_obj = json.loads(real_time_resdata)
        try:
            real_time_obj = real_time_obj['realtimePositionList']
        except KeyError:
            print('KEY ERROR')
            return render(request, 'real_min.html', {'left_tag': left_tag, 'last_time': last_time, 'arrive_tag': arrive_tag, 'real_next_station': real_next_station, 'real_time_line': real_time_line, 'min_joined_time_table_list': min_joined_time_table_list, 'real_time_position': real_time_position, 'destword': destword})

        # print(real_time_obj)

       # try:
        for item in real_time_obj:

            if min_joined_train_num_list[0+time_tag] == item.get('trainNo'):
                print(item.get('trainNo'))
                real_time_line = item.get('subwayNm')
                real_time_position = item.get('statnNm')
                print(real_time_position)
                if real_time_position == destword:
                    break

        # except AttributeError:
        #    print('AttributeError')
        # xcept IndexError:
        #    print('minIndexError')

        if real_time_position == '공릉(서울산업대입구)':
            real_time_position = '공릉'

        print(real_time_position)
        print(destword)

        # 환승1회 후 실시간 열차 정보

        # 현재 역 다음 역 찾기.
        # 지하철 경로 조회 서비스 https://devming.tistory.com/214 |http://swopenAPI.seoul.go.kr/api/subway/인증Key값/요청데이터형식/OpenAPI 이름(서비스명)/요청 데이터 행 시작번호/요청 데이터 행 끝번호/출발역명/도착역명

        path_api_url = 'http://swopenAPI.seoul.go.kr/api/subway/'+key_num + \
            '/json/shortestRoute/0/5/'+real_time_position+'/'+destword
        path_response = requests.get(path_api_url)
        path_resdata = path_response.text
        path_obj = json.loads(path_resdata)
        try:
            path_obj = path_obj['shortestRouteList']
        except KeyError:
            print("keyerror")
            send_notification(resgistration, 'Notty 알림', '목적지에 도착했습니다.')
            return render(request, 'arrive.html', {'left_tag': left_tag, 'last_time': last_time, 'arrive_tag': arrive_tag, 'real_next_station': real_next_station, 'real_time_line': real_time_line, 'min_joined_time_table_list': min_joined_time_table_list, 'real_time_position': real_time_position, 'destword': destword})

        # 최단 시간 찾기
        path_time = [9999, 9999, 9999, 9999,
                     9999, 9999, 9999, 9999, 9999, 9999]

        i = 0
        try:
            for time_set in path_obj:
                path_time[i] = int(time_set.get('minTravelTm'))
                i = i+1
        except AttributeError:
            print("AttributeError")
        min_min_path_time = min(path_time)

        try:
            for item in path_obj:
                min_real_path_list = item.get('minStatnNm')
                # min_path_msg = item.get('minTravelMsg') 실시간 기반 소요 시간 환승 횟수 메시지
                # min_path_trans_cnt = item.get('minTransferCnt') 실시간 기반 환승 횟수
                # min_path_time = item.get('minTravelTm') 실시간 기반 소요 시간
                if min_min_path_time == int(item.get('minTravelTm')):
                    break
        except AttributeError:
            print('AttributeError')
        print(min_real_path_list)

        try:
            min_real_path_list = min_real_path_list.replace(" ", "")
            min_real_path_list = min_real_path_list.split(',')
        except AttributeError:
            print('Attribute Error')
        try:
            print(min_path_time)
            found = min_real_path_list.index(min_path_list[0])
        except ValueError:
            print('valueError')
            found = 0

        if found_cnt == 0:
            if real_time_position == min_real_path_list[found]:
                left_tag = 1
                found_cnt = 1
            elif real_time_position == min_real_path_list[found-1]:
                left_tag = 2
            elif real_time_position == min_real_path_list[found-2]:
                left_tag = 3
            elif real_time_position == min_real_path_list[found-3]:
                left_tag = 4
            else:
                print('출발 태그 예외')
                left_tag = 99
        else:
            print('출발 태그 예외')
            left_tag = 99

            global notification_cnt
            resgistration = [user_token]
            print(min_real_path_list)
            print(real_time_position)
            if real_time_position == min_real_path_list[-2]:
                arrive_tag = 1
                if notification_cnt == 2:
                    send_notification(
                        resgistration, 'Notty 알림', '목적지에 도착했습니다.')
                print('도착역 도착')

            elif real_time_position == min_real_path_list[-3]:
                arrive_tag = 2
                print('도착역 전 역 도착')
                if notification_cnt == 1:
                    send_notification(resgistration, 'Notty 알림',
                                      '전 역에 도착했습니다. 내릴 준비 해주세요.')
                    notification_cnt += 1

            elif real_time_position == min_real_path_list[-4]:
                arrive_tag = 3
                print('도착역 전전역 도착')
                if notification_cnt == 0:
                    send_notification(resgistration, 'Notty 알림',
                                      '전전 역에 도착했습니다. 내릴 준비 해주세요.')
                    notification_cnt += 1
            else:
                print("도착 태그 예외")
            # 실시간 다음역 지정
            real_next_station = min_real_path_list[1]

    return render(request, 'real_min.html', {'left_tag': left_tag, 'last_time': last_time, 'arrive_tag': arrive_tag, 'real_next_station': real_next_station, 'real_time_line': real_time_line, 'min_joined_time_table_list': min_joined_time_table_list, 'real_time_position': real_time_position, 'destword': destword})


def arrive(request):

    return render(request, 'arrive.html')


def send_notification(registration_ids, message_title, message_desc):
    fcm_api = "AAAAPLVafOQ:APA91bFrZ6r2uS5HOx6AqptsohWyq1-UBI6jNhLAoWisYhHkrQa4we6-Q8vUxbd8BxA-Wtz23R7KBKX4_QEVKpsovnOVJUJC6DpTcUQVMmRR_8fKGZjGgS0uqS0OeZUT2J2asE9w4gyj"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids": registration_ids,
        "priority": "high",
        "notification": {
            "body": message_desc,
            "title": message_title,
            "image": "https://i.postimg.cc/mrbjrC8z/hqdefault.jpg",
            "icon": "https://i.postimg.cc/jqJFm69t/Group-1.png",

        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers)
    # print(result.json())


def send(request):
    global user_token

    resgistration = [user_token]
    time.sleep(1)

    send_notification(
        resgistration, 'Code Keen added a new video', 'Code Keen new video alert')
    return HttpResponse("sent")


def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
        'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
        'var firebaseConfig = {' \
        '        apiKey: "AIzaSyB7kDt6u_8oVS_IjV_dYq8GmthV8x9n3kU",' \
        '        authDomain: "notty-34ee7.firebaseapp.com",' \
        '        databaseURL: "https://notty-34ee7.firebaseio.com",' \
        '        projectId: "notty-34ee7",' \
        '        storageBucket: "notty-34ee7.appspot.com",' \
        '        messagingSenderId: "260740644068",' \
        '        appId: "1:260740644068:web:2ede7cab29eae48e9740f1",' \
        '        measurementId: "G-3VT1R1RFGL"' \
        ' };' \
        'firebase.initializeApp(firebaseConfig);' \
        'const messaging=firebase.messaging();' \
        'messaging.setBackgroundMessageHandler(function (payload) {' \
        '    console.log(payload);' \
        '    const notification=JSON.parse(payload);' \
        '    const notificationOption={' \
        '        body:notification.body,' \
        '        icon:notification.icon' \
        '    };' \
        '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
        '});'
    return HttpResponse(data, content_type="text/javascript")


def showFirebaseJS2(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
        'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
        'var firebaseConfig = {' \
        '        apiKey: "AIzaSyB7kDt6u_8oVS_IjV_dYq8GmthV8x9n3kU",' \
        '        authDomain: "notty-34ee7.firebaseapp.com",' \
        '        databaseURL: "https://notty-34ee7.firebaseio.com",' \
        '        projectId: "notty-34ee7",' \
        '        storageBucket: "notty-34ee7.appspot.com",' \
        '        messagingSenderId: "260740644068",' \
        '        appId: "1:260740644068:web:2ede7cab29eae48e9740f1",' \
        '        measurementId: "G-3VT1R1RFGL"' \
        ' };' \
        'firebase.initializeApp(firebaseConfig);' \
        'const messaging=firebase.messaging();' \
        'messaging.onMessage(function (payload) {' \
        '    console.log(payload);' \
        '    const notification=JSON.parse(payload);' \
        '    const notificationOption={' \
        '        body:notification.body,' \
        '        icon:notification.icon' \
        '    };' \
        '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
        '});'

    return HttpResponse(data, content_type="text/javascript")


def holiday(today_year):

    # https://www.data.go.kr/data/15012690/openapi.do

    key = 'oTsloDJ6xmHymJiItQxmn1GEp2HiiX%2B8fA%2BH6PRKbCUp3XWPNEAViCpeWOir0YPCRpFHH3XQ6i6PlYwNdEg4dQ%3D%3D'
    url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?_type=json&numOfRows=50&solYear=' + \
        str(today_year) + '&ServiceKey=' + str(key)
    response = requests.get(url)
    if response.status_code == 200:
        holidays_resdata = response.text
        holiday_obj = json.loads(holidays_resdata)
    holiday_obj = holiday_obj['response']
    holiday_obj = holiday_obj['body']
    holiday_obj = holiday_obj['items']
    holiday_obj = holiday_obj['item']

    holiday_list = []
    for item in holiday_obj:
        holiday_list += str(item.get('locdate'))
        holiday_list += ','
    joined_holiday_list = " ".join(holiday_list)
    joined_holiday_list = joined_holiday_list.replace(" ", "")
    joined_holiday_list = joined_holiday_list.split(',')
    joined_holiday_list = [v for v in joined_holiday_list if v]

    holidate = joined_holiday_list

    return holidate
