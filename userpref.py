import pyodbc
import json

server = 'DESKTOP-DT213HN\MSSQLSERVER01'
database = 'mflivedbprod'
username = 'Sinergia'
password = 'sinergia@123'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
def handle_datetimeoffset(dto_value):
    tup = struct.unpack("<6hI2h", dto_value) 
    return datetime(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6] // 1000,
                    datetime.timezone(datetime.timedelta(hours=tup[7], minutes=tup[8])))
cnxn.add_output_converter(-155, handle_datetimeoffset)
cursor.execute("SELECT * FROM dbo.UserPreference")
rows = cursor.fetchall()
# Convert query to objects of key-value pairs
objects_list = []
for row in rows:
    d={
    "Id":row[0],
    "UserId" : row[1],
    "DataTypeName" : row[2],
    "UoMId" : row[3],
    "CreatedBy": row[4],
    "CreatedAt":row[5],
    "ModifiedBy":row[6],
    "ModifiedAt":row[7]
    }
    
    objects_list.append(d)
j = json.dumps(objects_list,indent=4, sort_keys=True, default=str)
with open("userpref.json", "w") as f:
    f.write(j)

cnxn.close()