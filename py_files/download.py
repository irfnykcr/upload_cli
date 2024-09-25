from json import load
import requests
from sys import argv
from threading import Thread 
from time import perf_counter_ns, sleep

print("starting..")

WEBURL = argv[1]
OUTDIR = fr"{argv[2]}"
with open(r"./config/config.json", "r") as f:
	j = load(f)
	UNIQUE_KEY = j['api_key']
	MAX_THREADS = j['max_threads'] # ±1
THREADS_NOW = 0

def getfile_info():
	global WEBURL
	global UNIQUE_KEY
	r = requests.post(f"https://api.turkuazz.online/v1/download/getfile_info", headers={"api-key":UNIQUE_KEY}, json={"weburl":WEBURL})
	if r.status_code != 200:
		return False, r.content
	return eval(r.content)

file_info = getfile_info()
if file_info[0] == False:
	print(f"something went wrong while getting file info! {file_info[1]}")
	exit()
NAME = file_info[0]
URLS = eval(file_info[1])
TOTAL = len(URLS)
def download_chunk(url, n):
	global UNIQUE_KEY
	global DONE
	global TOTAL
	try:
		print(f"+ {n}")
		r = requests.post(f"https://api.turkuazz.online/v1/download/get_chunk", headers={"api-key":UNIQUE_KEY}, json={"url":url})
		data = r.content
		if r.status_code != 200:
			return download_chunk(url, n)
		DATALIST.append((n,data))
		DONE+=1
		up_s = round(DONE/((perf_counter_ns()/10e8)-TIME_STARTED), 2)
		print(f"- {n} --:: downloaded {round((DONE/TOTAL)*100,2)}% --:: {DONE}/{TOTAL} --:: {up_s}up/s --:: kalan ~= {round(((TOTAL-DONE)/up_s)/60, 2)}dk")
		return data
	except Exception as e:
		print(f"something went wrong with {n}, will try again in 5sec", e)
		sleep(5)
		return download_chunk(url, n)

threads = []
n = 0
for url in URLS:
	n+=1
	threads.append(Thread(target=download_chunk, args=(url, n)))

n = 0
DONE = 0
DATALIST = []
STARTED_THREAD = []
print("starting threads..")
TIME_STARTED = perf_counter_ns()/10e8

def write_downloaded():
	global STARTED_THREAD
	global DATALIST
	global WEBURL
	global NAME
	STARTED_THREAD = []
	DATALIST.sort(key=lambda x: x[0])
	with open(fr"{OUTDIR}/{WEBURL}.{NAME}", "ab") as f:
		for data in DATALIST:
			print(f"~ writing: {data[0]}")
			f.write(data[1])
	DATALIST = []

for t in threads:
	n+=1
	t.start()
	STARTED_THREAD.append(t)
	if n % MAX_THREADS == 0:
		for th in STARTED_THREAD:
			th.join()
		write_downloaded()

print("finishing last ones..")

for th in STARTED_THREAD:
	th.join()
write_downloaded()

print("all is okay!")