import time
from datetime import datetime,timedelta
from plyer import notification



def drinking_assistant(interval,duration):
    start_time = datetime.now()
    end_time = start_time + timedelta(hours = duration)

    while datetime.now() < end_time:
        print(datetime.now())
        notification.notify(
            title = "你最好是能喝水",
            message = "一次喝100ml！",
            app_name = "喝水小助手",
            timeout = 20
        )
        time.sleep(interval)



if __name__ == "__main__":
    drinking_assistant(interval=1200,duration=5)

