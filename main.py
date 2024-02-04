import csv
from calendar import Calendar
from tkinter import *
from tkinter import filedialog, ttk
import openmeteo_requests
import requests
import getpass
from datetime import datetime


import requests_cache
import pandas as pd
from retry_requests import retry

from tkcalendar import *
import tkinter as tk
import matplotlib.pyplot as plt
from decimal import Decimal
import numpy as np
class Day:
    def __init__(self, KodPP, DataOdczytu, Kierunek, HourUsageList):
        self.KodPP = KodPP
        self.DataOdczytu = DataOdczytu
        self.Kierunek = Kierunek
        self.HourUsageList = HourUsageList
        self.DailySum = sum(HourUsageList)

class FroniusDaily:
    def __init__(self, DataOdczytu, Daily_generated):
        self.DataOdczytu = DataOdczytu
        self.Daily_generated = Daily_generated

class FroniusMinute:
    def __init__(self, DataOdczytu, Daily_generated,HourUsageList):
        self.DataOdczytu = DataOdczytu
        self.Daily_generated = Daily_generated
        self.HourUsageList = HourUsageList


listEmpty = []
day = Day(590543520100010199,20230101,'En. Czynna zbilansowana', listEmpty)
global balanced
balanced = []
balanced.append(day)
balanced.clear()
global generated
generated = []
generated.append(day)
generated.clear()
global spent
spent = []
spent.append(day)
spent.clear()
global froniusDaily_usagelist
froniusDaily_usagelist = []
froniusDay = FroniusDaily('02.01.2023', 8.11099)
froniusDaily_usagelist.append(froniusDay)
froniusDaily_usagelist.clear()
global froniusMinute_usagelist
froniusMinute_usagelist = []
froniusMinute = FroniusMinute('01.01.2023', 0.0, listEmpty)
froniusMinute_usagelist.append(froniusMinute)
froniusMinute_usagelist.clear()

root = tk.Tk()
root.geometry("1500x1000")
root.title("Consumption Visualizer")
# label = tk.Label(text="Consumption Visualizer")
# label.pack()

enter_start_date_label = tk.Label(root, text='Enter start date YYYYMMDD')
enter_start_date_label.pack()
start_date_entry = Entry(root)
start_date_entry.pack()
enter_end_date_label = tk.Label(root, text='Enter end date YYYYMMDD')
enter_end_date_label.pack()
end_date_entry = tk.Entry(root)
end_date_entry.pack()


# Label(root, text= "Choose a Date", background= 'gray61', foreground="white").pack() #padx=20,pady=20
# #Create a Calendar using DateEntry
# class DateEntry:
#     pass
#
#
# cal = Calendar(root, selectmode='day',
#                year=2020, month=5,
#                day=22)
#
# cal.pack(pady=20)
#
#
# def grad_date():
#     date.config(text="Selected Date is: " + cal.get_date())
#     print(cal.get_date())
#
#
# # Add Button and Label
# Button(root, text="Get Date", command=grad_date).pack()
#
# date = Label(root, text="")
# date.pack()


#To jest potrzebne bo inaczej nie da sie normalnie poierac wartosci z tablic


def open_file():
    # global filename
    filename = filedialog.askopenfilename()
    with open(filename) as input:
        csv_reader = csv.reader(input, delimiter=';')
        line_count = 0
        parse_and_export_to_lists(csv_reader,line_count)
    # analyze_button.config(state=tk.DISABLED)
    #analyze_button.config(state=tk.NORMAL)

def open_file_fronius_daily():
    filename = filedialog.askopenfilename()
    with open(filename) as input:
        csv_reader = csv.reader(input, delimiter=',')
        line_count = 0
        parse_Fronius(csv_reader, line_count)

def open_file_fronius_15():
    filename = filedialog.askopenfilename()
    with open(filename) as input:
        csv_reader = csv.reader(input, delimiter=',')
        line_count = 0
        # parse_Fronius_15(csv_reader, line_count)


open_button = ttk.Button(root, text='Open PGE report', command=open_file)
open_button.pack()

open_button_Fronius_daily = ttk.Button(root, text='Open Fronius report', command=open_file_fronius_daily)
open_button_Fronius_daily.pack()

