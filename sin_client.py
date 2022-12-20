import requests
import time
import random
from tqdm import tqdm
import threading
from datetime import datetime
import pandas as pd
import math
import numpy as np

baseURL = "http://127.0.0.1:8866"
# name = "/iot_anomaly_detection"
# name = "/translate"
name = "/image_classify"

# tracker[datetime] = [trigger size, trigger ddl, total delay]
tracker = {}

random.seed(100)

# data = [random.random() for _ in range(152)]

data = np.load("test/mnist.npy").flatten().tolist()

# data = [4] * random.randint(20, 50)

def get_now():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if tracker.get(now) is None:
        tracker[now] = [0, 0, 0]
    return now


def send(now):
    start_time = time.time()
    req = requests.post(baseURL + name, json={
        "data": data
    })
    delay = time.time() - start_time
    delays.append(delay)
    if req.status_code == 200:
        tracker[now][int(req.json()["type"]) - 1] += 1
        tracker[now][2] += delay
    else:
        print("req error with", req.status_code)


def warm_up():
    requests.post(baseURL + name, json={
        "data": data
    })


# print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Warm Up")
# warm_up_task = []
# for _ in range(8):
#     task = threading.Thread(target=warm_up)
#     task.start()
#     warm_up_task.append(task)
#     time.sleep(0.5)
# [t.join() for t in warm_up_task]

# time.sleep(5)

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start to inference!")
delays = []

for i in tqdm(range(1000)):
    now = get_now()
    task = threading.Thread(target=send, args=(now,))
    task.start()
    interval_time = (1.5+math.sin((1/(10*math.pi))*i) +
                     random.uniform(-0.5, 0.5))/10
    time.sleep(interval_time)

print("总体平均时延：", round(1000*sum(delays) / len(delays)), "ms")

# requests.get(baseURL+"/stop_backend")

result = pd.DataFrame(tracker).T.reset_index().rename(
    columns={'index': 'time', 0: 'size', 1: 'limit', 2: 'delay_sum'})

# result.to_csv("high-logs/logs.csv")
# result.to_csv("high-logs/fixed-logs.csv")
