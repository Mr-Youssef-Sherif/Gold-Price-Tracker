# Gold Price Seeker

Gold Price Seeker is an innovative Python bot designed to provide daily gold price updates directly to users. It offers comprehensive coverage, including 24, 22, 21, 18, and 14 karat gold, gold coins, and the global ounce price.

## Features

Daily Gold Price Updates: Daily reports on gold prices across various karats (24, 22, 21, 18, 14), gold coins, and the global ounce.
Data Analysis: Analyzes daily gold price data to identify trends and insights. (Note: Visualizations are not currently included in the GitHub repository due to limitations)
CSV Database: Efficiently stores daily gold price data in a CSV file for historical analysis and backup.
Web Scraping: Utilizes web scraping to gather the latest gold prices from selected online sources.
Technologies Used

Python: The core programming language of the project.
Web Scraping Libraries: Beautiful Soup for parsing HTML and extracting the desired information.
Data Analysis Library: Pandas for data manipulation.
CSV File Handling: Python's built-in CSV module for reading from and writing to CSV files.

## Setup

1. **Clone the Repository**: `git clone https://github.com/Mr-Youssef-Sherif/Gold-Price-Seeker.git`
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Configuration (Optional)**: 
   - You need to add your telegram API key. Get your API key from Telegram Bot Father.
   - Add the user ID list you want to send the report to.

The script uses default settings. If needed, you can adjust these within the code to target specific URLs for web scraping or configure the path for your CSV database file.

## Usage

To launch Gold Price Seeker and start receiving gold price updates:

If you want to run it now:
  python main-GoldTracker.py
else: # You want to schedule it 
  python script-scheduler.py
This command runs the main script, activating the web scraping process, data analysis, and the sending of daily reports (without visualizations). The script will update the CSV database with new data each day.

## Data Sources

Gold Price Seeker relies on publicly available gold price data, which it accesses through web scraping. The exact sources of gold price data will vary, but they typically include financial news websites, gold trading platforms, and banks. Ensure you comply with the terms of use and copyright laws of the websites you scrape.

## Contributing

Contributions to the Gold Price Seeker project are welcome! If you have suggestions for improvements or new features, feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is available under the GNU License. Feel free to use, modify, and distribute the code as you see fit.