# open_button_Fronius_daily_15_minute_button = ttk.Button(root, text='Open Fronius 5 minute report', command=open_file_fronius_15)
# open_button_Fronius_daily_15_minute_button.pack()


# def analyze_csv():
#     with open(filename) as input:
#         csv_reader = csv.reader(input, delimiter=';')
#         line_count = 0
#         parse_and_export_to_lists(csv_reader,line_count)
#     # analyze_button.config(state=tk.DISABLED)
#
#     # values = [balancedSum, generatedSum, spentSum]
#     # labels = ['En. Czynna zbilansowana', 'En.Czynna Oddana', 'En.Czynna Pobrana']
#     # colors = ['blue', 'green', 'red']
#     # # Create a bar chart
#     # bars = plt.bar(labels, values, color=colors)
#     #
#     # startDate = balanced[0].DataOdczytu
#     # endDate = balanced[-1].DataOdczytu
#     # startDate = f"{startDate[:4]}/{startDate[4:6]}/{startDate[6:]}"
#     # endDate = f"{endDate[:4]}/{endDate[4:6]}/{endDate[6:]}"
#     # # Add labels and a title
#     # # plt.xlabel('Categories')
#     # plt.ylabel('Values')
#     # plt.title('Total energy consumption between ' + startDate + '-' + endDate)
#     #
#     # for bar, value in zip(bars, values):
#     #     plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')
#     #
#     # print(generated[0].DailySum)
#     # print(generated[0].DataOdczytu)

def parse_and_export_to_lists(csv_reader, line_count):
    global balanced, generated, spent
    for row in csv_reader:
        if line_count == 0:
            print(row)
            line_count += 1
        else:
            # HourUsageList = [row[3]]
            numbers = []
            outnum = (row[3:27])
            data = ['0' if value.strip() == '' else value for value in outnum]
            for value in data:
                value = value.replace(',', '').replace(';', '')
                if value.startswith('-'):
                    value = '-' + value[1:].replace('-', '.')
                else:
                    value = value.replace('-', '.')
                numbers.append(float(value) / 1000)
            # print(numbers)
            numbers = [Decimal(str(num)) for num in numbers]
            day = Day(row[0], row[numColDataOdczytu], row[numColKierunek], numbers)
            if row[numColKierunek] == 'En. Czynna zbilansowana':
                balanced.append(day)
            elif row[numColKierunek] == 'En.Czynna Oddana':
                generated.append(day)
            else:
                spent.append(day)
            line_count += 1

    print(f'Total: {line_count} lines')

def parse_Fronius(csv_reader,line_count):
    global froniusDaily_usagelist
    for row in csv_reader:
        if line_count == 0 or line_count == 1:
            print(row)
            line_count +=1
        else:
            decimal_daily_energy_generation_fronius = Decimal(str(row[1]))
            #The date is in [dd.MM.yyyy]
            fronius_day = FroniusDaily(row[0], decimal_daily_energy_generation_fronius)
            froniusDaily_usagelist.append(fronius_day)

# def parse_Fronius_15(csv_reader,line_count):
#     global froniusMinute_usagelist
#     hourly_sum = 0
#     prev_hour = 0
#     prev_day = ''
#     hour_usage_list = []
#     minute_usage_list = []
#     for row in csv_reader:
#         if line_count == 0 or line_count == 1:
#             print(row)
#             line_count +=1
#         else:
#             whPower = row[1]
#             froniusDate = row[0]
#             date_object = datetime.strptime(froniusDate, "%d.%m.%Y %H:%M")
#             # Extract the hour from the datetime object
#             hour = date_object.hour
#             date_without_hour = date_object.strftime("%d.%m.%Y")
#             if line_count == 2:
#                 prev_hour = hour
#                 prev_day
#                 hourly_sum += whPower
#                 minute_usage_list.append(whPower)
#                 continue
#             if prev_hour ==


