import sys
from datetime import date, timedelta
import logging

logging.basicConfig(level=logging.DEBUG)

def clean_inputs(film_title, screening_start_date):
    film_title = film_title.replace('_', ' ').title()
    logging.debug("Film title:" + film_title)
    
    start_month, start_day, start_year = screening_start_date.split('/')
    start_date = date(int(start_year), int(start_month), int(start_day))
    logging.debug('Film title: {}, start_date: {}'.format(film_title, start_date))
    return film_title, start_date

def retrieve_showtime_template(time_type):
    # PULL FILM TIME TEMPLATES FROM EXT FILE FROM SYS ARG
    if time_type == 'n':
        filename = 'normal_times'
    elif time_type == 'k':
        filename = 'kids_times'
    elif time_type == 'e':
        filename = 'extended_times'
    else:
        pass
    
    days_of_week = {'monday': 0,
                'tuesday': 1,
                'wednesday':2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6}
        
    with open(filename + ".txt") as f:
        current_time_template = {}
        for num, line in enumerate(f):
            day_data = line.split(',')
            day_data = [x.strip() for x in day_data]
            current_time_template[days_of_week[day_data[0].lower()]] = day_data[1:]
        return current_time_template

def retrieve_all_dates(starting_date, weeks_running):
    """ Gets a list if all dates in the range of start date for the number of weeks"""
    one_day = timedelta(days=1)
    show_dates = []
    current_day = starting_date

    while len(show_dates) < weeks_running * 7:
        show_dates.append(current_day)
        current_day += one_day
    return show_dates


def parse_screening_days(all_dates, screening_template):
    """ Determines what the screening dates are using the times template data and retreieved dates"""
    play_dates = {}
    for date in all_dates:
        if date.weekday() in screening_template:
            formatted_date = date.strftime("%m/%d/%y")
            play_dates[formatted_date]=screening_template[date.weekday()]
    logging.debug(play_dates)
    return play_dates


# TODO: FORMAT TXT FOR SUBMISSION
def format_text(film_title, dates_and_times):
    text = """
Hurleyville Arts Centre Cinema
219 Main Street
Hurleyville, NY
12747
845-707-8047

Film:
{title}
            
showtimes:
            
""".format(title=film_title)
    
    showtimes = ''
    
    for date, times in dates_and_times.items():
        showtimes += '{} : {} \n'.format(date, times)
    formatted_text = text + showtimes
    logging.debug(formatted_text)
    return formatted_text
    
    
def copy_to_clipboard(formatted_text):
    """Copys the final formatted text to clipboard"""
    logging.info("copying formatted text to clipboard...")
    # if OS is MacOS
    #pyperclip.copy(formatted_text)
    #if OS is iOS
    clipboard.set(formatted_text)
        

def generate_text_form(film_title, time_template, start_date, num_weeks):
    clean_title, clean_start_date = clean_inputs(film_title, start_date)
    screenings_template = retrieve_showtime_template(time_template)
    all_dates = retrieve_all_dates(clean_start_date, num_weeks)
    playing_dates = parse_screening_days(all_dates, screenings_template)
    formatted_text = format_text(clean_title, playing_dates)
    copy_to_clipboard(formatted_text)


if __name__ == '__main__':
    film_title = sys.argv[1]
    time_template = sys.argv[2]
    start_date = sys.argv[3]
    num_weeks = int(sys.argv[4])
    
    generate_text_form(film_title, time_template, start_date, num_weeks)
