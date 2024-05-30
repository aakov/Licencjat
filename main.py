import csv
import math
from calendar import Calendar
from tkinter import *
from tkinter import filedialog, ttk, messagebox
import openmeteo_requests
import requests
import getpass
from datetime import datetime
from PIL import Image, ImageTk
import PIL
import requests_cache
import pandas as pd
from retry_requests import retry
from matplotlib.ticker import FormatStrFormatter
from tkcalendar import Calendar, DateEntry

import tkinter as tk
from tkcalendar import *
from tkcalendar import Calendar
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
        self.DataOdczytu = DataOdczytu #YYYYMMDD
        self.Daily_generated = Daily_generated
        self.HourUsageList = HourUsageList
        self.Daily_generatedKWh = Daily_generated/1000

class RealConsumptionHourly:
    def __init__(self, DataOdczytu, HourUsageList):
        self.DataOdczytu = DataOdczytu
        self.HourUsageList = HourUsageList
        self.DailySum = sum(HourUsageList)

class RealConsumptionDaily:
    def __init__(self, DataOdczytu, DailyConsumpution):
        self.DataOdczytu = DataOdczytu
        self.DailyConsumpution = DailyConsumpution

class CustomDaily:
    def __init__(self, DataOdczytu, DailyConsumpution):
        self.DataOdczytu = DataOdczytu
        self.DailyConsumpution = DailyConsumpution


listEmpty = []
day = Day(590543520100010199,20230101,'En. Czynna zbilansowana', listEmpty)
global balanced
balanced = []
balanced.append(day)
balanced.clear()
global energySold
energySold = []
energySold.append(day)
energySold.clear()
global energyBought
energyBought = []
energyBought.append(day)
energyBought.clear()
global froniusDaily_production_list
froniusDaily_production_list = []
froniusDay = FroniusDaily('02.01.2023', 8.11099)
froniusDaily_production_list.append(froniusDay)
froniusDaily_production_list.clear()
global froniusMinute_prodcution_list
froniusMinute_prodcution_list = []
froniusMinute = FroniusMinute('01.01.2023', 0.0, listEmpty)
froniusMinute_prodcution_list.append(froniusMinute)
froniusMinute_prodcution_list.clear()
global realConsumptionHourly_list
realConsumptionHourly_list = []
realConsumptionHourly = RealConsumptionHourly('01.01.2023', listEmpty)
realConsumptionHourly_list.append(realConsumptionHourly)
realConsumptionHourly_list.clear()
global realConsumptionDaily_list
realConsumptionDaily_list = []
realConsumptionDaily = RealConsumptionDaily('01.01.2023', 0.0)
realConsumptionDaily_list.append(realConsumptionDaily)
realConsumptionDaily_list.clear()
global customBalanced
customBalanced = []
customDay = CustomDaily('01.01.2023', 0.0)
customBalanced.append(customDay)
customBalanced.clear()
global customGivenEnergy
customGivenEnergy = []
customDay = CustomDaily('01.01.2023', 0.0)
customGivenEnergy.append(customDay)
customGivenEnergy.clear()
global customTakenEnergy
customTakenEnergy = []
customDay = CustomDaily('01.01.2023', 0.0)
customTakenEnergy.append(customDay)
customTakenEnergy.clear()
global customProducedEnergy
customProducedEnergy = []
customDay = CustomDaily('01.01.2023', 0.0)
customProducedEnergy.append(customDay)
customProducedEnergy.clear()
global customConsumedEnergy
customConsumedEnergy = []
customDay = CustomDaily('01.01.2023', 0.0)
customConsumedEnergy.append(customDay)
customConsumedEnergy.clear()




# label = tk.Label(text="Consumption Visualizer")
# label.pack()




# bg_image = Image.open("bg_pv_hd.jpg")
# bg_photo = ImageTk.PhotoImage(bg_image)
#
# bg_label = tk.Label(root, image=bg_photo)
# bg_label.place(x = 0, y =0)

# frame1 = Frame(root)
# frame1.pack(pady = 20)

# enter_start_date_label = tk.Label(root, text='Enter start date :')
# enter_start_date_label.place(x=100, y=10)
#
# start_date_entry_cal = Calendar(root, selectmode='day', year=2023, month=1, day=1)
# start_date_entry_cal.place(x=30, y=40)
#
# enter_end_date_label = tk.Label(root, text='Enter end date :')
# enter_end_date_label.place(x=100, y=270)
#
# end_date_entry_cal = Calendar(root, selectmode='day', year=2023, month=1, day=9)
# end_date_entry_cal.place(x=30, y=300)
#
# start_date_entry_cal.config(state='disabled')
# end_date_entry_cal.config(state='disabled')

global available_dates
available_dates = []

def unlock_dates():
    min_date = min(available_dates)
    max_date = max(available_dates)
    min_date = datetime.strptime(min_date, "%m/%d/%y").date()
    max_date = datetime.strptime(max_date, "%m/%d/%y").date()
    start_date_entry_cal.config(mindate=min_date, maxdate=max_date)
    end_date_entry_cal.config(mindate=min_date, maxdate=max_date)
    start_date_entry_cal.configure(state='normal')
    end_date_entry_cal.configure(state='normal')
    # for date_str in available_dates:
        # min_date = datetime.strptime(min_date, "%m/%d/%y").date()
        # max_date = datetime.strptime(max_date, "%m/%d/%y").date()
        # print(date_str)


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
        parse_and_export_to_lists(csv_reader, line_count)
        unlock_dates()

    # analyze_button.config(state=tk.DISABLED)
    #analyze_button.config(state=tk.NORMAL)

