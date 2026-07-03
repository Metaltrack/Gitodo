from datetime import datetime
import json

class log_level:
    INFO :str = "INFO"
    WARNING :str = "WARNING"
    ERROR :str = "ERROR"
    CRITICAL :str = "CRITICAL"

def log(level :log_level, file :str, msg :str):
    timestamp = datetime.now().isoformat()

    data = {
        "Level": level,
        "Time-Stamp": timestamp,
        "From-File": file,
        "Message": msg
    }

    print(data)