def show_sum():
    startDate = start_date_entry.get()
    print(startDate)
    endDate = end_date_entry.get()
    print(endDate)

    startDateReached = False
    balancedSum = 0
    print(balanced[0].DailySum)
    for i in balanced:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            balancedSum += i.DailySum
        if endDate == i.DataOdczytu:
            break

    startDateReached = False
    generatedSum = 0
    for i in generated:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            generatedSum += i.DailySum
        if endDate == i.DataOdczytu:
            break


    startDateReached = False
    spentSum = 0
    for i in spent:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            spentSum += i.DailySum
        if endDate == i.DataOdczytu:
            break

    print(balancedSum)
    print(generatedSum)
    print(spentSum)

    values = [balancedSum, generatedSum, spentSum]
    labels = ['En. Czynna zbilansowana', 'En.Czynna Oddana', 'En.Czynna Pobrana']
    colors = ['blue', 'green', 'red']
    # Create a bar chart
    bars = plt.bar(labels, values, color=colors)

    # startDate = balanced[0].DataOdczytu
    # endDate = balanced[-1].DataOdczytu
    startDate = f"{startDate[:4]}/{startDate[4:6]}/{startDate[6:]}"
    endDate = f"{endDate[:4]}/{endDate[4:6]}/{endDate[6:]}"
    # Add labels and a title
    # plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Total energy consumption between ' + startDate + '-' + endDate)

    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')

    print(generated[0].DailySum)
    print(startDate)
    plt.show()

def show_energy_price():
    pricePerKwHSpent = Decimal(energy_price_spent_entry.get())
    pricePerKwHGenerated = Decimal(energy_price_generated_entry.get())

    startDate = start_date_entry.get()
    # print(startDate)
    endDate = end_date_entry.get()
    # print(endDate)

    startDateReached = False
    balancedSum = 0
    print(balanced[0].DailySum)
    for i in balanced:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            balancedSum += i.DailySum
        if endDate == i.DataOdczytu:
            break

    startDateReached = False
    generatedSum = 0
    for i in generated:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            generatedSum += i.DailySum
        if endDate == i.DataOdczytu:
            break


    startDateReached = False
    spentSum = 0
    for i in spent:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            spentSum += i.DailySum
        if endDate == i.DataOdczytu:
            break

    print(balancedSum)
    print(generatedSum)
    print(spentSum)

    priceGenerated = generatedSum*pricePerKwHGenerated
    priceSpent = spentSum*pricePerKwHSpent
    priceFinal = priceSpent-priceGenerated
    # print(priceSpent)

    values = [priceFinal, priceGenerated, priceSpent]
    labels = ['Cena finalna ', 'Cena energi oddanej ', 'Cena energii pobranej ']
    colors = ['blue', 'green', 'red']
    # Create a bar chart
    bars = plt.bar(labels, values, color=colors)

    # startDate = balanced[0].DataOdczytu
    # endDate = balanced[-1].DataOdczytu
    startDate = f"{startDate[:4]}/{startDate[4:6]}/{startDate[6:]}"
    endDate = f"{endDate[:4]}/{endDate[4:6]}/{endDate[6:]}"
    # Add labels and a title
    # plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Total energy consumption between ' + startDate + '-' + endDate)

    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')

    # print(generated[0].DailySum)
    # print(startDate)
    plt.show()

def show_stacks_balanced():
    startDate = start_date_entry.get()
    print(startDate)
    endDate = end_date_entry.get()
    print(endDate)

    balanced_dailySumList = []
    generated_dailySumList = []
    spent_dailySumList = []
    balanced_dateList = []
    generated_dateList = []
    spent_dateList = []
    #count = 20230101
    startDateReached = False
    for i in balanced:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            balanced_dailySumList.append(i.DailySum)
            balanced_dateList.append(i.DataOdczytu)
        if i.DataOdczytu == endDate:
            break
    # for i in generated:
    #     if i.DataOdczytu == startDate:
    #         startDateReached = True
    #     if startDateReached == True:
    #         balanced_dailySumList.append(i.DailySum)
    #         balanced_dateList.append(i.DataOdczytu)
    #     if i.DataOdczytu == endDate:
    #         break


    # for i in generated:
    #     generated_dailySumList.append(i.DailySum)
    # for i in spent:
    #     spent_dailySumList.append(i.DailySum)
    #
    #
    #
    # plt.plot(x_values, balanced_dailySumList)

    days = np.arange(1, 11)  # 10 days
    energy_usage = np.random.randint(50, 200, size=10)  # Random energy usage values

    # Create a bar graph
    plt.figure(figsize=(10, 6))
    bars = plt.bar(balanced_dateList, balanced_dailySumList, alpha=0.7, color='blue')
    for bar, value in zip(bars, balanced_dailySumList):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')
    # Add labels and title
    # plt.xlabel('Days')
    # plt.ylabel('Energy Usage (kWh)')
    # plt.title('Energy Usage Over 10 Days (Bar Graph)')

    # Show the plot
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    # Show the plot
    plt.show()

