import argparse
import datetime
import sys
import html
from collections import OrderedDict

## Constants
BASE_DAY = 26    ## Aroung this date, all the actions will be generated
HOLIDAYS = ["2025-06-05", "2025-06-08", "2025-06-09","2025-06-10","2025-06-11","2025-06-12"]
ACTIONS = {
    "PD Call-1": -17,
    "PD Bill Issue SMS/EMAIL": -16,
    "PD Call-2": -8,
    "PD Bill Reminder SMS/EMAIL - 1": -6,
    "PD Call-3": -2,
    "PD Bill Reminder SMS/EMAIL - 2": -1,
    "OG BAR/SUSPEND SMS/EMAIL-1": 0,
    "OG BAR/SUSPEND SMS/EMAIL-2": 2,
    "OG BAR/SUSPEND/SPEED DOWNGRADE ACTION": 2,
    "FULL BAR SMS/EMAIL-1": 25,
    "FULL BAR SMS/EMAIL-2": 26,
    "FULL BAR Action": 30,
    "BlackList Action": 31
}
# --- Utils ---
def parse_args():
    parser = argparse.ArgumentParser(description="Generate action dates for a customer")
    parser.add_argument("--use-next-month", action="store_true", help="Use next month as base date")
    parser.add_argument("--output", type=str, default="actions_output.html", help="HTML output file")
    return parser.parse_args()

## Action planning to be done w.r.t current month or next month (default - Current month)
def get_base_date(use_next_month):
    today = datetime.date.today()
    month = today.month + (1 if use_next_month else 0)
    year = today.year + (1 if month > 12 else 0)
    month = 1 if month > 12 else month
    return datetime.date(year, month, BASE_DAY)

## This function will make all 12 months with 30 days
def add_days_fixed_30(base_date, offset):
    day = base_date.day + offset
    month = base_date.month
    year = base_date.year

    while day > 30:
        day -= 30
        month += 1
        if month > 12:
            month = 1
            year += 1
    while day < 1:
        day += 30
        month -= 1
        if month < 1:
            month = 12
            year -= 1

    return datetime.date(year, month, day)

## Check the action date falls on weekends or on holidays and exception days (here it is 1 and 7)
def is_exception_date(date):
    return date.weekday() in (3, 4, 5) or date.strftime("%Y-%m-%d") in HOLIDAYS or date.day in (1, 7)

## For which all actions, skip the date change
def should_skip_adjustment(name):
    name_lower = name.lower()
    return any(x in name_lower for x in ["sms", "email", "call"])

## Change action date to next available and valid date.
def adjust_date(name, date):
    if should_skip_adjustment(name):
        return date
    while is_exception_date(date):
        date = add_days_fixed_30(date, 1)
    return date

# --- HTML + Console Output ---
## standard output
def print_console_table(rows):
    print(f"\n{'Action Name':<37} | {'Actual Date':<12} | {'Final Date':<12} | {'Note'}")
    print("-" * 75)
    for r in rows:
        print(f"{r['name']:<37} | {r['actual']} | {r['final']} | {r['note']}")
    print()

## HTML file generation, which can be send over email
def generate_html(rows, base_date, output_file):
    with open(output_file, "w") as f:
        f.write(f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>Action Plan</title>
<style>
body {{ font-family: Arial; }}
table {{ border-collapse: collapse; width: 90%; }}
th, td {{ border: 1px solid #999; padding: 4px 6px; font-size: 13px; }}
th {{ background: #333; color: #fff; }}
.modified {{ background: #fff3cd; }}
.no-change {{ background: #d4edda; }}
</style>
</head><body>
<h2>Generated Action Dates (Base Date: {base_date})</h2>
<table>
<tr><th>Action Name</th><th>Actual Date</th><th>Final Date</th><th>Note</th></tr>
""")
        for r in rows:
            cls = "no-change" if r["note"] == "No change" else "modified"
            f.write(f"<tr class='{cls}'><td>{html.escape(r['name'])}</td><td>{r['actual']}</td><td>{r['final']}</td><td>{r['note']}</td></tr>\n")

        f.write("""
</table>
<br><hr>
<p style="font-size: 13px; color: #555;">
Regards,<br>
<strong>Action Planner Bot</strong><br>
Collection Automation Team<br>
<a href="mailto:support@example.com.sa">Sample@sample.com</a>
</p>
</body></html>""")