def open_file_fronius_daily():
    filename = filedialog.askopenfilename()
    with open(filename) as input:
        csv_reader = csv.reader(input, delimiter=',')
        line_count = 0
        parse_Fronius(csv_reader, line_count)
        unlock_dates()

        for instance in froniusDaily_production_list:
            print(instance.DataOdczytu)
def open_file_fronius_5():
    filename = filedialog.askopenfilename()

    with open(filename) as input:
        csv_reader = csv.reader(input, delimiter=',')
        line_count = 0
        parse_Fronius_5(csv_reader, line_count)
        unlock_dates()

        for instance in froniusMinute_prodcution_list:
            print(instance.DataOdczytu)

def open_file_custom_daily_report():

    subwindow = tk.Toplevel(root)

    delimiter_entry_label = tk.Label(subwindow, text='Enter delimiter :')
    delimiter_entry_label.pack()
    delimiter_entry = tk.Entry(subwindow)
    delimiter_entry.insert(0, ';')
    delimiter_entry.pack()
    date_column_entry_label = tk.Label(subwindow, text='Enter date column :')
    date_column_entry_label.pack()
    date_column_entry = tk.Entry(subwindow)
    date_column_entry.pack()
    power_data_column_entry_label = tk.Label(subwindow, text='Enter power data column :')
    power_data_column_entry_label.pack()
    power_data_column_entry = tk.Entry(subwindow)
    power_data_column_entry.pack()
    date_format_entry_label = tk.Label(subwindow, text='Enter date format :')
    date_format_entry_label.pack()
    date_format_entry = tk.Entry(subwindow)
    date_format_entry.pack()
    report_type_entry_label = tk.Label(subwindow, text='Enter report type : Given, Taken, Balanced, Produced, Consumed')
    report_type_entry_label.pack()
    report_type_entry = tk.Entry(subwindow)
    report_type_entry.pack()
    power_format_entry_label = tk.Label(subwindow, text='Enter power format : WH, kWH')
    power_format_entry_label.pack()
    power_format_entry = tk.Entry(subwindow)
    power_format_entry.pack()
    def prewiew():
        filename = filedialog.askopenfilename()
        with open(filename) as input:
            csv_reader = csv.reader(input, delimiter=delimiter_entry.get())
            line_count = 0
            text1 = None
            text2 = None
            for row in csv_reader:
                if line_count == 0:
                    text1 = row
                if line_count == 1:
                    text2 = row
                    break
            line_count += 1

            prewiew_label1 = tk.Label(subwindow, text=text1)
            prewiew_label1.pack()
            prewiew_label2 = tk.Label(subwindow, text=text2)
            prewiew_label2.pack()

    def analyze_custom_daily_report():
        filename = filedialog.askopenfilename()
        with open(filename) as input:
            csv_reader = csv.reader(input, delimiter=delimiter_entry.get())
            line_count = 0
            prewiew_label = tk.Label(subwindow, csv_reader[0 - 1])
            prewiew_label.pack()
            for row in csv_reader:
                if line_count == 0 or line_count == 1:
                    print(row)
                    line_count += 1
                else:
                    custom_daily_power_amount = Decimal(str(row[int(power_data_column_entry.get())]))
                    date = row[int(date_column_entry.get())]
                    customDay = CustomDaily(date, custom_daily_power_amount)
                    formated_to_calendar_format_date = datetime.strptime(row[int(power_data_column_entry.get())],
                                                                         date_format_entry.get()).strftime(
                        "%m/%d/%y")

                    available_dates.append(formated_to_calendar_format_date)
                    if report_type_entry.get() == 'Given':
                        customGivenEnergy.append(customDay)
                    elif report_type_entry.get() == 'Taken':
                        customTakenEnergy.append(customDay)
                    elif report_type_entry.get() == 'Balanced':
                        customBalanced.append(customDay)
                    elif report_type_entry.get() == 'Produced':
                        customProducedEnergy.append(customDay)
                    elif report_type_entry.get() == 'Consumed':
                        customConsumedEnergy.append(customDay)

                    # The date is in [dd.MM.yyyy]
                    # fronius_day = FroniusDaily(row[0], decimal_daily_energy_generation_fronius)
                    # froniusDaily_production_list.append(fronius_day)
            # parse_Fronius_5(csv_reader, line_count)

        for instance in froniusMinute_prodcution_list:
            print(instance.DataOdczytu)
        unlock_dates()
    open_file_button = tk.Button(subwindow, text='Open File', command=analyze_custom_daily_report)
    open_file_button.pack()
    preview_button = tk.Button(subwindow, text='Preview', command=prewiew)
    preview_button.pack()

    # subwindow.mainloop()


def preview():
    preview_subwindow = tk.Toplevel(root)
    filename = filedialog.askopenfilename()
    with open(filename) as input_file:
        csv_reader = csv.reader(input_file)
        line_count = 0
        text1 = None
        text2 = None
        for row in csv_reader:
            if line_count == 0:
                text1 = row
            elif line_count == 1:
                text2 = row
                break
            line_count += 1

        preview_label1 = tk.Label(preview_subwindow, text=text1)
        preview_label1.pack()
        preview_label2 = tk.Label(preview_subwindow, text=text2)
        preview_label2.pack()
