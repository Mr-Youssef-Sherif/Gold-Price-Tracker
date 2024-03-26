import requests
from bs4 import BeautifulSoup
import csv
import lxml
import numpy as np
import pandas as pd
import os
from datetime import date
from data_ploter import GoldPricePlotter
import subprocess
from datetime import date,datetime
import logging
import constants

# First Phase: Collect Data

# Target URL

url = "https://banklive.net/gold-price-today-in-egypt"

# Get raw data from the Target website

request = requests.get(url)
req_stat = request.status_code
source_code = request.content
soup = BeautifulSoup(source_code, 'lxml')
# Current day
today = date.today()
# current time with hours minutes for the report
now = datetime.now()
# Get the current year
current_year = datetime.now().year
# Value Holders
source_code = None
soup = None
# Initialize lists to store data
unit_list = ["Global Ounce","24 Karat","22 Karat","21 Karat","18 Karat","14 Karat","12 Karat","Gold Ounce","Gold Coin"]
price_list = []
change_list = []

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def read_excel_fields(file_path, sheet_name, column_name):
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Extract the values of the specified column and convert them into a list
    field_list = df[column_name].tolist()
    
    return field_list


  
def remove_signs(items_list):
    filtered_list = []
    for item in items_list:
        if isinstance(item, str):
            filtered_list.append(int(item.replace('$', '')))
        else:
            filtered_list.append(item)
    return filtered_list
    

def get_price_changes_today(items_list):
    if len(items_list) > 1:
        if items_list[-1] > items_list[-2]:
            return f"INCREASE:{items_list[-1]-items_list[-2]} ↗️"
        elif items_list[-1] < items_list[-2]:
            return f"DECREASE:{items_list[-2]-items_list[-1]} ↘️"
        else:
            return "SAME PRICE AS LAST TIME"
    else:
        return 'NOT ENOUGH DATA'

if int(req_stat) == 200:
    
    logger.info("Connection == 200")
    
    source_code = request.content
    soup = BeautifulSoup(source_code,'lxml')
    
    logger.info("Got data")
    
#------------------------------------------------------------------------------------#

    # Get the table that contains everything
    table = soup.find("div", {"class": "block-content"}).find("table")
    
#------------------------------------------------------------------------------------#
    # Find all rows in the table
    rows = table.find_all("tr")

    # Iterate over rows skipping the header row (first row)
    for row in rows[1:]:
        # Find all cells in the row
        cells = row.find_all("td")
        # Extract data from cells
        price = cells[1].text.strip()
        change = cells[2].text.strip()
        # Append data to lists
        price_list.append(price)
        change_list.append(change)
        
#------------------------------------------------------------------------------------#
# Filter Data
    price_list = [round(float(item.replace('ج.م', '').replace(',', '').replace('$', ''))) for item in price_list]
# Add the Dollar sign to the Global price
    price_list[0] = str(price_list[0]) + ' $'
#------------------------------------------------------------------------------------#
    #data = {
    #    'Type': unit_list,
    #    'Price': price_list,
    #    'Change': change_list
    #}
    data = {
        'Type': ['Price', 'Change'],
        unit_list[0]: [price_list[0], change_list[0]],
        unit_list[1]: [price_list[1], change_list[1]],
        unit_list[2]: [price_list[2], change_list[2]],
        unit_list[3]: [price_list[3], change_list[3]],
        unit_list[4]: [price_list[4], change_list[4]],
        unit_list[5]: [price_list[5], change_list[5]],
        unit_list[6]: [price_list[6], change_list[6]],
        unit_list[7]: [price_list[7], change_list[7]],
        unit_list[8]: [price_list[8], change_list[8]],
}
#------------------------------------------------------------------------------------#

# Add today's date to the data dictionary
    data['Date'] = [today.strftime("%Y-%m-%d")] *2

    
# Add day names to the data dictionary
    data['Day'] = [datetime.strptime(today.strftime("%Y-%m-%d"), "%Y-%m-%d").strftime("%A")] *2
    
# Add Month names to the data dictionary
    data['Month'] = [datetime.strptime(today.strftime("%Y-%m-%d"), "%Y-%m-%d").strftime("%B")] *2

#------------------------------------------------------------------------------------#

# Create a pandas dataframe

    df_web_data = pd.DataFrame(data)
    
    logger.info("Added Data to db")

else:
    if int(req_stat) == 404:
        logger.info("URL not Found")
    else:
        logger.info("ERROR requesting page")
        
# Second phase: Add data to 1 excel file , visualize it,save visualizations
# Adding the data to an excel file and adding any new data

# Check if the Excel file exists
if os.path.isfile(constants.excel_file_path):
    # Load existing data
    df_excel = pd.read_excel(constants.excel_file_path)
    # Append new data
    df_combined = pd.concat([df_excel, df_web_data], axis=0)
else:
    # Create a new DataFrame
    df_combined = df_web_data

# Save the combined DataFrame to Excel
df_combined.to_excel(constants.excel_file_path, index=False)


logger.info("Running periodic reports handler")
# Run periodic reports handler.py
subprocess.run(['python',constants.periodic_reports_handler])

logger.info("Running bot report sender")
# Run the Python file using subprocess
subprocess.run(['python', constants.bot_report_sender_file])