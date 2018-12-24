#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing modules
import csv
import sys

FILE1 = sys.argv[1]
FILE2 = sys.argv[2]

#FILE1 = '/home/svoronov/Загрузки/ping188.225.27.13_ix.csv'
#FILE2 = '/home/svoronov/Загрузки/ping188.225.27.13_noix.csv'


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_length(file):
    with open(file) as f:
        fileobject = csv.reader(f)
        return sum(1 for i in fileobject) - 1


def get_data(file, column):
    return_list = []
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            return_list.append(row[column])
            #avr_list.append(float(row['RTT (сред.), мс.'].replace(',', '.')))
    return return_list


def compare(avg1, avg2, cities, row_count):
    for i in range(row_count):
        try:
            if float(avg1[i].replace(',', '.')) >= float(avg2[i].replace(',', '.')):
                print(cities[i] + ' '*5 + BColors.FAIL + avg1[i] + BColors.ENDC +
                ' '*5 + BColors.OKGREEN + avg2[i] + BColors.ENDC)
            else:
                print(cities[i] + ' '*5 + BColors.OKGREEN + avg1[i] + BColors.ENDC +
                ' '*5 + BColors.FAIL + avg2[i] + BColors.ENDC)
        except:
            continue


def write_to_csv(avg1, avg2, cities, row_count):
    data = ['']
    data[0] = ['Точка мониторинга', 'Среднее значение с MSK-IX', 'Среднее значение без MSK-IX']
    for i in range(1, row_count):
        data.append([cities[i], avg1[i], avg2[i]])
    filename = 'Comparison_for_' + get_data(FILE1, 'IP')[1] + '.csv'
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


def main():
    cities_of_checkout = get_data(FILE1, 'Точка мониторинга')
    averages_file1 = get_data(FILE1, 'RTT (сред.), мс.')
    averages_file2 = get_data(FILE2, 'RTT (сред.), мс.')
    row_count = get_length(FILE1)
    #if sys.argv[3]: #== '-w':
        #write_to_csv(averages_file1, averages_file2, cities_of_checkout, row_count)
    #else:
    compare(averages_file1, averages_file2, cities_of_checkout, row_count)


# START THE PROGRAM
if __name__ == "__main__":
    main()