def find_by_date(objects_list, date):
    for obj in objects_list:
        if obj.DataOdczytu == date:
            return obj
    # messagebox.showerror("Error", "No objects found with date '{}'".format(date))
    return None

def analyze_day():
    subwindow = tk.Toplevel(root)
    labelRemaining = ttk.Label(subwindow, text='Choose a date')
    labelRemaining.pack()
    cal = Calendar(subwindow, selectmode='day', year=2023, month=2, day=22)
    cal.pack()
    date = cal.get_date()

    def show_hourly_usage_linechart_day():
        print(balanced[0].DataOdczytu)
        print(balanced[0].HourUsageList)
        date = cal.get_date()
        startDate = datetime.strptime(date, "%m/%d/%y")
        startDate = startDate.strftime("%Y%m%d")
        print(startDate)
        picked_day_balanced = day
        picked_day_generated = day
        picked_day_spent = day
        labels = list(range(0, 24))
        # print(labels)

        for i in balanced:
            if i.DataOdczytu == startDate:
                picked_day_balanced = i
                break
        for i in energySold:
            if i.DataOdczytu == startDate:
                picked_day_generated = i
                break
        for i in energyBought:
            if i.DataOdczytu == startDate:
                picked_day_spent = i
                break
        print(picked_day_balanced.DataOdczytu)
        print(picked_day_balanced.HourUsageList)
        formatted_date = f"{startDate[:4]}/{startDate[4:6]}/{startDate[6:]}"
        plt.plot(labels, picked_day_balanced.HourUsageList, label='Balanced')
        plt.plot(labels, picked_day_generated.HourUsageList, label='Generated')
        plt.plot(labels, picked_day_spent.HourUsageList, label='Spent')
        plt.xlabel('Hour')
        plt.ylabel('KWH')
        plt.legend()
        plt.title('Hourly usage on ' + str(formatted_date))
        plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.show()

    def show_fronius_hourly():
        date = datetime.strptime(cal.get_date(), "%m/%d/%y").strftime("%d.%m.%Y")
        print(date)
        # end_date = datetime.strptime(end_date_entry.get(), "%Y%m%d").strftime("%d.%m.%Y")
        day = find_by_date(froniusMinute_prodcution_list, date)
        if day == None:
            messagebox.showerror("Error No objects found with date ", date)
        else:
            labels = list(range(0, 24))
            plt.plot(labels, day.HourUsageList, label='Produced Fronius')
            plt.xlabel('Hour')
            plt.ylabel('WH')
            plt.legend()
            plt.title('Hourly usage on ' + str(date))
            plt.show()

    def show_weather_temp():
        show_weather_hourly_1day(date)


    open_button_show_hourly_usage_linechart_day = ttk.Button(subwindow, text='Show_hourly_usage_linechart_day', command=show_hourly_usage_linechart_day)
    open_button_show_hourly_usage_linechart_day.pack()
    show_fronius_hourly_button = ttk.Button(subwindow, text='Show_fronius_linechart_hourly_button', command=show_fronius_hourly)
    show_fronius_hourly_button.pack()
    show_weather_temp_button = ttk.Button(subwindow, text='show_weather_temp', command=show_weather_temp)
    show_weather_temp_button.pack()
    subwindow.protocol("WM_DELETE_WINDOW", subwindow.destroy)



def show_weather_hourly_1day(date):
    date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 51.25,
        "longitude": 22.5667,
        "start_date": date,
        "end_date": date,
        "hourly": "temperature_2m",
        "daily": "sunshine_duration",
        "timezone": "Europe/Berlin"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    # print(hourly_dataframe)
    # print(hourly_temperature_2m)
    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_sunshine_duration = daily.Variables(0).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    daily_data["sunshine_duration"] = daily_sunshine_duration
    labels = list(range(0, 24))
    plt.plot(labels, hourly_temperature_2m, label='Produced')
    plt.xlabel('Hour')
    plt.ylabel('°C')
    plt.legend()
    plt.title('Hourly usage on ' + str(date))
    # plt.show()
    plt.figure(figsize=(10, 6))
    rounded_temp = [round(num) for num in hourly_temperature_2m]
    bars = plt.bar(labels, rounded_temp, alpha=0.7, color='blue')
    for bar, value in zip(bars, rounded_temp):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')
    # Show the plot
    plt.show()
    daily_dataframe = pd.DataFrame(data=daily_data)
    # print(daily_dataframe)

def parse_and_export_to_lists(csv_reader, line_count):
    global balanced, energySold, energyBought
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
            formated_to_calendar_format_date = datetime.strptime(row[numColDataOdczytu], "%Y%m%d").strftime("%m/%d/%y")
            available_dates.append(formated_to_calendar_format_date)
            if row[numColKierunek] == 'En. Czynna zbilansowana':
                balanced.append(day)
            elif row[numColKierunek] == 'En.Czynna Oddana':
                energySold.append(day)
            else:
                energyBought.append(day)
            line_count += 1

    print(f'Total: {line_count} lines')

