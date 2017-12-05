#!/usr/bin/python3
import random as rand
import csv


# MessageType1 (start, after calibration) - calibrationFlexValue1 - calibrationFlexValue2 - calibrationFlexValue3 - pattern - endingByte
# MessageType2 (every cycle)  - Total millis since start - FlexSensorValue1 - FlexSensorValue2 - FlexSensorValue3 - endingByte


# How many times did the user have to be corrected?
# How long did it take before the user corrected itself (average of values)?
# How long did they maintain correct posture? (percentage of total time)

def main():
    # writeFileFunc('data.txt')
    data = read_file_func('data.txt')
    print(data[0])

    # This list contains all measurements of the flexSensors which are equal to or greater than the sensors values.
    correctedList = get_correct_values(data[1], data[0])

    # print(*correctedList, sep='\n')
    print(len(correctedList))
    # filtered = [x for x in set(data[1]) if x < C]

# How many times did the user has to be corrected?
# First we have to calculate how many correct values there are (values are > calibration value)
def get_correct_values(data_list, calibration_values):
    correctedList = []
    for item in data_list:
        if item[1] >= calibration_values[1] and item[2] >= calibration_values[2] and item[1] >= calibration_values[3]:
            correctedList.append(item)
    return correctedList


def read_file_func(file_name):
    calibrationValues = []
    sensorsValues = []
    data = []
    with open(file_name, encoding='utf8', buffering=1024) as inputFile:
        temp = False
        for line in csv.reader(inputFile, delimiter="\t"):
            if temp == False:
                calibrationValues = line
                temp = True
            else:
                sensorsValues.append(line)
        data.append(calibrationValues)
        data.append(sensorsValues)
    return data


def write_file_func(file_name):
    outFile = open(file_name, 'w')
    print('42', '\t', '55', '\t', '33', '\t', '3', file=outFile, end='\n')
    for x in range(0, 10000):
        print(rand.randint(1, 1512462370064), '\t', rand.randint(25, 120), '\t', rand.randint(30, 120), '\t',
              rand.randint(33, 120)
              , file=outFile, end='\n')


if __name__ == "__main__": main()
