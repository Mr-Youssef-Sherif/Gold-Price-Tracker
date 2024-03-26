import json
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from data_ploter import GoldPricePlotter
import constants
import logging


today = date.today()
# Get the current year
current_year = datetime.now().year
# current time with hours minutes for the report
now = datetime.now()

unit_list = ["Global Ounce","24 Karat","22 Karat","21 Karat","18 Karat","14 Karat","12 Karat","Gold Ounce","Gold Coin"]

# Get the date, day name, and time without milliseconds
formatted_datetime = now.strftime("%A, %B %d, %Y %H:%M")

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Data Format
#data = {
#    "Number_of_days": 48,
#    "Number_of_Daily_reports": 4,
#    "Number_of_Weekly_reports": 0,
#    "Number_of_Monthly_reports": 0,
#    "Number_of_Plots": 4,
#    "Last_updated": str(datetime.now())
#}
    
# Functions that send periodic reports

def get_value_from_json(json_file_path, key):
    # Reading data from JSON file
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
    
    # Check if the key exists in the data
    if key in data:
        return data[key]
    else:
        print(f"Key '{key}' not found in the data.")
        return None

def increment_values(json_file_path, key, increment):
    # Reading data from JSON file
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
    
    # Incrementing the specified key
    if key in data:
        data[key] += increment
    else:
        print(f"Key '{key}' not found in the data.")
        return
    
    # Updating last_updated timestamp
    data["Last_updated"] = str(datetime.now())
    
    # Writing updated data back to JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def read_excel_fields(file_path, sheet_name, column_name):
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Extract the values of the specified column and convert them into a list
    field_list = df[column_name].tolist()
    
    return field_list

def check_yesterday_not_in_current_month():
    # Get today's date
    today = datetime.now()

    # Get yesterday's date
    yesterday = today - timedelta(days=1)

    # Check if yesterday's month is different from today's month
    if yesterday.month != today.month:
        return True
    else:
        return False
    
def remove_signs(items_list):
    filtered_list = []
    for item in items_list:
        if isinstance(item, str):
            filtered_list.append(int(item.replace('$', '')))
        else:
            filtered_list.append(item)
    return filtered_list


def get_price_changes_daily(items_list):
    if len(items_list) > 1:
        if items_list[-1] > items_list[-2]:
            return f"INCREASE:{items_list[-1]-items_list[-2]} ↗️"
        elif items_list[-1] < items_list[-2]:
            return f"DECREASE:{items_list[-2]-items_list[-1]} ↘️"
        else:
            return "Same price as yesterday"
    else:
        return 'NOT ENOUGH DATA'
    
def get_price_changes_weekly(items_list):
    if len(items_list) > 1:
        if items_list[-1] > items_list[0]:
            return f"INCREASE:{items_list[-1]-items_list[0]} ↗️"
        elif items_list[-1] < items_list[0]:
            return f"DECREASE:{items_list[0]-items_list[-1]} ↘️"
        else:
            return "Same prices as last week"
    else:
        return 'NOT ENOUGH DATA'

def get_price_changes_monthly(items_list):
    if len(items_list) > 1:
        if items_list[-1] > items_list[0]:
            return f"INCREASE:{items_list[-1]-items_list[0]} ↗️"
        elif items_list[-1] < items_list[0]:
            return f"DECREASE:{items_list[0]-items_list[-1]} ↘️"
        else:
            return "Same price as last month"
    else:
        return 'NOT ENOUGH DATA'


# Read data from db