def parse_Fronius(csv_reader,line_count):
    global froniusDaily_production_list
    for row in csv_reader:
        if line_count == 0 or line_count == 1:
            print(row)
            line_count +=1
        else:
            decimal_daily_energy_generation_fronius = Decimal(str(row[1]))
            #The date is in [dd.MM.yyyy]
            fronius_day = FroniusDaily(row[0], decimal_daily_energy_generation_fronius)
            froniusDaily_production_list.append(fronius_day)
            formated_to_calendar_format_date = datetime.strptime(row[0], "%d.%m.%Y").strftime("%m/%d/%y")
            # formated_to_calendar_format_date = row[0].strptime(start_date_entry_cal.get_date(), "%d.%m.%Y").strftime("%m/%d/%y")
            available_dates.append(formated_to_calendar_format_date)

def parse_Fronius_5(csv_reader, line_count):
    global froniusMinute_prodcution_list
    hourly_sum = 0
    prev_hour = 0
    prev_day = ''
    hour_usage_list = []
    minute_usage_list = []
    fronius_minutes_dict = {}
    daily_data = {}
    for row in csv_reader:
        if line_count == 0 or line_count == 1:
            print(row)
            line_count +=1
        else:
            date_str, energy_str = row[0], row[1]
            date_time = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
            date = date_time.date()
            energy = Decimal(energy_str) if energy_str.replace('.', '', 1).isdigit() else Decimal(0.0)
            if date not in daily_data:
                daily_data[date] = {'total_energy': Decimal(0), 'hourly_energy': [0] * 24}
            # Add energy production to total for the day
            daily_data[date]['total_energy'] += energy
             # Add energy production to appropriate hourly slot
            hour_index = date_time.hour
            daily_data[date]['hourly_energy'][hour_index] += energy
    for date, data in daily_data.items():
        formated_date = date.strftime("%d.%m.%Y")
        formated_to_calendar_format_date = date.strftime("%m/%d/%y")
        available_dates.append(formated_to_calendar_format_date)
        instance = FroniusMinute(formated_date, data['total_energy'], data['hourly_energy'])
        froniusMinute_prodcution_list.append(instance)

