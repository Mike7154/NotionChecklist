import datetime
import math
import calendar

def get_next_last_weekday(date, weekday):
    last_day_of_month = date.replace(day=28) + datetime.timedelta(days=4)
    last_day_of_month = last_day_of_month - datetime.timedelta(days=last_day_of_month.day)
    return last_day_of_month - datetime.timedelta(days=((last_day_of_month.weekday()+1) - weekday) % 7)

def get_last_weekday_of_month(year, month, weekday):
    date = datetime.date(year, month, 1)
    while True:
        next_last_weekday = get_next_last_weekday(date, weekday)
        if next_last_weekday.month != month:
            return next_last_weekday
        date = next_last_weekday + datetime.timedelta(days=1)

# A function that takes a date and finds
#the next date that is then nth day of
#the week of the mth weekofthe oth
#monthofthe quarter
def next_quarterly_mwd(date, nth_weekday, nth_week, nth_month):
    # A dictionary that maps each quarter to its starting month
    quarter_start = {1: 1, 2: 4, 3: 7, 4: 10}
    # Get the year, month and day ofthe given date
    year = date.year
    month = date.month
    day = date.day
    #If nth_month is 0, get last month
    if nth_month == 0:
        nth_month = 3
    #If week is 0, get last week
    if nth_week == 0:
        nth_week = 4
        last = True
    else:
        last = False
    # Findthe quarterofthe given date
    quarter = math.ceil(month / 3)

    # Findthe startingmonthofthe desiredmonthinthe quarter
    start_month = (quarter_start[quarter] + (nth_month-1)) % 12

    # Create a new date object that represents
    #the first dayofthe desiredmonth
    start_date = datetime.date(year, start_month, 1)

    # Findthe weekdayofthe firstdayofthe desiredmonth (1=Monday,7=Sunday)
    weekday = start_date.isoweekday()

    # Find how many days to add to gettothen thdayoftheweekinthe desiredmonth
    days_to_add = (nth_weekday - weekday) % 7

    # Add those days to gettothen thdayoftheweekinthe desiredmonth
    first_day = start_date + datetime.timedelta(days=days_to_add)

    # Add (m-1) *7 more days to gettothen thdayoftheweekinthe mthweekofthe desiredmonth
    result_date = first_day + datetime.timedelta(days=(nth_week-1)*7)
    if last:
        print(True)
        result_date = get_next_last_weekday(result_date, day)
    # Check if this date is after or equaltothegiven date
    if result_date >= date:
        print(True)
        print(result_date)
        # Return this date as theresult
        return result_date
    else:
        # Add3 months to gettothenextquarter
        next_quarter = start_date + datetime.timedelta(days=3*30)
        # Repeat steps6to10with thenewdate
        return next_quarterly_mwd(next_quarter, nth_weekday, nth_week, nth_month)


# A function that finds
#the next date that is then th day of
#the week of them th weekofthe oth
#monthofthe year
def next_yearly_mwd(date, day, week, month):
    # Getthe yearandmonthofthe given date
    year = date.year
    current_month = date.month
    #If week is 0, get last week
    if week == 0:
        week = 4
        last = True
    else:
        last = False
    #If nth_month is 0, get last month
    if month == 0:
        month = 12
    # Findthe targetmonthbyaddingthemonthoffsettothe currentmonth
    target_month = month

    # Create a new date object that represents
    #the first dayofthe targetmonth
    start_date = datetime.date(year, target_month, 1)

    # Findthe weekdayofthe firstdayofthe targetmonth (1=Monday,7=Sunday)
    weekday = start_date.isoweekday()

    # Find how many days to add to gettothen thdayoftheweekinthe targetmonth
    days_to_add = (day - weekday) % 7

    # Add those days to gettothen thdayoftheweekinthe targetmonth
    first_day = start_date + datetime.timedelta(days=days_to_add)

    # Add (week-1) *7 more days to gettothen thdayoftheweekinthe weekthweekof
    #the targetmonth
    result_date = first_day + datetime.timedelta(days=(week-1)*7)
    if last == True:
        result_date = get_next_last_weekday(date, day)


    # Check if this date is after or equaltothegiven date
    if result_date >= date:
        # Return this date as theresult
        return result_date
    else:
        # Add one year to gettothenextyear
        next_year = start_date + datetime.timedelta(days=365)
        # Repeat steps4to9with thenewdate
        return next_yearly_mwd(next_year, day, week, month)

def get_next_weekday(date, weekday):
    days_until_weekday = (weekday - (date.weekday()+3)) % 7
    return date + datetime.timedelta(days=days_until_weekday)

def get_nth_weekday_of_month(date, weekday, n):
    first_day_of_month = date.replace(day=1)
    offset = (weekday - (first_day_of_month.weekday()+1)) % 7
    nth_weekday = first_day_of_month + datetime.timedelta(days=offset + (n - 1) * 7)
    return nth_weekday

