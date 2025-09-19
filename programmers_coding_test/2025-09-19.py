#1 
from typing import Tuple

def prev_pos(current_pos: Tuple[int, int])-> Tuple[int, int]:
    if current_pos[1] >= 10:
        current_pos[1] -= 10
    elif current_pos[1] < 10:
        current_pos[0] -= 1
        current_pos[1] = current_pos[1] + 60 - 10
        
    if current_pos[0] < 0 or (current_pos[0] == 0 and current_pos[1] < 0):
        current_pos[0] = 0
        current_pos[1] = 0
    return current_pos

def next_pos(current_pos: Tuple[int, int], op_end: str)-> Tuple[int, int]:
    current_pos[1] += 10
    
    if current_pos[1] > 59:
        current_pos[0] += 1
        current_pos[1] = 0
        
    end_hour, end_minutes = get_int_time(op_end)
    
    if current_pos[0] > end_hour or (current_pos[0] == end_hour and current_pos[1] > end_minutes):
        current_pos[0] = end_hour
        current_pos[1] = end_minutes
    
    return current_pos

def skip_opening(current_pos: Tuple[int, int], op_start: str, op_end: str)-> Tuple[int, int]:
    start_time = get_int_time(op_start)
    end_time = get_int_time(op_end)
    
    start_total_time = start_time[0] * 60 + start_time[1]
    end_total_time = end_time[0] * 60 + end_time[1]
    current_total_time = current_pos[0] * 60 + current_pos[1]
    
    if start_total_time <= current_total_time and current_total_time <= end_total_time:
        current_pos = [end_time[0], end_time[1]]
    return current_pos
def get_str_time(current_pos: Tuple[int, int] )-> str:

    
    hour = str(current_pos[0])
    minute = str(current_pos[1])
    if len(hour) == 1:
        hour = f'0{hour}'
    if len(minute) == 1:
        minute = f'0{minute}'
    return f'{hour}:{minute}'

def get_int_time(time: str)-> Tuple[int, int]:
    return [int(time[:2]), int(time[3:5])]

def solution(video_len, pos, op_start, op_end, commands):
    answer = ''
    
    current_pos = get_int_time(pos)

    for command in commands:
        current_pos = skip_opening(current_pos, op_start, op_end)
        
        if command == 'next':
            current_pos = next_pos(current_pos, video_len)
        elif command == 'prev':
            current_pos = prev_pos(current_pos)
    
    current_pos = skip_opening(current_pos, op_start, op_end)
    answer = get_str_time(current_pos)
    
    return answer

# 2 seconds 통일 버전

from typing import Tuple

def prev_pos(current_pos: int)-> int:
    current_pos -= 10
    if current_pos < 0:
        current_pos = 0
    return current_pos

def next_pos(current_pos: int, video_length: str)-> int:
    current_pos += 10
    video_end = get_int_time(video_length)
    
    if current_pos > video_end:
        current_pos = video_end
    
    return current_pos

def skip_opening(current_pos: int, op_start: str, op_end: str)-> Tuple[int, int]:
    start_time = get_int_time(op_start)
    end_time = get_int_time(op_end)
    
    if start_time <= current_pos and current_pos <= end_time:
        current_pos = end_time
    return current_pos

def get_str_time(current_pos: int)-> str:
    hour = str(current_pos // 60)
    minute = str(current_pos % 60)
    if len(hour) == 1:
        hour = f'0{hour}'
    if len(minute) == 1:
        minute = f'0{minute}'
    return f'{hour}:{minute}'

def get_int_time(time: str)-> int:
    return int(time[:2]) * 60 +  int(time[3:5])

def solution(video_len, pos, op_start, op_end, commands):
    answer = ''
    
    current_pos = get_int_time(pos)

    for command in commands:
        current_pos = skip_opening(current_pos, op_start, op_end)
        
        if command == 'next':
            current_pos = next_pos(current_pos, video_len)
        elif command == 'prev':
            current_pos = prev_pos(current_pos)
    
    current_pos = skip_opening(current_pos, op_start, op_end)
    answer = get_str_time(current_pos)
    
    return answer

# prev => 10초 전 이동, 10초 미만 남았을 시 처음 위치 이동
# next => 10초 후 이동, 10초 미만 남았을 시 마지막 위치 이동 
# 오프닝 건너뛰기 => 최종 루프 이후 위치를 파악해야함
    # 전체 명령 수행 이후 최종 결과를 반환

# 로직
# 1. pos int 로 환산 
# 2. commands 수행 
# 3. 최종 점검(오프닝 건너뛰기)

# 3
# 시간 변환
def get_int_time(time: str) -> int:
    return int(time[:2]) * 60 + int(time[3:5])

def get_str_time(current_pos: int) -> str:
    # 나누기와 몫 둘다 필요시 
    minutes, seconds = divmod(current_pos, 60)
    # f-string 포매팅 적용
    return f'{minutes:02d}:{seconds:02d}'

def solution(video_len, pos, op_start, op_end, commands):
    # 쓸거니깐 미리 변환 다해두기
    video_len_sec = get_int_time(video_len)
    op_start_sec = get_int_time(op_start)
    op_end_sec = get_int_time(op_end)
    current_pos_sec = get_int_time(pos)
    
    # 오프닝 스킵을 위한 헬퍼, 내부의 변수들 접근, 굳이 외부 함수로 뺄 필요 없으니 
    # 내부 함수 => 해당 함수 내부의 변수들 접근 용이
    def check_and_skip_opening(pos_sec: int) -> int:
        if op_start_sec <= pos_sec <= op_end_sec:
            return op_end_sec
        return pos_sec
    
    current_pos_sec = check_and_skip_opening(current_pos_sec)
    
    for command in commands:
        if command == 'next':
            current_pos_sec = min(video_len_sec, current_pos_sec + 10)
        elif command == 'prev':
            current_pos_sec = max(0, current_pos_sec - 10)
    
        current_pos_sec = check_and_skip_opening(current_pos_sec)
    
    return get_str_time(current_pos_sec)