column_Global_ounce = read_excel_fields(constants.excel_file_path, constants.sheet_name, unit_list[0])[::2]
column_24k = read_excel_fields(constants.excel_file_path, constants.sheet_name, unit_list[1])[::2]
column_22k = read_excel_fields(constants.excel_file_path, constants.sheet_name, unit_list[2])[::2]
column_21k = read_excel_fields(constants.excel_file_path, constants.sheet_name, unit_list[3])[::2]
column_18k = read_excel_fields(constants.excel_file_path, constants.sheet_name, unit_list[4])[::2]
column_14k = read_excel_fields(constants.excel_file_path, constants.sheet_name, unit_list[5])[::2]
column_12k = read_excel_fields(constants.excel_file_path, constants.sheet_name, unit_list[6])[::2]
column_ounce = read_excel_fields(constants.excel_file_path, constants.sheet_name, unit_list[7])[::2]
column_coin = read_excel_fields(constants.excel_file_path, constants.sheet_name, unit_list[8])[::2]
# Read days,months
column_Day = read_excel_fields(constants.excel_file_path, constants.sheet_name, "Day")[::2]
column_Date = read_excel_fields(constants.excel_file_path, constants.sheet_name, "Date")[::2]
column_Month = read_excel_fields(constants.excel_file_path, constants.sheet_name, "Month")[::2]


# Analyize Data

# Make each date a datetime object

dates = [datetime.strptime(date, "%Y-%m-%d") for date in column_Date]

# Get the current date
current_date = datetime.now()

# Subtract one month from the current date
previous_month_date = current_date - relativedelta(months=1)

# Get the name of the previous month
previous_month_name = previous_month_date.strftime("%B")

# Get the number of occurrences of the previous month in the last column
previous_month_occurrences = sum(1 for month in column_Month if month == previous_month_name)

# Change its value to negative and add one to it to get its range from the list
# Add 1 to the number of occurrences 
previous_month_occurrences+=1
# make it negative
previous_month_occurrences*=-1

def create_daily_report():
    price_list = []
    price_list.append(column_Global_ounce[-1])
    price_list.append(column_24k[-1])
    price_list.append(column_22k[-1])
    price_list.append(column_21k[-1])
    price_list.append(column_18k[-1])
    price_list.append(column_14k[-1])
    price_list.append(column_12k[-1])
    price_list.append(column_ounce [-1])
    price_list.append(column_coin[-1])
    
    # get Daily differences

    column_Global_ounce_filtered_daily = remove_signs(column_Global_ounce)
    column_global_ounce_stat_daiy = get_price_changes_daily(column_Global_ounce_filtered_daily)
    column_24k_stat_daiy = get_price_changes_daily(column_24k)
    column_22k_stat_daiy = get_price_changes_daily(column_22k)
    column_21k_stat_daiy = get_price_changes_daily(column_21k)
    column_18k_stat_daiy = get_price_changes_daily(column_18k)
    column_14k_stat_daiy = get_price_changes_daily(column_14k)
    column_12k_stat_daiy = get_price_changes_daily(column_12k)
    column_ounce_stat_daiy = get_price_changes_daily(column_ounce)
    column_coin_stat_daiy= get_price_changes_daily(column_coin)
    
    report = f"""
    Daily report {formatted_datetime}
    Global ounce price - {price_list[0]}
    24 Gold Karat price - {price_list[1]}
    22 Gold Karat price - {price_list[2]} 
    21 Gold Karat price - {price_list[3]}
    18 Gold Karat price - {price_list[4]}
    14 Gold Karat price - {price_list[5]}
    12 Gold Karat price - {price_list[6]}
    Gold Ounce price - {price_list[7]}
    Gold Coin price - {price_list[8]}
    -----------------Price Changes------------------------
    Global ounce price - {column_global_ounce_stat_daiy}
    24 Gold Karat price - {column_24k_stat_daiy}
    22 Gold Karat price - {column_22k_stat_daiy} 
    21 Gold Karat price - {column_21k_stat_daiy}
    18 Gold Karat price - {column_18k_stat_daiy}
    14 Gold Karat price - {column_14k_stat_daiy}
    12 Gold Karat price - {column_12k_stat_daiy}
    Gold Ounce price - {column_ounce_stat_daiy}
    Gold Coin price - {column_coin_stat_daiy}"""
    # Save it as txt

    with open(constants.daily_report_file_path, "w", encoding="utf-8") as file:
        file.write(report)
    logger.info(f"Report has been saved to {constants.daily_report_file_path}")

