import os

apps = ['brand', 'LnF', 'map', 'user']

for app in apps:
    file_list = [file for file in os.listdir(app+'/migrations') if file.endswith(".py")]
    
    for f in file_list:
        if f =="__init__.py":
            continue
        else:
            os.remove(app+'/migrations/'+f)
    
    # print(file_list)

os.remove('db.sqlite3')
print("DB 초기화 완료")