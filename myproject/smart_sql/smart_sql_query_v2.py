from openai import OpenAI
import sqlite3
# from faker import Faker
import random
import os
# import google_stt

client = OpenAI()

create_table_sql = '''
                    CREATE TABLE stillwater_inspections (
                        InspectionId INTEGER NOT NULL,
                        Surveyed_By TEXT,
                        Owner TEXT,
                        Customer TEXT,
                        Drainage_Area TEXT,
                        PO_Number TEXT,
                        Pipe_Segment_Reference TEXT,
                        Date DATE,
                        Time TIME,
                        Street TEXT,
                        City TEXT,
                        Location_Details TEXT,
                        Upstream_MH TEXT,
                        Up_Rim_to_Invert REAL,
                        Up_Grade_to_Invert REAL,
                        Up_Rim_to_Grade REAL,
                        Downstream_MH TEXT,
                        Down_Rim_to_Invert REAL,
                        Down_Grade_to_Invert REAL,
                        Down_Rim_to_Grade REAL,
                        Sewer_Use TEXT,
                        Direction TEXT,
                        Flow_Control TEXT,
                        Height SMALLINT,
                        Width SMALLINT,
                        Shape TEXT,
                        Material TEXT,
                        Lining_Method TEXT,
                        Pipe_Joint_Length REAL,
                        Total_Length REAL,
                        Length_Surveyed REAL,
                        Year_Laid SMALLINT,
                        Year_Renewed SMALLINT,
                        Media_Label TEXT,
                        Purpose TEXT,
                        Sewer_Category TEXT,
                        Pre_Cleaning TEXT,
                        Date_Cleaned DATETIME,
                        Weather TEXT,
                        Location_Code TEXT,
                        Additional_Info TEXT,
                        Reverse_Setup SMALLINT,
                        Sheet_Number SMALLINT,
                        IsImperial SMALLINT,
                        PressureValue REAL,
                        WorkOrder TEXT,
                        Project TEXT,
                        Northing TEXT,
                        Easting TEXT,
                        Elevation TEXT,
                        Coordinate_System TEXT,
                        GPS_Accuracy TEXT,
                        Organization TEXT,
                        Flag TINYINT NOT NULL
                    );
                    '''

