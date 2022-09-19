import pyodbc
import json

import datetime
import struct

server = 'DESKTOP-DT213HN\MSSQLSERVER01'
database = 'mflivedbprod'
username = 'Sinergia'
password = 'sinergia@123'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

def handle_datetimeoffset(dto_value):
    tup = struct.unpack("<6hI2h", dto_value) 
    return datetime(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6] // 1000,
                    datetime.timezone(datetime.timedelta(hours=tup[7], minutes=tup[8])))
cursor = cnxn.cursor()
cnxn.add_output_converter(-155, handle_datetimeoffset)
cursor.execute("SELECT * FROM dbo.AspNetUsers")
rows = cursor.fetchall()
rowarray_list = []

# for row in rows:
#     t = (row[0], row[1], row[2], row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[20],row[21],row[23],row[24],row[25],row[26],row[27])
#     rowarray_list.append(t)

# print(rowarray_list,"\n")
# j = json.dumps(rowarray_list)
# with open("users.json", "w") as f:
#     f.write(j)
# Convert query to objects of key-value pairs
objects_list = []
for row in rows:
    # d = collections.OrderedDict()
    d={
        "Id": row[0],
        "Email" : row[1],
        "EmailConfirmed" :row[2],
        "CountryCode" : row[5],
        "PhoneNumber" : row[6],
        "PhoneNumberConfirmed" : row[7],
        "IsAdmin" :row[13],
        "IsSMSEnabled" : row[14],
        "IsEmailEnabled" : row[15],
        "AccountId" : row[17],
        "FirstName" : row[18],
        "LastName" : row[19],
        "IsDeactivated" : row[20],
        "Country" : row[21]


     }

    objects_list.append(d)
j = json.dumps(objects_list)
with open("users.json", "w") as f:
    f.write(j)

cnxn.close()