#!/usr/bin/env python3
import argparse
import datetime
import sys
import html
from collections import OrderedDict
from utility.utils import add_days_fixed_30, get_base_date, generate_html, adjust_date,should_skip_adjustment, print_console_table, parse_args, ACTIONS

# --- Main ---

if __name__ == "__main__":
    args = parse_args()
    base_date = get_base_date(args.use_next_month)

    output_rows = []
    used_dates = set()
    sorted_actions = sorted(ACTIONS.items(), key=lambda x: x[1])  # Sort by offset to maintain order

    for name, offset in sorted_actions:
        actual = add_days_fixed_30(base_date, offset)
        final_date = adjust_date(name, actual)
        while final_date in used_dates:
            final_date = add_days_fixed_30(final_date, 1)
        used_dates.add(final_date)
        note = "No change" if actual == final_date else "Modified due to exception"
        output_rows.append({
            "name": name,
            "actual": actual.strftime("%Y-%m-%d"),
            "final": final_date.strftime("%Y-%m-%d"),
            "note": note
        })

    output_rows.sort(key=lambda r: r["final"])
    print_console_table(output_rows)
    generate_html(output_rows, base_date, args.output)
    print(f"✅ HTML report saved to: {args.output}")