def get_next_monthly_wd(date, weekday, nth_week):
    result_date = get_nth_weekday_of_month(date, weekday, nth_week)
     # Check if this date is after or equaltothegiven date
    
    if result_date >= date:
        # Return this date as theresult
        return result_date
    else:
        next_month = result_date.replace(month = result_date.month + 1)
        # Add one month to gettothenextyear
        result_date = get_nth_weekday_of_month(next_month, weekday, nth_week)
        # Repeat steps4to9with thenewdate
        return result_date


def last_day_of_week(year, weekday):
    # A function that returns the date of the last given day of the week for the current year
    # weekday: an integer from 0 (Monday) to 6 (Sunday)
    
    # Get the last day of the year
    last_day = datetime.date(year, 12, 31)
    
    # Get the weekday of the last day of the year
    last_weekday = last_day.weekday() + 1
    
    # Calculate the difference between the desired weekday and the last weekday
    diff = last_weekday - weekday
    
    # Adjust the difference if it is negative or zero
    if diff < 0:
        diff += 7
    
    if diff >= 7:
        diff -= 7
    
    # Subtract the difference from the last day to get the last given day of the week
    return last_day - datetime.timedelta(days=diff)

def nth_weekday(year, weekday, n):
    # A function that returns the date of the nth weekday of the current year
    # n: an integer from 1 to 52
    # weekday: an integer from 0 (Sunday) to 6 (Saturday)
    
    
    # Get the first day of the year
    first_day = datetime.date(year, 1, 1)
    
    # Get the weekday of the first day of the year
    first_weekday = first_day.weekday() + 1
    
    # Calculate the difference between the desired weekday and the first weekday
    diff = weekday - first_weekday
    
    # Adjust the difference if it is negative or zero
    if diff <= 0:
        diff += 7
    
    # Add the difference and (n-1) weeks to the first day to get the nth weekday
    if n == 0:
        return last_day_of_week(year, weekday)
    else:
        return first_day + datetime.timedelta(days=diff + (n-1)*7)


def nth_day(year, n):
    # A function that returns the date of the nth day of the current year
    # n: an integer from 1 to 365 or 366
    
    
    # Get the first day of the year
    first_day = datetime.date(year, 1, 1)
    
    # Add (n-1) days to the first day to get the nth day
    return first_day + datetime.timedelta(days=n-1)

def get_nth_day_of_quarter(date, n):
    # get the current year and quarter
    year = date.year
    quarter = (date.month - 1) // 3 + 1
    
    # get the first month of the current quarter
    first_month_of_quarter = 3 * quarter - 2
    
    # get the first day of the current quarter
    qstart = datetime.date(year, first_month_of_quarter, 1)
    
    # add n - 1 days to get the nth day of the quarter
    qnth = qstart + datetime.timedelta(days = n - 1)
    
    # if the nth day is before or equal to the given date, move to the next quarter
    if qnth <= date:
        # if the current quarter is the last one, move to the next year
        if quarter == 4:
            year += 1
            quarter = 1
        else:
            # otherwise, increment the quarter by one
            quarter += 1
        
        # get the first month of the next quarter
        first_month_of_quarter = 3 * quarter - 2
        
        # get the first day of the next quarter
        qstart = datetime.date(year, first_month_of_quarter, 1)
        
        # add n - 1 days to get the nth day of the next quarter
        qnth = qstart + datetime.timedelta(days = n - 1)
    
    # return the next date that is the nth day of a quarter
    return qnth


def get_next_nth_weekday_of_month(date, n, weekday):
    # get the current year and month
    year = date.year
    month = date.month
    
    # get the first day of the current month
    first_day = datetime.date(year, month, 1)
    
    # get the first weekday of the current month
    first_weekday = first_day.isoweekday()
    
    # calculate the offset to get the first occurrence of the given weekday
    offset = (weekday - first_weekday) % 7
    
    # add n - 1 weeks to get the nth occurrence of the given weekday
    nth_weekday = first_day + datetime.timedelta(days = offset + (n - 1) * 7)
    
    # if the nth weekday is before or equal to the given date, move to the next month
    if nth_weekday <= date:
        # if the current month is December, move to the next year
        if month == 12:
            year += 1
            month = 1
        else:
            # otherwise, increment the month by one
            month += 1
        
        # get the first day of the next month
        first_day = datetime.date(year, month, 1)
        
        # get the first weekday of the next month
        first_weekday = first_day.isoweekday()
        
        # calculate the offset to get the first occurrence of the given weekday
        offset = (weekday - first_weekday) % 7
        
        # add n - 1 weeks to get the nth occurrence of the given weekday
        nth_weekday = first_day + datetime.timedelta(days = offset + (n - 1) * 7)
    
    # return the next day that is the nth weekday of a month
    return nth_weekday

