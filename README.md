# productivity_calculator

Uses exports from QuickEMR & opentimeclock.com to calculate employee productivity


#FIXME

# Obtaining Inputs

quickEMR > Reports > Documentation > Provider Productivity > All Providers > Export

https://www.opentimeclock.com > Reports > Payroll Excel (under other) > Download > Open in Excel > File > Export > Change File Type > .csv


# Scrappy manual hour adjustment

If someone was traveling / at a school / for some reason being logged in OpenTimeClock but not in the clinic, this may be needed.

In the OpenTimeClock csv (probably named `PayrollExcel *`), simply change the number of "OpenTimeClock Hours" to the number of "Clinic Hours" for each day. Then run the program normally.

# Development

---

## Packaging

See `src/setup.py`

## Versioning

See `src/cfg.py` & `CHANGELOG.md`