def create_weekly_report():
    
    # get Weekly differences
    column_Global_ounce_filtered_weekly = remove_signs(column_Global_ounce)
    column_global_ounce_stat_weekly = get_price_changes_weekly(column_Global_ounce_filtered_weekly[-7:])
    column_24k_stat_weekly = get_price_changes_weekly(column_24k[-7:])
    column_22k_stat_weekly = get_price_changes_weekly(column_22k[-7:])
    column_21k_stat_weekly = get_price_changes_weekly(column_21k[-7:])
    column_18k_stat_weekly = get_price_changes_weekly(column_18k[-7:])
    column_14k_stat_weekly = get_price_changes_weekly(column_14k[-7:])
    column_12k_stat_weekly = get_price_changes_weekly(column_12k[-7:])
    column_ounce_stat_weekly = get_price_changes_weekly(column_ounce[-7:])
    column_coin_stat_weekly = get_price_changes_weekly(column_coin[-7:])
    
    # Calculate the date 7 days ago
    seven_days_ago = current_date - timedelta(days=7)

    # Format the date as "yyyy-mm-dd"
    formatted_date_seven_days_ago = seven_days_ago.strftime("%Y-%m-%d")
    

    report = f"""
    Weekly report from:{formatted_date_seven_days_ago} to : {formatted_datetime}
    
    -----------------Price changes since last week------------------------
    Global ounce price - {column_global_ounce_stat_weekly}
    24 Gold Karat price - {column_24k_stat_weekly}
    22 Gold Karat price - {column_22k_stat_weekly} 
    21 Gold Karat price - {column_21k_stat_weekly}
    18 Gold Karat price - {column_18k_stat_weekly}
    14 Gold Karat price - {column_14k_stat_weekly}
    12 Gold Karat price - {column_12k_stat_weekly}
    Gold Ounce price - {column_ounce_stat_weekly}
    Gold Coin price - {column_coin_stat_weekly}"""
    # Save it as txt

    with open(constants.weekly_report_file_path, "w", encoding="utf-8") as file:
        file.write(report)
    logger.info(f"Report has been saved to {constants.weekly_report_file_path}")

def create_monthly_report():
    # Calculate the date since last month
    date_since_last_month = current_date - timedelta(days=previous_month_occurrences*-1)

    # Format the date as "yyyy-mm-dd"
    formatted_date_seven_days_ago = date_since_last_month.strftime("%Y-%m-%d")
    # get from the first time the previos month had a record to the item before the last item
    # e.g previous month had 30 occurrences so make it -31 to get the full range
    # because you don't take the last item you leave it which is the -1 item
    
    # get Monthly differences

    column_Global_ounce_filtered_monthly = remove_signs(column_Global_ounce)
    column_global_ounce_stat_monthly = get_price_changes_monthly(column_Global_ounce_filtered_monthly[previous_month_occurrences:-1])
    column_24k_stat_monthly = get_price_changes_monthly(column_24k[previous_month_occurrences:-1])
    column_22k_stat_monthly = get_price_changes_monthly(column_22k[previous_month_occurrences:-1])
    column_21k_stat_monthly = get_price_changes_monthly(column_21k[previous_month_occurrences:-1])
    column_18k_stat_monthly = get_price_changes_monthly(column_18k[previous_month_occurrences:-1])
    column_14k_stat_monthly = get_price_changes_monthly(column_14k[previous_month_occurrences:-1])
    column_12k_stat_monthly = get_price_changes_monthly(column_12k[previous_month_occurrences:-1])
    column_ounce_stat_monthly = get_price_changes_monthly(column_ounce[previous_month_occurrences:-1])
    column_coin_stat_monthly = get_price_changes_monthly(column_coin[previous_month_occurrences:-1])
    report = f"""
    Monthly report from:{formatted_date_seven_days_ago} to : {formatted_datetime}
    
    -----------------Price changes since last month-----------------------
    Global ounce price - {column_global_ounce_stat_monthly}
    24 Gold Karat price - {column_24k_stat_monthly}
    22 Gold Karat price - {column_22k_stat_monthly} 
    21 Gold Karat price - {column_21k_stat_monthly}
    18 Gold Karat price - {column_18k_stat_monthly}
    14 Gold Karat price - {column_14k_stat_monthly}
    12 Gold Karat price - {column_12k_stat_monthly}
    Gold Ounce price - {column_ounce_stat_monthly}
    Gold Coin price - {column_coin_stat_monthly}"""
    # Save it as txt
    with open(constants.monthly_report_file_path, "w", encoding="utf-8") as file:
        file.write(report)
    logger.info(f"Report has been saved to {constants.monthly_report_file_path}")
    
