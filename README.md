# schedule_generator
Film Screening Schedule Generator
auto detects schedule dates from a weekly template and creates and prints a schedule based on it

Cmd line args:

film_title: the full title of a film separated by underscores. Program will title and format for spaces
i.e. 'queen_and_slim' becomes "Queen and Slim",

time_template: (n,k,e) pulls from 3 sets of time templates, (normal, extended or kids films),
and generates dates based on weekday and time.

start_date: the first screening of the current run  
(format: MM/DD/YYYY),

num_weeks: the total number of weeks playing from the start date