def show_sum():
    startDate = datetime.strptime(start_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")
    endDate = datetime.strptime(end_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")

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
    for i in energySold:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            generatedSum += i.DailySum
        if endDate == i.DataOdczytu:
            break


    startDateReached = False
    spentSum = 0
    for i in energyBought:
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
    startDate = f"{startDate[:4]}/{startDate[4:6]}/{startDate[6:]}"
    endDate = f"{endDate[:4]}/{endDate[4:6]}/{endDate[6:]}"
    # Add labels and a title
    # plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Total energy consumption between ' + startDate + '-' + endDate)

    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')

    print(energySold[0].DailySum)
    print(startDate)
    plt.show()

global called
def show_energy_price():
    pricePerKwHSpent = Decimal(energy_price_spent_entry.get())
    pricePerKwHGenerated = Decimal(energy_price_generated_entry.get())

    startDate = datetime.strptime(start_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")
    endDate = datetime.strptime(end_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")
    numberOfDays = 0
    startDateReached = False
    balancedSum = 0
    print(balanced[0].DailySum)
    for i in balanced:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            balancedSum += i.DailySum
            numberOfDays+=1
        if endDate == i.DataOdczytu:
            break

    startDateReached = False
    generatedSum = 0
    for i in energySold:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            generatedSum += i.DailySum
        if endDate == i.DataOdczytu:
            break


    startDateReached = False
    spentSum = 0
    for i in energyBought:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            spentSum += i.DailySum
        if endDate == i.DataOdczytu:
            break

    priceGenerated = generatedSum*pricePerKwHGenerated
    priceSpent = spentSum*pricePerKwHSpent
    priceFinal = priceSpent-priceGenerated

    called, fixedDailyCharge, fixedHourlyCharge
    fixedChargePriceModifier = numberOfDays*fixedDailyCharge + fixedHourlyCharge*numberOfDays*24
    priceFinal = priceFinal+fixedChargePriceModifier
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

def configure_price_settings():
    global called
    called = True
    # Nowe funkcje moga byc dodane w razie potrzeby
    # fixedHourlyCharge, fixedDailyCharge, offPeakRate, peakRate
    subwindow = Toplevel(root)
    subwindow.title("Ceny")
    peakRate_entry = ttk.Entry(subwindow)
    peakRate_entry.pack()
    offPeakRate_entry = ttk.Entry(subwindow)
    offPeakRate_entry.pack()
    fixedDailyCharge_entry = ttk.Entry(subwindow)
    ttk.Label(subwindow, text="Opłata stała dzienna").pack()
    fixedDailyCharge_entry.pack()
    fixedDailyCharge_entry.insert(0,"0")
    ttk.Label(subwindow, text="Opłata stała pogodzinna ").pack()
    fixedHourlyCharge_entry = ttk.Entry(subwindow)
    fixedHourlyCharge_entry.pack()
    fixedHourlyCharge_entry.insert(0,"0")

    peakRate_entry.insert(0,"1.5")
    offPeakRate_entry.insert(0,"0.75")
    global cena_zalezna_od_godziny
    cena_zalezna_od_godziny = BooleanVar()
    cena_zalezna_od_godziny_checkbox = ttk.Checkbutton(subwindow, text="Cena zalezna od godziny", variable=cena_zalezna_od_godziny)
    cena_zalezna_od_godziny_checkbox.pack()

    kary_za_prekroczenie_limitu = ttk.Checkbutton(subwindow, text="Kary za prekroczenie limitu")
    kary_za_prekroczenie_limitu.pack()

    # stawka dzienna, nocna, za oddanie, pobranie energii,
    ttk.Label(subwindow, text="Cena za pobranie energii z sieci w godzinach dziennych ").pack()
    dzienna_stawka_pobrane_entry = ttk.Entry(subwindow)
    dzienna_stawka_pobrane_entry.pack()
    ttk.Label(subwindow, text="Cena za pobranie energii z sieci w godzinach nocnych").pack()
    nocna_stawka_pobrane_entry = ttk.Entry(subwindow)
    nocna_stawka_pobrane_entry.pack()
    ttk.Label(subwindow, text="Cena za oddanie energii do sieci w godzinach dziennych").pack()
    dzienna_stawka_oddane_entry = ttk.Entry(subwindow)
    dzienna_stawka_oddane_entry.pack()
    ttk.Label(subwindow, text="Cena za oddanie energii do sieci w godzinach nocnych").pack()
    nocna_stawka_oddane_entry = ttk.Entry(subwindow)
    nocna_stawka_oddane_entry.pack()

    global fixedDailyCharge
    fixedDailyCharge = Decimal(fixedDailyCharge_entry.get())
    global fixedHourlyCharge
    fixedHourlyCharge = Decimal(fixedHourlyCharge_entry.get())
    # save_price_settings_button = ttk.Button(subwindow, text="Save price settings", command=save_price_settings)
    # save_price_settings_button.pack()
    cena_zalezna_od_godziny = BooleanVar()



def show_stacks_balanced():
    startDate = datetime.strptime(start_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")
    endDate = datetime.strptime(end_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")

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
    startDate = datetime.strptime(start_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")
    endDate = datetime.strptime(end_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")

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
    startDate = datetime.strptime(start_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")
    endDate = datetime.strptime(end_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")

    spent_dailySumList = []
    spent_dateList = []
    #count = 20230101
    startDateReached = False
    for i in energyBought:
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
    startDate = datetime.strptime(start_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")
    endDate = datetime.strptime(end_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")

    balanced_dailySumList = []
    generated_dailySumList = []
    spent_dailySumList = []
    balanced_dateList = []
    generated_dateList = []
    spent_dateList = []
    # count = 20230101

    startDateReached = False
    for i in energySold:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            generated_dailySumList.append(i.DailySum)
            generated_dateList.append(i.DataOdczytu)
        if i.DataOdczytu == endDate:
            break
    startDateReached = False
    for i in energyBought:
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
    startDate = start_date_entry_cal.get_date()
    endDate = end_date_entry_cal.get_date()
    start_date = datetime.strptime(start_date_entry_cal.get_date(), "%Y%m%d").strftime("%Y-%m-%d")
    end_date = datetime.strptime(end_date_entry_cal.get_date(), "%Y%m%d").strftime("%Y-%m-%d")
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
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunshine_duration"],
        "timezone": "Europe/Berlin"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(3).ValuesAsNumpy()

    daily_data = {"Date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s").normalize(),
        end=pd.to_datetime(daily.TimeEnd(), unit="s").normalize(),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    description = [interpret_weather_code(str(int(code))) for code in daily_weather_code]
    daily_data["weather_code"] = description
    daily_data["temperature_2m_max"] = [round(num) for num in daily_temperature_2m_max]
    daily_data["temperature_2m_min"] = [round(num) for num in daily_temperature_2m_min]
    # daily_data["sunshine_duration"] = daily_sunshine_duration

    daily_dataframe = pd.DataFrame(data=daily_data)
    subwindow = tk.Toplevel(root)
    tk.Label(subwindow, text=str(daily_dataframe.to_string(index=False))).pack()
    # print(daily_dataframe)

def interpret_weather_code(code):
    # Dokumentacja wzięta z OpenMeteo
    weather_interpretation = {
        "0": "Clear sky",
        "1": "Mainly clear",
        "2": "Partly cloudy",
        "3": "Overcast",
        "45": "Fog",
        "48": "Depositing rime fog",
        "51": "Drizzle: Light intensity",
        "53": "Drizzle: Moderate intensity",
        "55": "Drizzle: Dense intensity",
        "56": "Freezing Drizzle: Light intensity",
        "57": "Freezing Drizzle: Dense intensity",
        "61": "Rain: Slight intensity",
        "63": "Rain: Moderate intensity",
        "65": "Rain: Heavy intensity",
        "66": "Freezing Rain: Light intensity",
        "67": "Freezing Rain: Heavy intensity",
        "71": "Snow fall: Slight intensity",
        "73": "Snow fall: Moderate intensity",
        "75": "Snow fall: Heavy intensity",
        "77": "Snow grains",
        "80": "Rain showers: Slight intensity",
        "81": "Rain showers: Moderate intensity",
        "82": "Rain showers: Violent intensity",
        "85": "Snow showers: Slight intensity",
        "86": "Snow showers: Heavy intensity",
        "95": "Thunderstorm: Slight or moderate",
        "96": "Thunderstorm with slight hail",
        "99": "Thunderstorm with heavy hail"
    }

    description = weather_interpretation.get(code, "Unknown weather code")
    return description

def show_current_weather():
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
        "current": ["temperature_2m", "is_day", "rain", "showers", "snowfall", "weather_code", "cloud_cover"],
        "timezone": "auto"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_is_day = current.Variables(1).Value()
    current_rain = current.Variables(2).Value()
    current_showers = current.Variables(3).Value()
    current_snowfall = current.Variables(4).Value()
    current_weather_code = current.Variables(5).Value()
    current_cloud_cover = current.Variables(6).Value()

    print(f"Current time {current.Time()}")
    print(f"Current temperature_2m {current_temperature_2m}")
    print(f"Current is_day {current_is_day}")
    print(f"Current rain {current_rain}")
    print(f"Current showers {current_showers}")
    print(f"Current snowfall {current_snowfall}")
    print(f"Current weather_code {current_weather_code}")
    print(f"Current cloud_cover {current_cloud_cover}")

    description = interpret_weather_code(str(int(current_weather_code)))
    sunny_image = Image.open("sunny.jpg")
    sunny_image = sunny_image.resize((100, 100))
    sunny_image_tk = ImageTk.PhotoImage(sunny_image)
    moon_image = Image.open("moon.png")
    moon_image = moon_image.resize((100, 100))
    moon_image_tk = ImageTk.PhotoImage(moon_image)
    subwindow = tk.Toplevel(root)
    tk.Label(subwindow,text=description).pack()
    if current_is_day == 0.0:
        weather_label = tk.Label(subwindow, image=moon_image_tk)
        weather_label.pack()
        weather_label.image = moon_image_tk
    else:
        weather_label = tk.Label(subwindow, image=sunny_image_tk)
        weather_label.pack()
        weather_label.image = sunny_image_tk
    temp_label = tk.Label(subwindow, text=str(round(current_temperature_2m))+'°C')
    temp_label.pack()
    subwindow.protocol("WM_DELETE_WINDOW", subwindow.destroy)

def show_weather_forecast():
    lat, lon = get_coord()
    # Kod przeważnie z dokumentacji
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
        "timezone": "auto",
	    "forecast_days": 6
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()

    daily_data = {"Date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s").normalize(),
        end=pd.to_datetime(daily.TimeEnd(), unit="s").normalize(),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    description = [interpret_weather_code(str(int(code))) for code in daily_weather_code]
    daily_data["weather_code"] = description
    daily_data["Max"] = [round(num) for num in daily_temperature_2m_max]
    daily_data["Min"] = [round(num) for num in daily_temperature_2m_min]
    # print(str(daily_temperature_2m_min[1]) + " " + str(daily_temperature_2m_max[1]))
    daily_dataframe = pd.DataFrame(data=daily_data)
    subwindow = tk.Toplevel(root)
    tk.Label(subwindow, text=str(daily_dataframe.to_string(index=False))).pack()


def show_weather_forecast_for_energy_prediction_days(subwindow, date1, date2):
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
        "timezone": "auto",
        "forecast_days": 3
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
    day1TempMin = math.ceil(daily_temperature_2m_min[1])
    day1TempMax = math.ceil(daily_temperature_2m_max[1])
    day2TempMin = math.ceil(daily_temperature_2m_min[2])
    day2TempMax = math.ceil(daily_temperature_2m_max[2])
    print(str(day1TempMin) + " " + str(daily_temperature_2m_max[1]))
    t = "Weather on " + str(date1)+ " " + str(day1TempMin) + "C to " + str(day1TempMax) + "C " + "and on " + str(date2) + str(day2TempMin) + "C to" + str(day2TempMax) + "C "
    label = ttk.Label(subwindow, text=t).pack()

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

def show_hourly_usage_linechart():
    startDate = datetime.strptime(start_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")
    # endDate = datetime.strptime(end_date_entry_cal.get_date(), "%m/%d/%y").strftime("%Y%m%d")    print(startDate)
    picked_day_balanced = day
    picked_day_generated = day
    picked_day_spent = day
    labels = list(range(0, 24))
    print(labels)
    for i in balanced:
        if i.DataOdczytu == startDate:
            picked_day_balanced = i
            break
    for i in energySold:
        if i.DataOdczytu == startDate:
            picked_day_generated = i
            break
    for i in energyBought:
        if i.DataOdczytu == startDate:
            picked_day_spent = i
            break
    print(picked_day_balanced.DataOdczytu)
    print(picked_day_balanced.HourUsageList)
    formatted_date = f"{startDate[:4]}/{startDate[4:6]}/{startDate[6:]}"
    plt.plot(labels, picked_day_balanced.HourUsageList, label='Balanced')
    plt.plot(labels, picked_day_generated.HourUsageList, label='Generated')
    plt.plot(labels, picked_day_spent.HourUsageList, label='Spent')
    plt.xlabel('Hour')
    plt.ylabel('KWH')
    plt.legend()
    plt.title('Hourly usage on ' + str(formatted_date))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.show()

def show_fronius_sum():
    start_date = datetime.strptime(start_date_entry_cal.get_date(), "%Y%m%d").strftime("%d.%m.%Y")
    end_date = datetime.strptime(end_date_entry_cal.get_date(), "%Y%m%d").strftime("%d.%m.%Y")
    # print(start_date)
    # print(end_date)
    sum_fronius = 0
    startDateReached = False
    for i in froniusDaily_production_list:
        if i.DataOdczytu == start_date:
            startDateReached = True
        if startDateReached == True:
            sum_fronius += i.Daily_generated
        if i.DataOdczytu == end_date:
            break
    # for i in froniusDaily_usagelist:
    #     sum_fronius += i.Daily_generated
    subwindow = tk.Toplevel(root)
    subwindow.title("Ammount of energy generated during the given time period")
    labelRemaining = ttk.Label(subwindow, text='Ammount of energy generated during the given time period : ' + str(sum_fronius))
    labelRemaining.pack()
    subwindow.protocol("WM_DELETE_WINDOW", subwindow.destroy)

def show_stacks_Fronius_daily():
    start_date = datetime.strptime(start_date_entry_cal.get_date(), "%Y%m%d").strftime("%d.%m.%Y")
    end_date = datetime.strptime(end_date_entry_cal.get_date(), "%Y%m%d").strftime("%d.%m.%Y")

    dailyProduction_list = []
    dateList = []

    startDateReached = False
    for i in froniusDaily_production_list:
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
    start_date = datetime.strptime(start_date_entry_cal.get_date(), "%Y%m%d").strftime("%d.%m.%Y")
    end_date = datetime.strptime(end_date_entry_cal.get_date(), "%Y%m%d").strftime("%d.%m.%Y")

    dailyProduction_list = []
    dateList = []

    startDateReached = False
    for i in froniusDaily_production_list:
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
    startDate = start_date_entry_cal.get_date()
    endDate = end_date_entry_cal.get_date()
    start_date = datetime.strptime(start_date_entry_cal.get_date(), "%Y%m%d").strftime("%d.%m.%Y")
    end_date = datetime.strptime(end_date_entry_cal.get_date(), "%Y%m%d").strftime("%d.%m.%Y")

    startDateReached = False
    generatedSum = 0
    for i in energySold:
        if i.DataOdczytu == startDate:
            startDateReached = True
        if startDateReached == True:
            generatedSum += i.DailySum
        if endDate == i.DataOdczytu:
            break

    sum_fronius = 0
    startDateReached = False
    for i in froniusDaily_production_list:
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

    print(energySold[0].DailySum)
    print(startDate)
    plt.show()

def get_coord():
    # lat, lon = None, None
    city = city_entry.get()
    print(city)
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': city,
        'format': 'json',
        'limit': 1
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()

        if data:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            print(latitude)
            print(longitude)
            return latitude, longitude
        else:
            return None, None
    else:
        return None, None

def solar_energy_prediction_forecast():
    lat, lon = get_coord()
    plant_power = plant_power_entry.get()
    url = "https://api.forecast.solar/estimate/watthours/day/"+ str(lat) + "/"+ str(lon) +"/0/0/"+plant_power
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
        subwindow = tk.Toplevel(root)
        subwindow.title("Weather data")
        t = "Predicted energy output on " + date1 + " : " + str(prod1) + " and on " + date2 + " : " + str(prod2)
        label = ttk.Label(subwindow, text=t)
        label.pack(padx=20, pady=20)
        show_weather_forecast_for_energy_prediction_days(subwindow,date1,date2)
        limitText = "Limit per hour:" + str(message_data['ratelimit']['limit'])
        labelLimit = ttk.Label(subwindow, text=limitText)
        labelLimit.pack()
        remainingText = "Remaining Rate Limit: " + str(remaining_rate_limit)
        labelRemaining = ttk.Label(subwindow, text=remainingText)
        labelRemaining.pack()
        subwindow.protocol("WM_DELETE_WINDOW", subwindow.destroy)

        # print(api_data)
    else:
        print(f"Error: {response.status_code} - {response.text}")

root = tk.Tk()
root.geometry("1000x800")

# Menu
menubar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open PGE report ", command=open_file)
# file_menu.add_separator()
file_menu.add_command(label="Open fronius daily report ", command=open_file_fronius_daily)
# file_menu.add_separator()
file_menu.add_command(label="Open fronius 15 minute report ", command=open_file_fronius_5)
file_menu.add_separator()
file_menu.add_command(label="Conigure custom report", command=open_file_custom_daily_report)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

# Edit menu
edit_menu = tk.Menu(menubar, tearoff=0)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")
menubar.add_cascade(label="Edit", menu=edit_menu)

root.config(menu=menubar)

# Left: Calendars
enter_start_date_label = tk.Label(root, text='Enter start date:')
enter_start_date_label.place(x=100, y=10)

start_date_entry_cal = Calendar(root, selectmode='day', year=2023, month=1, day=1)
start_date_entry_cal.place(x=30, y=40)

enter_end_date_label = tk.Label(root, text='Enter end date:')
enter_end_date_label.place(x=100, y=270)

end_date_entry_cal = Calendar(root, selectmode='day', year=2023, month=1, day=9)
end_date_entry_cal.place(x=30, y=300)

start_date_entry_cal.config(state='disabled')
end_date_entry_cal.config(state='disabled')

# Center: PGE related stuff
button_size = 40
style = ttk.Style()
style.configure('Custom.TButton', background='blue')

open_button = ttk.Button(root, text='Open PGE report', command=open_file, width=button_size, style='Custom.TButton')
open_button.place(x=340, y=40)

open_button_Fronius_daily = ttk.Button(root, text='Open Fronius report', command=open_file_fronius_daily, width=button_size, style='Custom.TButton')
open_button_Fronius_daily.place(x=340, y=70)

open_button_Fronius_daily_15_minute_button = ttk.Button(root, text='Open Fronius 5 minute report', command=open_file_fronius_5, width=button_size, style='Custom.TButton')
open_button_Fronius_daily_15_minute_button.place(x=340, y=100)

open_button_custom_daily_report = ttk.Button(root, text='Open Custom Report', command=open_file_custom_daily_report, width=button_size, style='Custom.TButton')
open_button_custom_daily_report.place(x=340, y=130)

analyze_day_button = ttk.Button(root, text='Analyze day', command=analyze_day, width=button_size, style='Custom.TButton')
analyze_day_button.place(x=340, y=160)

preview_report_button = ttk.Button(root, text='Preview report', command=preview, width=button_size, style='Custom.TButton')
preview_report_button.place(x=340, y=190)
# Right: Other widgets

button_size1 = 30
show_line_graph_button = ttk.Button(root, text='Show line graph', command=show_line_graph, width=button_size1)
show_line_graph_button.place(x=640, y=10)

show_stacks_button_balanced = ttk.Button(root, text='Show stacks balanced', command=show_stacks_balanced, width=button_size1)
show_stacks_button_balanced.place(x=640, y=40)

show_stacks_button_generated = ttk.Button(root, text='Show stacks generated', command=show_stacks_generated, width=button_size1)
show_stacks_button_generated.place(x=640, y=70)

show_stacks_button_spent = ttk.Button(root, text='Show stacks spent', command=show_stacks_spent, width=button_size1)
show_stacks_button_spent.place(x=640, y=100)

show_fronius_sum_button = ttk.Button(root, text='Show fronius sum', command=show_fronius_sum, width=button_size1)
show_fronius_sum_button.place(x=640, y=130)

show_sum_button = ttk.Button(root, text='Show sum', command=show_sum, width=button_size1)
show_sum_button.place(x=640, y=160)
tk.Label(root, text="Default pricing model is W11 without additional costs").place(x=640, y=180)
tk.Label(root, text="Price per KwH Spent:").place(x=640, y=200)
energy_price_spent_entry = tk.Entry(root)
energy_price_spent_entry.place(x=640, y=220)

tk.Label(root, text="Price per KwH Generated:").place(x=640, y=250)
energy_price_generated_entry = tk.Entry(root)
energy_price_generated_entry.place(x=640, y=270)

show_energy_price_button = ttk.Button(root, text='Show energy price spent', command=show_energy_price, width=button_size1)
show_energy_price_button.place(x=640, y=300)
configure_energy_price_settings_button = ttk.Button(root, text='Modify energy price spent', command=configure_price_settings, width=button_size1)
configure_energy_price_settings_button.place(x=640, y=370)

show_stacks_Fronius_daily_button = ttk.Button(root, text='Show stacks Fronius daily', command=show_stacks_Fronius_daily, width=button_size1)
show_stacks_Fronius_daily_button.place(x=640, y=330)

show_linechart_Fronius_daily_button = ttk.Button(root, text='Show linechart Fronius daily', command=show_linechart_Fronius_daily, width=button_size1)
show_linechart_Fronius_daily_button.place(x=640, y=360)

show_differnce_betweenFronius_and_PGE_daily_button = ttk.Button(root, text='Show differnce between Fronius and PGE data ', command=show_differnce_betweenFronius_and_PGE_daily)
show_differnce_betweenFronius_and_PGE_daily_button.place(x=640, y=390)

display_graph_button = ttk.Button(root, text='Display Graph')
display_graph_button.place(x=640, y=420)

city_label = ttk.Label(root, text="Enter City: ")
city_label.place(x=640, y=450)

city_entry = ttk.Entry(root, width=20)
city_entry.insert(0, "Lublin")
city_entry.place(x=640, y=470)

show_weather_history_button = ttk.Button(root, text='Show weather history', command=show_weather_history, width=button_size1)
show_weather_history_button.place(x=640, y=500)

show_weather_forecast_button = ttk.Button(root, text='Show 7day weather forecast', command=show_weather_forecast, width=button_size1)
show_weather_forecast_button.place(x=640, y=530)

show_current_weather_button = ttk.Button(root, text='Show current weather', command=show_current_weather, width=button_size1)
show_current_weather_button.place(x=640, y=560)

show_hourly_usage_linechart_button = ttk.Button(root, text='Show hourly usage linechart', command=show_hourly_usage_linechart, width=button_size1)
show_hourly_usage_linechart_button.place(x=640, y=590)

tk.Label(root, text="Enter plant power:").place(x=640, y=620)
plant_power_entry = tk.Entry(root)
plant_power_entry.place(x=640, y=640)

solar_energy_prediction_forecast_button = ttk.Button(root, text='Solar energy prediction forecast', command=solar_energy_prediction_forecast, width=button_size1)
solar_energy_prediction_forecast_button.place(x=640, y=670)

get_coord_button = ttk.Button(root, text='Get coord', command=get_coord, width=button_size1)
get_coord_button.place(x=640, y=700)
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
