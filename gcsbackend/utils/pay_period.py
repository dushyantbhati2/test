from datetime import date

def current_month_period():
    today = date.today()
    return today.strftime("%B %Y")
