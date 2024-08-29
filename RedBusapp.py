# importing libraries
import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu
import time

# kerala bus
lists_k=[]
df_k=pd.read_csv("Bus_Routes.csv")
for i,r in df_k.iterrows():
    lists_k.append(r["Route Name"])

#Andhra bus
lists_A=[]
df_A=pd.read_csv("Red_Bus_A.csv")
for i,r in df_A.iterrows():
    lists_A.append(r["Route Name"])

#Telungana bus
lists_T=[]
df_T=pd.read_csv("Red_Bus_T.csv")
for i,r in df_T.iterrows():
    lists_T.append(r["Route Name"])

#Goa bus
lists_g=[]
df_G=pd.read_csv("Red_Bus_G.csv")
for i,r in df_G.iterrows():
    lists_g.append(r["Route Name"])

#Rajastan bus
lists_R=[]
df_R=pd.read_csv("Red_Bus_R.csv")
for i,r in df_R.iterrows():
    lists_R.append(r["Route Name"])


# South bengal bus 
lists_SB=[]
df_SB=pd.read_csv("Red_Bus_SB.csv")
for i,r in df_SB.iterrows():
    lists_SB.append(r["Route Name"])

# Haryana bus
lists_H=[]
df_H=pd.read_csv("Red_Bus_H.csv")
for i,r in df_H.iterrows():
    lists_H.append(r["Route Name"])

#Assam bus
lists_AS=[]
df_AS=pd.read_csv("Red_Bus_AS.csv")
for i,r in df_AS.iterrows():
    lists_AS.append(r["Route Name"])

#UP bus
lists_UP=[]
df_UP=pd.read_csv("Red_Bus_UP.csv")
for i,r in df_UP.iterrows():
    lists_UP.append(r["Route Name"])

#West bengal bus
lists_WB=[]
df_WB=pd.read_csv("Red_Bus_WB.csv")
for i,r in df_WB.iterrows():
    lists_WB.append(r["Route Name"])


#setting up streamlit page
slt.set_page_config(layout="wide")

web=option_menu(menu_title="🚌OnlineBus",
                options=["Home page","📍States and Routes"],
                icons=["house","info-circle"],
                orientation="horizontal"
                )
# Home page setting
if web=="Home page":
    #slt.image("images_500x300.jpg",use_column_width=True)
    slt.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
    slt.subheader(":blue[Domain:]  Transportation")
    slt.subheader(":blue[Ojective:] ")
    slt.markdown("The 'Redbus Data Scraping and Filtering with Streamlit Application' providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data ") 
# States and Routes page setting
if web == "📍States and Routes":
    S = slt.selectbox("Lists of States", ["Kerala", "Adhra Pradesh", "Telugana", "Goa", "Rajastan", 
                                          "South Bengal", "Haryana", "Assam", "Uttar Pradesh", "West Bengal"])
    
    col1,col2=slt.columns(2)
    with col1:
        select_type = slt.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_fare = slt.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))
    TIME=slt.time_input("select the time")

    # Kerala bus fare filtering
    if S == "Kerala":
        K = slt.selectbox("List of routes",lists_k)

        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="murali", password="root", database="bus_routes")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{K}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        slt.dataframe(df_result)

    # Adhra Pradesh bus fare filtering
    if S=="Adhra Pradesh":
        A=slt.selectbox("list of routes",lists_A)

        def type_and_fare_A(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="murali", password="root", database="bus_routes")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{A}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_A(select_type, select_fare)
        slt.dataframe(df_result)
          

    # Telugana bus fare filtering
    if S=="Telugana":
        T=slt.selectbox("list of routes",lists_T)

        def type_and_fare_T(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="murali", password="root", database="bus_routes")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{T}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_T(select_type, select_fare)
        slt.dataframe(df_result)

    # Goa bus fare filtering
    if S=="Goa":
        G=slt.selectbox("list of routes",lists_g)

        def type_and_fare_G(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="murali", password="root", database="bus_routes")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{G}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_G(select_type, select_fare)
        slt.dataframe(df_result)

    # Rajastan bus fare filtering
    if S=="Rajastan":
        R=slt.selectbox("list of routes",lists_R)

        def type_and_fare_R(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="murali", password="root", database="bus_routes")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{R}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_R(select_type, select_fare)
        slt.dataframe(df_result)
          

    # South Bengal bus fare filtering       
    if S=="South Bengal":
        SB=slt.selectbox("list of rotes",lists_SB)

        def type_and_fare_SB(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="murali", password="root", database="bus_routes")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{SB}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_SB(select_type, select_fare)
        slt.dataframe(df_result)
    
    # Haryana bus fare filtering
    if S=="Haryana":
        H=slt.selectbox("list of rotes",lists_H)

        def type_and_fare_H(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="murali", password="root", database="bus_routes")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{A}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_H(select_type, select_fare)
        slt.dataframe(df_result)


    # Assam bus fare filtering
    if S=="Assam":
        AS=slt.selectbox("list of rotes",lists_AS)

        def type_and_fare_AS(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="murali", password="root", database="bus_routes")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{AS}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_AS(select_type, select_fare)
        slt.dataframe(df_result)

    # Utrra Pradesh bus fare filtering
    if S=="Utrra Pradesh":
        UP=slt.selectbox("list of rotes",lists_UP)

        def type_and_fare_UP(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="murali", password="root", database="bus_routes")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{UP}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_UP(select_type, select_fare)
        slt.dataframe(df_result)

    # West Bengal bus fare filtering
    if S=="West Bengal":
        WB=slt.selectbox("list of rotes",lists_WB)

        def type_and_fare_WB(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="murali", password="root", database="bus_routes")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{WB}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time  DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_WB(select_type, select_fare)
        slt.dataframe(df_result)