data_to_insert = [
            (1,'John Huff',None,None,None,None,'742','2017-01-27','13:31:00.000000','#46 Yellowbrick','Stillwater',None,'2186',None,None,None,'2185',None,None,None,None,'D',None,None,None,'Round','VCP',None,None,369.900,369.900,None,None,None,'Sewer Call','WasteWater','Yes',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (2,None,None,None,None,None,None,'2017-01-27',None,None,'Stillwater',None,None,None,None,None,None,None,None,None,None,None,None,None,None,'Round',None,None,None,0.000,None,None,None,None,None,'WasteWater',None,None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (3,'John Huff',None,None,None,None,'1257','2017-01-06','13:44:51.000000','112 S. Melrose','Stillwater',None,'2617',None,None,None,'2616',None,None,None,None,'D',None,None,None,'Round','VCP',None,None,116.800,116.800,None,None,None,'Camera list','WasteWater','Yes',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (4,None,None,None,None,None,None,'2017-01-09',None,None,'Stillwater',None,None,None,None,None,None,None,None,None,None,None,None,None,None,'Round',None,None,None,0.000,None,None,None,None,None,'WasteWater',None,None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (5,'John Huff',None,None,None,None,None,'2017-01-06','09:56:31.000000','112 S. Melrose','Stillwater',None,'2616',None,None,None,'2617',None,None,None,None,'U',None,None,None,'Round','VCP',None,None,5.000,5.000,None,None,None,'Sewer Call','WasteWater','No',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (6,None,None,None,None,None,None,'2017-01-17',None,None,'Stillwater',None,None,None,None,None,None,None,None,None,None,None,None,None,None,'Round',None,None,None,0.000,None,None,None,None,None,'WasteWater',None,None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (7,'John Huff',None,None,None,None,'731','2017-01-17','09:07:38.000000','124 W. 6th','Stillwater',None,'208',None,None,None,'2689',None,None,None,None,'U',None,None,None,'Round','VCP',None,None,328.800,328.800,None,None,None,'Sewer Call','WasteWater','No',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (8,'John Huff',None,None,None,None,'1271','2017-01-05','11:49:25.000000','220 S. Cleveland','Stillwater',None,'2641',None,None,None,'2640',None,None,None,None,'U',None,None,None,'Round','VCP',None,None,26.600,26.600,None,None,None,'Camera list','WasteWater','No',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (9,'John Huff',None,None,None,None,'1271','2017-01-05','13:22:50.000000','220 S. Cleveland st','Stillwater',None,'2641',None,None,None,'2640',None,None,None,None,'U',None,None,None,'Round','VCP',None,None,106.300,106.300,None,None,None,'Sewer Call','WasteWater','No',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (10,None,None,None,None,None,None,'2017-01-12',None,None,'Stillwater',None,None,None,None,None,None,None,None,None,None,None,None,None,None,'Round',None,None,None,0.000,None,None,None,None,None,'WasteWater',None,None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (11,'John Huff',None,None,None,None,'1515','2017-01-19','14:37:22.000000','220 W. Cantwell','Stillwater',None,'1394',None,None,None,'5672',None,None,None,None,'D',None,None,None,'Round','VCP',None,None,46.000,46.000,None,None,None,'Camera list','WasteWater','No',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (12,None,None,None,None,None,None,'2017-01-18',None,None,'Stillwater',None,None,None,None,None,None,None,None,None,None,None,None,None,None,'Round',None,None,None,0.000,None,None,None,None,None,'WasteWater',None,None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (13,'John Huff',None,None,None,None,None,'2017-01-18','12:59:20.000000','323 S. Ramsey','Stillwater',None,'unknown LH',None,None,None,'3345',None,None,None,None,'U',None,None,None,'Round','VCP',None,None,92.600,92.600,None,None,None,'Sewer Call','WasteWater','No',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (14,'John Huff',None,None,None,None,'2406','2017-01-20','09:48:28.000000','409 S. Arington','Stillwater',None,'1936',None,None,None,'1935',None,None,None,None,'U',None,None,None,'Round','VCP',None,None,154.600,148.600,None,None,None,'Camera list','WasteWater','No',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (15,'John Huff',None,None,None,None,'2407','2017-01-20','10:41:11.000000','409 S. Arington','Stillwater',None,'1935',None,None,None,'419',None,None,None,None,'D',None,None,None,'Round','VCP',None,None,95.000,95.000,None,None,None,'Camera list','WasteWater','No',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (16,'John Huff',None,None,None,None,'627','2017-01-30','13:17:17.000000','416 W. 29th','Stillwater',None,'3020',None,None,None,'3022',None,None,None,None,'D',None,None,None,'Round','VCP',None,None,141.000,140.900,None,None,None,'gen. condition control','WasteWater','Root Cut',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (17,'John Huff',None,None,None,None,'628','2017-01-30','13:03:40.000000','416 W. 29th','Stillwater',None,'3021',None,None,None,'3020',None,None,None,None,'U',None,None,None,'Round','VCP',None,None,269.000,269.000,None,None,None,'gen. condition control','WasteWater','Root Cut',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (18,'John Huff',None,None,None,None,'1823','2017-01-30','10:44:08.000000','416 W. 29 th','Stillwater',None,'3017',None,None,None,'3018',None,None,None,None,'U',None,None,None,'Round','VCP',None,None,200.000,199.000,None,None,None,'gen. condition control','WasteWater','No',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (19,'John Huff',None,None,None,None,'625','2017-01-30','10:19:28.000000','416 W. 29th','Stillwater',None,'3018',None,None,None,'3019',None,None,None,None,'U',None,None,None,'Round','VCP',None,None,211.500,211.500,None,None,None,'SSO','WasteWater','No',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0),
            (20,'John Huff',None,None,None,None,'626','2017-01-30','11:06:58.000000','416 W. 29tj','Stillwater',None,'3019 ',None,None,None,'3020',None,None,None,None,'D',None,None,None,'Round','VCP',None,None,270.300,270.300,None,None,None,'gen. condition control','WasteWater','Root Cut',None,'Sunny, Dry',None,None,None,None,None,None,None,None,None,None,None,None,None,'Stillwater',0)        
            ]


def query_database(sql_cmd,database_name):
    conn = sqlite3.connect(database_name)
    #conn = mysql.connector.connect(user='root', password='123456',
    #                          host='localhost',
    #                          database='new_infratie', charset='utf8mb4', collation='utf8mb4_general_ci')
    print(conn)
    cursor = conn.cursor()

    cursor.execute(sql_cmd)
    rows = cursor.fetchall()
    column_names = ["InspectionId","Surveyed_By","Owner","Customer","Drainage_Area","PO_Number","Pipe_Segment_Reference","Date","Time","Street","City","Location_Details","Upstream_MH","Up_Rim_to_Invert","Up_Grade_to_Invert","Up_Rim_to_Grade","Downstream_MH","Down_Rim_to_Invert","Down_Grade_to_Invert","Down_Rim_to_Grade","Sewer_Use","Direction","Flow_Control","Height","Width","Shape","Material","Lining_Method","Pipe_Joint_Length","Total_Length","Length_Surveyed","Year_Laid","Year_Renewed","Media_Label","Purpose","Sewer_Category","Pre_Cleaning","Date_Cleaned","Weather","Location_Code","Additional_Info","Reverse_Setup","Sheet_Number","IsImperial","PressureValue","WorkOrder","Project","Northing","Easting","Elevation","Coordinate_System","GPS_Accuracy","Organization","Flag"]

    # print(" | ".join(column_names))
    # print("\n")
    res = []
    for row in rows:
        formatted_row = " | ".join(str(value) for value in row)
        print(formatted_row)
        res.append(formatted_row)
        # print("\n")

    conn.close()

    return res




def query_chatgpt(user_input):
    completion = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {"role": "system", "content": "You need to purely generate SQL code for me to query my database. The database was created using the code: "+ create_table_sql + " There are some example data: "+ str(data_to_insert) +" Please just give me the SQL code. No other words"},
        {"role": "user", "content": user_input}
    ]
    )
    out = completion.choices[0].message.content.replace("sql","").replace("```","")
    print(out)
    print("\n")
    return out








# user_input = google_stt.main()

def query_demo(input = None):

    print("please say your query...\n")
    # user_input = input("")
    user_input = "show me all the tables"
    if input != None:
        user_input = input

    data_base_name = 'inspections.db'
    data_base_name = '/home/ascc/LF_Workspace/project_shan/myproject/smart_sql/inspections.db'
    sql_code = query_chatgpt(user_input)
    res = query_database(sql_code,data_base_name)
    return res

# conda activate gym
# query_demo("Supposing today is January 30 2017. Shom me the inspections that we did within one week.")

# Supposing today is January 30 2017. Shom me the inspections that we did within one week.
# When was the last inspection carried out?
# Who did the inspection last time?
# How many times has the person who conducted the last inspection conducted inspections?

#export GOOGLE_APPLICATION_CREDENTIALS="/Users/zhidongsu/Documents/RL_bot_dialog/new-project-2021-07-28-a5bdb4508c2c_1.json"
#export OPENAI_API_KEY='sk-xxx'




