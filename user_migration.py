import datetime
import json
import struct
import pyodbc

server = 'DESKTOP-DT213HN\MSSQLSERVER01'
database = 'mflex_dev'
username = 'Sinergia'
password = 'sinergia@123'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
user_list=[]

def handle_datetimeoffset(dto_value):
    tup = struct.unpack("<6hI2h", dto_value) 
    return datetime(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6] // 1000,
                    datetime.timezone(datetime.timedelta(hours=tup[7], minutes=tup[8])))
cursor = cnxn.cursor()
cnxn.add_output_converter(-155, handle_datetimeoffset)
users=cursor.execute("select * from dbo.AspNetUsers")
print(repr(users))
for i in users:
    user_list.append({
        "user_id":str(i[0]),
        "email":i[1],
        "given_name":i[18],
        "name":i[12],
        "custom_password_hash": {
            "algorithm":"bcrypt",
            "hash": {
                "value": "$2a$10$aHF7mbpWT6tZ7PJVtwtjNelaKbszikcYBCB2jibvbFcGFmOsu/s4K"
            }
        }
        
    })
filename="./users_list.json"
with open(filename, 'w') as json_file:
    json.dump(user_list, json_file, 
                        indent=4,  
                        separators=(',',': '))

    