def show_stacks_generated():
    startDate = start_date_entry.get()
    print(startDate)
    endDate = end_date_entry.get()
    print(endDate)

    balanced_dailySumList = []
    generated_dailySumList = []
    spent_dailySumList = []
    balanced_dateList = []
    generated_dateList = []
    spent_dateList = []
    #count = 20230101
    startDateReached = False
    for i in balanced:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            balanced_dailySumList.append(i.DailySum)
            balanced_dateList.append(i.DataOdczytu)
        if i.DataOdczytu == endDate:
            break

    plt.figure(figsize=(10, 6))
    bars = plt.bar(generated_dateList, generated_dailySumList, alpha=0.7, color='blue')
    for bar, value in zip(bars, generated_dailySumList):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')
    # Show the plot
    plt.show()

def show_stacks_spent():
    startDate = start_date_entry.get()
    print(startDate)
    endDate = end_date_entry.get()
    print(endDate)

    spent_dailySumList = []
    spent_dateList = []
    #count = 20230101
    startDateReached = False
    for i in spent:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            spent_dailySumList.append(i.DailySum)
            spent_dateList.append(i.DataOdczytu)
        if i.DataOdczytu == endDate:
            break

    plt.figure(figsize=(10, 6))
    bars = plt.bar(spent_dateList, spent_dailySumList, alpha=0.7, color='blue')
    for bar, value in zip(bars, spent_dailySumList):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')
    # Show the plot
    plt.show()

def show_line_graph():
    startDate = start_date_entry.get()
    endDate = end_date_entry.get()

    balanced_dailySumList = []
    generated_dailySumList = []
    spent_dailySumList = []
    balanced_dateList = []
    generated_dateList = []
    spent_dateList = []
    # count = 20230101

    startDateReached = False
    for i in generated:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            generated_dailySumList.append(i.DailySum)
            generated_dateList.append(i.DataOdczytu)
        if i.DataOdczytu == endDate:
            break
    startDateReached = False
    for i in spent:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            spent_dailySumList.append(i.DailySum)
            spent_dateList.append(i.DataOdczytu)
        if i.DataOdczytu == endDate:
            break
    for i in balanced:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            balanced_dailySumList.append(i.DailySum)
            balanced_dateList.append(i.DataOdczytu)
        if i.DataOdczytu == endDate:
            break
    plt.plot(balanced_dateList,balanced_dailySumList)
    plt.plot(generated_dateList, generated_dailySumList)
    plt.plot(spent_dateList, spent_dailySumList)
    plt.show()

def show_weather_history():
    lat, lon = get_coord()
    startDate = start_date_entry.get()
    endDate = end_date_entry.get()
    start_date = datetime.strptime(start_date_entry.get(), "%Y%m%d").strftime("%Y-%m-%d")
    end_date = datetime.strptime(end_date_entry.get(), "%Y%m%d").strftime("%Y-%m-%d")
    # Kod wzięty z dokimentacji Historical Weather API
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s"),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    print(hourly_dataframe)

#Kod przeważnie z dokumentacji

