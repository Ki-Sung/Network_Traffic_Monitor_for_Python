# 네트워크 인터페이스별 사용량 트래픽 모니터링 

# 0. 필요 라이브러리 불러오기 
import psutil  # 파이썬을 위한 실행중인 프로세스 및 시스템 리소스 및 정보 검색을 위한 크로스 플랫폼 라이브러리
import time  # 시간 라이브러리 
import os  # 운영체제에서 제공되는 여러 기능을 파이썬에서 수행시켜주는 라이브러리 
import pandas as pd # 판다스 라이브러리 

# 1. 바이트를 nice한 현식으로 출력하는 함수 반들기 
UPDATE_DELAY = 1 # in seconds

def get_size(bytes):
    """
    Returns size of bytes in a nice format 
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:        # IEC prefix names 기반 표기 기준 1 KiB = 1024 bytes
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024
        
# psutil에서 각 네트워크 인터페이스별 I/O(입출력) 통계 가져오기 
io = psutil.net_io_counters(pernic=True) # 'pernic'을 True로 설정 

# 2. 다운로드 및 업로드 속도 계산하고 실시간 네트워크 사용량 출력 
while True:
    # 'UPDATE_DELAY' time.sleep 
    time.sleep(UPDATE_DELAY)
    
    # 각 네트워크 인터페이스별 I/O(입출력) 통계 다시 가져오기
    io_2 = psutil.net_io_counters(pernic=True)
    
    # 수집할 데이터 초기화(딕셔너리 목록)
    data = []
    for iface, iface_io in io.items():
        # 새로운 통계 - 이전에 선언한 통계
        upload_speed, download_speed = io_2[iface].bytes_sent - iface_io.bytes_sent, io_2[iface].bytes_recv - iface_io.bytes_recv
        data.append({
            "iface": iface, "Download": get_size(io_2[iface].bytes_recv),
            "Upload": get_size(io_2[iface].bytes_sent),
            "Upload Speed": f"{get_size(upload_speed / UPDATE_DELAY)}/s",
            "Download Speed": f"{get_size(download_speed / UPDATE_DELAY)}/s",
        })
        
    # 다음 반복을 위해 I/O 통계 업데이트 
    io = io_2
    
    # 통계를 표 스타일로 출력하기 위해 Pandas DataFrame사용 
    df = pd.DataFrame(data)
    
    # 다운로드 기준, 원본 대체, 내림차순으로 정렬 
    df.sort_values("Download", inplace=True, ascending=False)
    
    # OS에 따라 화면 지우기 
    os.system("cls") if "nt" in os.name else os.system("clear")
    
    # 최종 통계 출력 
    print(df.to_string())
