# handleWorkData
Toggl APIに入力した勤怠データを加工/CSV出力する  
※ 日毎の項目: 勤務開始時間、勤務終了時間、休憩時間  

## 事前準備
env作成  
```
$ python3.8 -m venv env
$ . env/bin/activate
(env) $ pip install -r requirements.txt
```

conf追記  
```
(env) $ cp config.ini.template config.ini
```

## 使い方
```
$ python run.py (year) (month)
```
