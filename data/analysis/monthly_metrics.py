import csv
from datetime import datetime
from datetime import timedelta
import statistics
import numpy as np


data = []
with open('data/csv/salesforce.csv') as csv_file:
    reader = csv.reader(csv_file)
    for i, line in enumerate(reader):
        # print(i, line)
        data.append(line)
historical_closed = []
historical_submissions = []
# start1, start2 = [datetime(2020, 12, 20), datetime(2021, 1, 3)]
# date_checks = []
# for i in range(39):
#     date_checks.append(
#         [start1 + timedelta(days=14*i),
#          start2 + timedelta(days=14*i)])
protocols_closed = []
time_to_close = []
new_submissions = []
date_checks = [[datetime(2021, 11, 1), datetime(2021, 11, 30)]]


def create_datetime(date_str):
    if date_str:
        date_str = date_str[:10]
        year, month, day = [int(val) for val in date_str.split('-')]
        return datetime(year, month, day)
    else:
        return None


data = [line for line in data[1:] if line[1]]
for line in data:
    status = line[6].lower()
    date_sub = create_datetime(line[2])
    id = line[1]
    historical_submissions.append(id)
    if status == 'closed':
        historical_closed.append(id)
        date_closed = create_datetime(line[3])
        author = line[7]
        if date_closed and date_closed >= date_checks[-1][0] and date_closed <= date_checks[-1][1]:
            protocols_closed.append({'id': id, 'author': author})
            # print(id, author)
            tat = line[4]
            time_to_close.append(tat)
    # print(date_sub)
    if date_sub >= date_checks[-1][0] and date_sub <= date_checks[-1][1]:
        new_submissions.append(id)


print(protocols_closed)
print(f'med: {statistics.median(time_to_close)}')

on_time = 0
for time in time_to_close:
    print(time)
    if time <= 14:
        on_time += 1
print(on_time)
print(len(protocols_closed), len(new_submissions))
# print(new_submissions)
# print(len(protocols_closed))
# for p in protocols_closed:
#     print('{')
#     for key, val in p.items():
#         print(f'\t{key}: {val}')
#     print('}')
# print(len(new_submissions))
# print(len(historical_closed))
# print(len(historical_submissions))
