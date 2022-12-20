import requests
import time
import random
from tqdm import tqdm
import threading
from datetime import datetime
import pandas as pd

baseURL = "http://127.0.0.1:8866"

# tracker[datetime] = [trigger size, trigger ddl, total delay]
tracker = {}

random.seed(100)


def get_now():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if tracker.get(now) is None:
        tracker[now] = [0, 0, 0]
    return now


def send(now):
    start_time = time.time()
    req = requests.post(baseURL + "/iot_anomaly_detection", json={
        "data": [random.random() for _ in range(152)],
    })
    delay = time.time() - start_time
    delays.append(delay)
    if req.status_code == 200:
        tracker[now][int(req.json()["type"]) - 1] += 1
        tracker[now][2] += delay
    else:
        print("req error with", req.status_code)


delays = []

for i in tqdm(range(50), desc="50 ms"):
    now = get_now()
    task = threading.Thread(target=send, args=(now,))
    task.start()
    time.sleep(0.05)

for i in tqdm(range(10), desc="0 - 3000 ms, Small Variance"):
    now = get_now()
    task = threading.Thread(target=send, args=(now,))
    task.start()
    time.sleep(random.random() * 3)


for i in tqdm(range(30), desc="100 - 150 ms"):
    now = get_now()
    task = threading.Thread(target=send, args=(now,))
    task.start()
    time.sleep(0.1 + random.random() / 20)


for i in tqdm(range(30), desc="200 - 250 ms"):
    now = get_now()
    task = threading.Thread(target=send, args=(now,))
    task.start()
    time.sleep(0.2 + random.random() / 20)


for i in tqdm(range(10), desc="0 - 3000 ms, Large Variance"):
    now = get_now()
    task = threading.Thread(target=send, args=(now,))
    task.start()
    time.sleep(random.random() * random.randint(1, 3))


print("总体平均时延：", round(1000*sum(delays) / len(delays)), "ms")

result = pd.DataFrame(tracker).T.reset_index().rename(
    columns={'index': 'time', 0: 'size', 1: 'limit', 2:'delay_sum'})
result.to_csv("logs/fixed-logs.csv")
