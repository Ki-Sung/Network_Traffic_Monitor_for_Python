# 총 네트워크 사용량 트래픽 모니터 

# 0. 필요 라이브러리 불러오기 
import psutil  # 파이썬을 위한 실행중인 프로세스 및 시스템 리소스 및 정보 검색을 위한 크로스 플랫폼 라이브러리
import time   # 시간 라이브러리 

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

# 2. psutil에서 네트워크 I/O(입출력) 통계 가져오기 
io = psutil.net_io_counters() 

# 전송 및 수신된 총 바이트 추출 
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv

# 3. 다운로드 및 업로드 속도 계산하고 실시간 네트워크 사용량 출력 
while True:
    # 'UPDATE_DELAY' time.sleep 
    time.sleep(UPDATE_DELAY)
    
    # 통계 다시 가져오기 
    io_2 = psutil.net_io_counters()
    
    # 속도 측정 
    # 새로운 통계(io_2.bytes_sent, io_2.bytes_recv) - 이전에 선언한 통계(bytes_sent, bytes_recv) 
    us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
    
    #  현재 속도와 같이 총 다운로드 / 업로드 출력
    print(f"Upload: {get_size(io_2.bytes_sent)}    "
          f", Download: {get_size(io_2.bytes_recv)}    "
          f", Upload Speed: {get_size(us / UPDATE_DELAY)}/s    "
          f", Download Speed: {get_size(ds / UPDATE_DELAY)}/s   ", end="\r")
    
    # 다음 반복을 위해 bytes_sent 및 bytes_recv 업데이트 
    bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv