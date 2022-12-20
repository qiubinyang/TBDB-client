import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

BASE_LOG_DIR = "logs/"

sns.set_style("whitegrid")
sns.set_context(context="paper", font_scale=3.0, rc={"lines.linewidth": 3})

data = pd.read_csv(BASE_LOG_DIR+"logs.csv")
data["total"] = data["size"] + data["limit"]
data["delay"] = data["delay_sum"] / data["total"]

fixed_data = pd.read_csv(BASE_LOG_DIR+"fixed-logs.csv")
fixed_data["total"] = fixed_data["size"] + fixed_data["limit"]
fixed_data["delay"] = fixed_data["delay_sum"] / fixed_data["total"]

plt.figure(figsize=(15, 12))
plt.subplots_adjust(hspace=0.5)

# --- Trigger Type ---
plt.subplot(3,1,1)
plt.title("Fixed batch trigger type")
sns.barplot(x=fixed_data.index, y="total", data=fixed_data, color="blue", label="trigger batch size")
bar_fixed = sns.barplot(x=fixed_data.index, y="limit", data=fixed_data, color="gray", label="trigger time limit")
bar_fixed.set_xlabel(None)
plt.xticks([0,20,40,60,80,100,120,140,160],[0,20,40,60,80,100,120,140,160])
f = plt.Rectangle((0, 0), 1, 1, fc="blue", edgecolor='none')
d = plt.Rectangle((0, 0), 1, 1, fc="gray", edgecolor='none')
l = plt.legend([f, d], ['MBS', 'MBT'],
                loc=1, ncol=2, prop={'size': 20})
l.draw_frame(False)

plt.subplot(3,1,2)
plt.title("Dynamic batch trigger type")
sns.barplot(x=data.index, y="total", data=data, color="blue", label="trigger batch size")
bar = sns.barplot(x=data.index, y="limit", data=data, color="gray", label="trigger time limit")
bar.set_xlabel(None)
plt.xticks([0,20,40,60,80,100,120,140,160],[0,20,40,60,80,100,120,140,160])
f = plt.Rectangle((0, 0), 1, 1, fc="blue", edgecolor='none')
d = plt.Rectangle((0, 0), 1, 1, fc="gray", edgecolor='none')
l = plt.legend([f, d], ['MBS', 'MBT'],
                loc=1, ncol=2, prop={'size': 20})
l.draw_frame(False)

# --- Delay ---
plt.subplot(3,1,3)
plt.title("Average delay per request")
sns.lineplot(x=fixed_data.index, y="delay", data=fixed_data, color="red", label="Fixed Batch")
cpu = sns.lineplot(x=data.index, y="delay", data=data, color="green", label="Dynamic Batch")
sns.despine()
cpu.set_ylabel("Average Delay")
cpu.set_xlabel("Log Time")
f = plt.Rectangle((0, 0), 1, 1, fc="red", edgecolor='none')
d = plt.Rectangle((0, 0), 1, 1, fc="green", edgecolor='none')
l = plt.legend([f, d], ['Fixed Batch', 'Dynamic Batch'],
                loc=1, ncol=2, prop={'size': 20})
l.draw_frame(False)

plt.savefig(BASE_LOG_DIR+"vis.png", dpi=200)