def get_next_nth_day_of_month(date, n):
    # get the current year and month
    year = date.year
    month = date.month
    
    # get the number of days in the current month
    days_in_month = calendar.monthrange(year, month)[1]
    
    # if n is 0, use the number of days in the month as n
    if n == 0:
        n = days_in_month
    
    # if n is larger than the number of days in the month, return None
    if n > days_in_month:
        return None
    
    # get the nth day of the current month
    nth_day = datetime.date(year, month, n)
    
    # if the nth day is before or equal to the given date, move to the next month
    if nth_day < date:
        # if the current month is December, move to the next year
        if month == 12:
            year += 1
            month = 1
        else:
            # otherwise, increment the month by one
            month += 1
        
        # get the number of days in the next month
        days_in_month = calendar.monthrange(year, month)[1]
        
        # if n is 0, use the number of days in the month as n
        if n == 0:
            n = days_in_month
        
        # if n is larger than the number of days in the next month, return None
        if n > days_in_month:
            return None
        
        # get the nth day of the next month
        nth_day = datetime.date(year, month, n)
    
    # return the next date that is the nth day of a month
    return nth_day

def get_next_date_by_weekday(date, weekday):
    # get the current weekday of the date
    current_weekday = date.isoweekday()
    # calculate the difference between the given weekday and the current weekday
    diff = (weekday - current_weekday) % 7
    
    # add the difference to the date to get the next date that is the given weekday
    next_date = date + datetime.timedelta(days = diff)
    
    # return the next date that is the given weekday
    return next_date

def next_date_matching_pattern(from_date, day_pattern, pattern, interval):
    print(day_pattern)
    if interval == "Yearly":
        year = from_date.year
        if pattern == "Month-Day":
            # Parse the day as a month and a day
            month, day = map(int, day_pattern.split("-"))
            # Get the year of the from_date
            
            # Create a new date object with the same month and day as the day parameter
            next_date = datetime.date(year, month, day)
            
        
        if pattern == "Month-Week-Day":
            month, week, day = map(int, day_pattern.split("-"))
            next_date = next_yearly_mwd(from_date, day, week, month)
            return next_date
        if pattern == "Month":
            month = int(day_pattern)
            day = 1
            next_date = datetime.date(year, month, day)
            return next_date
            
        if pattern == "Week":
            week = int(day_pattern)
            next_date = nth_week(year, week, 0)
            return next_date
        
        if pattern == "Week-Day":
            week, day = map(int, day_pattern.split("-"))
            next_date = nth_weekday(year, week, day)
            if next_date < from_date:
                next_date = nth_weekday(year+1, week, day)

        if pattern == "Day":
            day = int(day_pattern)
            next_date = nth_day(year,day)
            if next_date < from_date:
                next_date = nth_day(year + 1, day)
        
        if next_date < from_date:
            next_date = next_date.replace(year=year + 1)
        return next_date
    
    if interval == "Quarterly":
        if pattern == "Month-Week-Day":
            month, week, day = map(int, day_pattern.split("-"))
            next_date = next_quarterly_mwd(from_date, day, week, month)
            return next_date
        if pattern == "Day":           
            day = int(day_pattern)
            if day == 0:
                day = 1
                last = True
            else:
                last = False
            next_date = get_nth_day_of_quarter(from_date, day)
            if last:
                next_date = next_date - datetime.timedelta(days = 1)    
        else:
            next_date = get_nth_day_of_quarter(from_date, 1)
        return next_date
    if interval == "Monthly":
        if pattern == "Week-Day":
            week, day = map(int, day_pattern.split("-"))
            if week == 0:
                tomrrow = from_date + datetime.timedelta(days = 1)
                first_wd = get_next_monthly_wd(tomrrow, day, 1)
                next_date = first_wd - datetime.timedelta(days = 7)
                return next_date
            next_date = get_next_monthly_wd(from_date, day, week)
            return next_date
        if pattern == "Day":
            day = int(day_pattern)
            next_date = get_next_nth_day_of_month(from_date,day)
            return next_date
        else:
            next_date = get_next_nth_day_of_month(from_date,1)
            return next_date
    if interval == "Weekly":
        if pattern == "Day":
            day = int(day_pattern)
            next_date = get_next_date_by_weekday(from_date, day)
            return next_date
        else:
            next_date = get_next_date_by_weekday(from_date, 0)
            return next_date
    else:
        next_date = from_date
    return next_date


def next_date_matching_list(day_list, pattern, interval, from_date = datetime.date.today()):
    word_list = day_list.split(",")
    result_list = [next_date_matching_pattern(from_date,day_pattern, pattern, interval) for day_pattern in word_list]
    return sorted(result_list)