# Plot Data
    
def plot_daily_plot():
    if len(dates) >= 6:
        gold_plotter = GoldPricePlotter(dates[-6:], column_Global_ounce[-6:], column_24k[-6:], column_22k[-6:], column_21k[-6:], column_18k[-6:], column_14k[-6:], column_12k[-6:], column_ounce[-6:], column_coin[-6:],constants.daily_plots_path)
        gold_plotter.plot_gold_prices()
    else:
        gold_plotter = GoldPricePlotter(dates,column_Global_ounce, column_24k, column_22k, column_21k, column_18k, column_14k, column_12k, column_ounce, column_coin,constants.daily_plots_path)
        gold_plotter.plot_gold_prices()

        
def plot_weekly_plot():
    if len(dates) >= 9:
        gold_plotter = GoldPricePlotter(dates[-9:], column_Global_ounce[-9:], column_24k[-9:], column_22k[-9:], column_21k[-9:], column_18k[-9:], column_14k[-9:], column_12k[-9:], column_ounce[-9:], column_coin[-9:],constants.weekly_plots_path)
        gold_plotter.plot_gold_prices()
    else:
        gold_plotter = GoldPricePlotter(dates, column_Global_ounce, column_24k, column_22k, column_21k, column_18k, column_14k, column_12k, column_ounce, column_coin,constants.weekly_plots_path)
        gold_plotter.plot_gold_prices()
        
def plot_month_plot():
    if len(dates) >= (previous_month_occurrences*-1):
        gold_plotter = GoldPricePlotter(dates[previous_month_occurrences:-1], column_Global_ounce[previous_month_occurrences:-1], column_24k[previous_month_occurrences:-1], column_22k[previous_month_occurrences:-1], column_21k[previous_month_occurrences:-1], column_18k[previous_month_occurrences:-1], column_14k[previous_month_occurrences:-1], column_12k[previous_month_occurrences:-1], column_ounce[previous_month_occurrences:-1], column_coin[previous_month_occurrences:-1],constants.monthly_plots_path)
        gold_plotter.plot_gold_prices()
    else:
        gold_plotter = GoldPricePlotter(dates, column_Global_ounce, column_24k, column_22k, column_21k, column_18k, column_14k, column_12k, column_ounce, column_coin,constants.monthly_plots_path)
        gold_plotter.plot_gold_prices()


# After the scan add to the days that one scan have been made 
increment_values(constants.stats_file_path, "Number_of_Days", 1)
increment_values(constants.stats_file_path, "Number_of_Plots", 1)
increment_values(constants.stats_file_path, "Number_of_Daily_reports", 1)


yesterday_not_in_current_month = check_yesterday_not_in_current_month() # bool
number_of_reports=  get_value_from_json(constants.stats_file_path, "Number_of_Daily_reports")


# Create reports based on stats
logger.info("Creating Daily report")
create_daily_report()
logger.info("Creating Daily Plot")
plot_daily_plot()

if (number_of_reports%7==0):
    logger.info("Creating Weekly report")
    create_weekly_report()
    logger.info("Creating Weekly Plot")
    # After the scan add to the days that one scan have been made 
    increment_values(constants.stats_file_path, "Number_of_Plots", 1)
    increment_values(constants.stats_file_path, "Number_of_Weekly_reports", 1)
    plot_weekly_plot()
if (yesterday_not_in_current_month):
    logger.info("Creating Monthly report")
    create_monthly_report()
    logger.info("Creating Monthly Plot")
    plot_month_plot()
    # After the scan add to the days that one scan have been made 
    increment_values(constants.stats_file_path, "Number_of_Plots", 1)
    increment_values(constants.stats_file_path, "Number_of_Monthly_reports", 1)
    

#if (number_of_reports%365==0):
#    create_yearly_report()
