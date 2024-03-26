from datetime import date,datetime
# Current day
today = date.today()
# Get the current year
current_year = datetime.now().year
# Sheet name
sheet_name = 'Sheet1'
# File names
main = "main-GoldTracker.py"
excel_file_path = f"assets/Data/Gold-Prices-File-{current_year}.xlsx"
periodic_reports_handler = "periodic_reports_handler.py"
bot_report_sender_file = "bot_report_sender.py"
# Reports
daily_report_file_path = f"assets/Reports/daily_report-{today}.txt"
weekly_report_file_path = f"assets/Reports/weekly_report-{today}.txt"
monthly_report_file_path = f"assets/Reports/monthly_report-{today}.txt"
# Plots
daily_plots_path = f"assets/Plots/Daily/plots-{today}.jpg"
weekly_plots_path = f"assets/Plots/Weekly/plots-{today}.jpg"
monthly_plots_path = f"assets/Plots/Monthly/plots-{today}.jpg"
# Stats
stats_file_path = "assets/Stats/stats.json"