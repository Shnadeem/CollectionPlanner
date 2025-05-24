# 📅 Action Date Generator (Single-File Version)

This script computes **customer action dates** based on a base date (26th of the month), offset rules, and business day exceptions. It outputs the results to both the terminal and an HTML report.

## 🚀 Features
- Computes predefined customer actions with custom day offsets.
- Uses the 26th of the current (or next) month as a base reference date.
- Adjusts for:
  - Thursdays, Fridays, Saturdays
  - The 1st and 7th of the month
  - Predefined public holidays
- Skips adjustments for action names that include: `SMS`, `EMAIL`, or `CALL` (case-insensitive).
- Outputs:
  - Neatly formatted terminal table
  - Colorized HTML report with status highlights
- HTML report includes a branded signature

## 🛠 Requirements
- Python 3.7+

## 📄 Usage

```bash
python action_planner.py
```

### Optional Arguments

```bash
--use-next-month       # Use next month's 26th instead of current month
--output <filename>    # Specify output HTML filename (default: actions_output.html)
```

### Example

```bash
python action_planner.py --use-next-month --output next_month_plan.html
```

## 🧮 Logic Summary

1. Base date: 26th of current or next month.
2. Offsets applied to each action.
3. Adjusts dates that fall on restricted days (Thu, Fri, Sat, 1st, 7th, holidays), unless exempted.
4. Outputs in both terminal and HTML formats.

## 📧 Signature
HTML output includes:

```
— Automated by Action Date Generator Bot 🤖
```

## 👤 Author
**Your Name**  
Customer Automation Team  
📫 support@example.com

## 📝 License
MIT License
