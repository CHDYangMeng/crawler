
from datetime import date, time, datetime, timedelta

def get_data():
    print("123")

def runTask():
    # Init time
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    print("now:", strnow)

    period = timedelta(seconds=5)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    print("next run:", strnext_time)
    while True:
        # Get system current time
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            # Get every start work time
            print("start work: %s" % iter_now_time)
            get_data()
            print("task done.")
            # Get next iteration time
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            print("next_iter: %s" % strnext_time)
            # Continue next iteration
            continue

if __name__ == '__main__':
    runTask()