def show_weather_forecast():
    lat, lon = get_coord()
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s"),
        end=pd.to_datetime(daily.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min

    daily_dataframe = pd.DataFrame(data=daily_data)
    print(daily_dataframe)

# Set the login URL and other relevant URLs
# tk.Label(root, text="Login:").pack()
# login_entry = tk.Entry(root)
# login_entry.pack()
# tk.Label(root, text="Password:").pack()
# password_entry = tk.Entry(root, show='*')
# password_entry.pack()

def download_file(url, destination):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        with open(destination, 'wb') as file:
            file.write(response.content)

        print(f"File downloaded successfully to {destination}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download file from {url}. Error: {e}")

# def login():
#     username = login_entry.get()
#     password = password_entry.get()
#     login_url = 'https://login.fronius.com/'
#     reports_url = 'https://www.solarweb.com/Report/Reports?pvSystemId=097e980e-b07d-4e1f-910e-eb1355d999eb'
#     with requests.Session() as session:
#     # Perform login
#         login_payload = {'username': username, 'password': password}
#         session.post(login_url, data=login_payload)
#         print("Logged in")
#     # Navigate to the reports section
#         reports_page = session.get(reports_url)
#
#     # url = 'https://www.solarweb.com/Report/Reports?pvSystemId=097e980e-b07d-4e1f-910e-eb1355d999eb'
#     url = 'https://www.solarweb.com/Report/Download?reportId=3ca0673a-1d01-4fdb-a3e8-b0bf00cd373c'

# login__button = ttk.Button(root,text ='Login', command=login)
# login__button.pack()

def download_2023_daily_fronius():
    dowloadUrl = 'https://www.solarweb.com/Report/Download?reportId=ac33e9c1-7bf7-4bbb-8f0a-b0ef010d85d2'
    destination = '2023_year_report_PV_Production_daily.csv'
    download_file(dowloadUrl, destination)

def download_2022_daily_fronius():
    dowloadUrl = 'https://www.solarweb.com/Report/Download?reportId=53d7f4e6-df1b-460f-9183-b0f7001a95b3'
    destination = '2023_15_minute_report.csv'
    download_file(dowloadUrl, destination)

def download_2023_15_minute_report():
    dowloadUrl = 'https://www.solarweb.com/Report/Download?reportId=a8c25c30-382d-4d3b-a7de-b0f700fd1d3d'
    destination = '2023_15_minute_report.csv'
    download_file(dowloadUrl, destination)

# download_2023_daily_fronius_button = ttk.Button(root, text='Download_2023_daily', command=download_2023_daily_fronius)
# download_2023_daily_fronius_button.pack()  # Adjust padx as needed
#
#
# download_2022_daily_fronius_button = ttk.Button(root, text='Download_2022_daily', command=download_2022_daily_fronius)
# download_2022_daily_fronius_button.pack()
#
# download_2023_15_minute_report_button = ttk.Button(root, text='Download_2023_15_minute_report', command=download_2023_15_minute_report)
# download_2023_15_minute_report_button.pack()


def show_hourly_usage_linechart():
    startDate = start_date_entry.get()
    print(startDate)
    picked_day_balanced = day
    picked_day_generated = day
    picked_day_spent = day
    labels = list(range(0, 24))
    print(labels)
    for i in balanced:
        if i.DataOdczytu == startDate:
            picked_day_balanced = i
            break
    for i in generated:
        if i.DataOdczytu == startDate:
            picked_day_generated = i
            break
    for i in spent:
        if i.DataOdczytu == startDate:
            picked_day_spent = i
            break
    print(picked_day_balanced.DataOdczytu)
    print(picked_day_balanced.HourUsageList)
    plt.plot(labels, picked_day_balanced.HourUsageList)
    plt.plot(labels, picked_day_generated.HourUsageList)
    plt.plot(labels, picked_day_spent.HourUsageList)
    plt.show()

def show_fronius_sum():
    start_date = datetime.strptime(start_date_entry.get(), "%Y%m%d").strftime("%d.%m.%Y")
    end_date = datetime.strptime(end_date_entry.get(), "%Y%m%d").strftime("%d.%m.%Y")
    print(start_date)
    print(end_date)
    sum_fronius = 0
    startDateReached = False
    for i in froniusDaily_usagelist:
        if i.DataOdczytu == start_date:
            startDateReached = True
        if startDateReached == True:
            sum_fronius += i.Daily_generated
        if i.DataOdczytu == end_date:
            break
    # for i in froniusDaily_usagelist:
    #     sum_fronius += i.Daily_generated
    print(sum_fronius)

def show_stacks_Fronius_daily():
    start_date = datetime.strptime(start_date_entry.get(), "%Y%m%d").strftime("%d.%m.%Y")
    end_date = datetime.strptime(end_date_entry.get(), "%Y%m%d").strftime("%d.%m.%Y")

    dailyProduction_list = []
    dateList = []

    startDateReached = False
    for i in froniusDaily_usagelist:
        if i.DataOdczytu == start_date:
            startDateReached = True
        if startDateReached == True:
            dailyProduction_list.append(i.Daily_generated)
            dateList.append(i.DataOdczytu)
        if i.DataOdczytu == end_date:
            break

    plt.figure(figsize=(10, 6))
    bars = plt.bar(dateList, dailyProduction_list, alpha=0.7, color='blue')
    for bar, value in zip(bars, dailyProduction_list):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')
    # Show the plot
    plt.show()

def show_linechart_Fronius_daily():
    start_date = datetime.strptime(start_date_entry.get(), "%Y%m%d").strftime("%d.%m.%Y")
    end_date = datetime.strptime(end_date_entry.get(), "%Y%m%d").strftime("%d.%m.%Y")

    dailyProduction_list = []
    dateList = []

    startDateReached = False
    for i in froniusDaily_usagelist:
        if i.DataOdczytu == start_date:
            startDateReached = True
        if startDateReached == True:
            dailyProduction_list.append(i.Daily_generated)
            dateList.append(i.DataOdczytu)
        if i.DataOdczytu == end_date:
            break

    plt.plot(dateList, dailyProduction_list)
    plt.show()

def show_differnce_betweenFronius_and_PGE_daily():
    startDate = start_date_entry.get()
    endDate = end_date_entry.get()
    start_date = datetime.strptime(start_date_entry.get(), "%Y%m%d").strftime("%d.%m.%Y")
    end_date = datetime.strptime(end_date_entry.get(), "%Y%m%d").strftime("%d.%m.%Y")

    startDateReached = False
    generatedSum = 0
    for i in generated:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            generatedSum += i.DailySum
        if endDate == i.DataOdczytu:
            break

    sum_fronius = 0
    startDateReached = False
    for i in froniusDaily_usagelist:
        if i.DataOdczytu == start_date:
            startDateReached = True
        if startDateReached == True:
            sum_fronius += i.Daily_generated
        if i.DataOdczytu == end_date:
            break
    difference = sum_fronius-generatedSum

    values = [generatedSum, sum_fronius, difference]
    labels = ['PGE', 'Fronius', 'Difference']
    colors = ['blue', 'green', 'red']
    # Create a bar chart
    bars = plt.bar(labels, values, color=colors)

    # startDate = balanced[0].DataOdczytu
    # endDate = balanced[-1].DataOdczytu
    startDate = f"{startDate[:4]}/{startDate[4:6]}/{startDate[6:]}"
    endDate = f"{endDate[:4]}/{endDate[4:6]}/{endDate[6:]}"
    # Add labels and a title
    # plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Difference between produced energy and energy given back to the provider between ' + startDate + '-' + endDate)

    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')

    print(generated[0].DailySum)
    print(startDate)
    plt.show()

def get_coord():
    lat, lon = None, None
    city = city_entry.get()
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json"}

    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200 and data:
        first_result = data[0]
        lat, lon = float(first_result["lat"]), float(first_result["lon"])

    else:
        print("Error: Unable to retrieve coordinates.")
    return lat, lon



show_line_graph_button = ttk.Button(root,text='Show_line graph', command=show_line_graph)
show_line_graph_button.pack()

show_stacks_button_balanced = ttk.Button(root,text='Show_stacks balanced', command=show_stacks_balanced)
show_stacks_button_balanced.pack()

show_stacks_button_generated = ttk.Button(root,text='Show_stacks generated', command=show_stacks_generated)
show_stacks_button_generated.pack()

show_stacks_button_spent = ttk.Button(root,text='Show_stacks spent', command=show_stacks_spent)
show_stacks_button_spent.pack()



city_label = ttk.Label(root, text="Enter City: ")
city_label.pack()
city_entry = ttk.Entry(root, width=20)
city_entry.pack()

show_weather_history_button = ttk.Button(root,text='Show_weather_history', command=show_weather_history)
show_weather_history_button.pack()

show_weather_forecast_button = ttk.Button(root,text='Show_7day_weather_forecast', command=show_weather_forecast)
show_weather_forecast_button.pack()

show_hourly_usage_linechart_button = ttk.Button(root,text ='Show_hourly_usage_linechart', command=show_hourly_usage_linechart)
show_hourly_usage_linechart_button.pack()


# analyze_button = ttk.Button(root, text='Analyze PGE', command=analyze_csv)
# analyze_button.config(state=DISABLED)
# analyze_button.pack()
show_fronius_sum_button = ttk.Button(root,text ='Show_fronius_sum', command=show_fronius_sum)
show_fronius_sum_button.pack()

show_sum_button = ttk.Button(root,text='Show sum', command=show_sum)
show_sum_button.pack()

tk.Label(root, text="Price per KwH Spent:").pack()
energy_price_spent_entry = tk.Entry(root)
energy_price_spent_entry.pack()
tk.Label(root, text="Price per KwH Generated:").pack()
energy_price_generated_entry = tk.Entry(root)
energy_price_generated_entry.pack()

show_energy_price_button = ttk.Button(root,text='Show energy price spent', command=show_energy_price)
show_energy_price_button.pack()

show_stacks_Fronius_daily_button = ttk.Button(root,text='Show_stacks_Fronius_daily', command=show_stacks_Fronius_daily)
show_stacks_Fronius_daily_button.pack(padx=70)

show_linechart_Fronius_daily_button = ttk.Button(root,text='Show_linechart_Fronius_daily', command=show_linechart_Fronius_daily)
show_linechart_Fronius_daily_button.pack()

show_differnce_betweenFronius_and_PGE_daily_button = ttk.Button(root,text='Show_differnce_betweenFronius_and_PGE', command=show_differnce_betweenFronius_and_PGE_daily)
show_differnce_betweenFronius_and_PGE_daily_button.pack(padx=70)

display_graph_button = ttk.Button(root, text='Display Graph')

tk.Label(root, text="Enter plant power:").pack()
plant_power_entry = tk.Entry(root)
plant_power_entry.pack()

def solar_energy_prediction_forecast():
    plant_power = plant_power_entry.get()
    url = "https://api.forecast.solar/estimate/watthours/day/51.24/22.56/0/0/"+plant_power
    response = requests.get(url)
    #Pokazuje przewidywaną generację energii
    if response.status_code == 200:
        # Parse the JSON response
        api_data = response.json()
        result_data = api_data['result']
        message_data = api_data['message']

        # print(result_data)
        result_dates = list(result_data.keys())
        result_values = list(result_data.values())
        remaining_rate_limit = message_data['ratelimit']['remaining']
        # result_dates = str(result_dates).replace('[', '').replace(']', '')
        date1, date2 = result_dates
        print("Result Dates: ", date1, date2)
        prod1, prod2 = result_values
        print("Result Values in WH:", prod1, prod2)
        print("Limit per hour:", message_data['ratelimit']['limit'])
        print("Remaining Rate Limit:", remaining_rate_limit)
        # plt.ylabel('WH')
        # plt.title('Energy prefiction for ' + date1 + '-' + date2)
        # labels = [date1, date2]
        # values = [prod1, prod2]
        # bars = plt.bar(labels,values)
        # for bar, value in zip(bars, values):
        #     plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')
        # plt.show()
        # subwindow = tk.Toplevel(root)
        # subwindow.title("Weather data")
        t = "Predicted energy output on" + date1 + " : " + str(prod1) + "and on " + date2 + " : " + str(prod2)
        ttk.Label(root, text=t).pack()
        # label.pack(padx=20, pady=20)
        # subwindow.protocol("WM_DELETE_WINDOW", subwindow.destroy)
        # print(api_data)
    else:
        print(f"Error: {response.status_code} - {response.text}")


solar_energy_prediction_forecast_button = ttk.Button(root, text='Solar energy prediction forecast', command=solar_energy_prediction_forecast)
solar_energy_prediction_forecast_button.pack()

# L1 = Label(root, text="Enter Date")
# L1.pack()
# dateEntry = Entry(root)
# dateEntry.pack()

numColKierunek = 2
numColDataOdczytu = 1
# print('Numer kolumny daty ')
# print(numColDataOdczytu)
# print('Numer kolumny kierunku ')
# print(numColKierunek)
# print('Delimiter ;')

root.mainloop()
