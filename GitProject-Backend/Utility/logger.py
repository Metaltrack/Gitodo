from datetime import datetime
import sys
import threading

class log_level:
    INFO :str = "INFO"
    WARNING :str = "WARNING"
    ERROR :str = "ERROR"
    CRITICAL :str = "CRITICAL"

def log(level :log_level, file :str, msg :str):
    timestamp = datetime.now().isoformat()

    if(level == log_level.WARNING):
        print(f"\033[33m>>{level} |\033[0m At: {timestamp} \033[33m|\033[0m File: {file} \033[33m|\033[0m Msg: {msg} \033[33m|>\033[0m")
        return
    elif(level == log_level.ERROR):
        print(f"\033[31m>>{level} |\033[0m At: {timestamp} \033[31m|\033[0m File: {file} \033[31m|\033[0m Msg: {msg} \033[31m|>\033[0m")
        return
    elif(level == log_level.CRITICAL):
        print(f"\033[7m\e[31m>>{level} |\033[0m At: {timestamp} \033[7m|\033[0m File: {file} \033[7m|\033[0m Msg: {msg} \033[7m|>\033[0m")
        return

    print(f"\033[32m>>{level} |\033[0m At: {timestamp} \033[32m|\033[0m File: {file} \033[32m|\033[0m Msg: {msg} \033[32m|>\033[0m")
    return


