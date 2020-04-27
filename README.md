# handleWorkData
Toggl APIに入力した勤怠データを加工/CSV出力する  
※ 日毎の項目: 勤務開始時間、勤務終了時間、休憩時間  

## 事前準備
env作成  
```
$ python3.8 -m venv env
$ . env/bin/activate
```

conf追記  
```
$ cp config.ini.template config.ini
```

## 使い方
```
$ python run.py (year) (month)
```

## Todo
* 勤務がない日を補完する  
* 1日の区切り時間を指定できるようにする（今は0:00固定）  
* Work Project指定あり・なしで抽出できるようにする   
* Click Help書く  
* 今月の勤務時間合計を出すコマンド作成  
