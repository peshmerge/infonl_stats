#!/usr/bin/python3
import random as rand
import csv


# MessageType1 (start, after calibration)
#  - calibrationFlexValue1 - calibrationFlexValue2 - calibrationFlexValue3 - pattern - endingByte
# MessageType2 (every cycle)  -
# Total millis since start - FlexSensorValue1 - FlexSensorValue2 - FlexSensorValue3 - endingByte

# How many times did the user has to be corrected?
# How long did it take before the user corrected him/herself (average of values)?
# How long did they maintain correct posture? (percentage of total time)
from jsonschema._validators import pattern

pattern1 = [-20, 20]
pattern2 = [-35, 35]
pattern3 = [-35, 35]

def main():
    # writeFileFunc('data.txt')

    with open('data/p3/results_p3.txt', 'w') as out_file:
        for i in range(1,14):
            print("User",str(i), file=out_file, end='\n')
            data = read_file_func("data/p3/USER_"+str(i)+"_PATTERN_3.csv")
            corrected_times = get_correct_values(data[1], data[0])
            correct_posture_duration = get_time_of_maintaining_correct_posture(data[1], data[0])
            print("How many times the user has to be corrected per flex Sensor?", file=out_file, end='\n')
            print("\tFlex sensor#1=", corrected_times[0], file=out_file, end='\n')
            print("\tFlex sensor#2=", corrected_times[1], file=out_file, end='\n')
            print("\tFlex sensor#3=", corrected_times[2], file=out_file, end='\n')
            print("", file=out_file)
            print("How long did it take before the user corrected him/herself (average of values)?", file=out_file, end='\n')
            print("\t",get_time_before_correction(data[1], data[0]), file=out_file, end='\n')
            print("", file=out_file)
            print("How long did they maintain correct posture? (percentage of total time)", file=out_file, end='\n')
            print("\t",round(correct_posture_duration, 4), file=out_file, end='\n')

            print("\n \n", file=out_file, end='\n')
# How long did it take before the user corrected him/herself (average of values)?
def get_time_before_correction(data_list, calibration_values):
    started = True
    correction_flex_sensor_1 = [False, False]
    correction_flex_sensor_2 = [False, False]
    correction_flex_sensor_3 = [False, False]

    time_list_1 = []
    time_list_2 = []
    time_list_3 = []
    # Loop through the data list to be able to collect the needed data
    data_list_counter = 1
    for item in data_list:
        if data_list_counter == len(data_list):
            if correction_flex_sensor_1[0]:
                time_list_1[-1] = [time_list_1[-1][0], item[0], item[0] - time_list_1[-1][0]]

            if correction_flex_sensor_2[0]:
                time_list_2[-1] = [time_list_2[-1][0], item[0], item[0] - time_list_2[-1][0]]

            if correction_flex_sensor_3[0]:
                time_list_3[-1] = [time_list_3[-1][0], item[0], item[0] - time_list_3[-1][0]]
        else:
            if item[1] > pattern2[0] or item[1] < pattern2[1]:
                if correction_flex_sensor_1[0] == False:
                    time_list_1.append([item[0], 0, 0])
                    correction_flex_sensor_1 = [True, False]

            else:
                if correction_flex_sensor_1[0]:
                    correction_flex_sensor_1 = [False, False]
                    time_list_1[-1] = [time_list_1[-1][0], item[0], item[0] - time_list_1[-1][0]]

            if item[2] > pattern2[0] or item[2] < pattern2[1]:
                if correction_flex_sensor_2[0] == False:
                    time_list_2.append([item[0], 0, 0])
                    correction_flex_sensor_2 = [True, False]

                else:
                    if correction_flex_sensor_2[0]:
                        correction_flex_sensor_2 = [False, False]
                        time_list_2[-1] = [time_list_2[-1][0], item[0], item[0] - time_list_2[-1][0]]

            if item[3] > pattern2[0] or item[3] < pattern2[1]:
                if correction_flex_sensor_3[0] == False:
                    time_list_3.append([item[0], 0, 0])
                    correction_flex_sensor_3 = [True, False]

                else:
                    if correction_flex_sensor_3[0]:
                        correction_flex_sensor_3 = [False, False]
                        time_list_3[-1] = [time_list_3[-1][0], item[0], item[0] - time_list_3[-1][0]]
            data_list_counter += 1

    time_sum_1 = 0
    time_sum_2 = 0
    time_sum_3 = 0
    for time_item in time_list_1:
        time_sum_1 += time_item[2]

    for time_item in time_list_2:
        time_sum_2 += time_item[2]

    for time_item in time_list_3:
        time_sum_3 += time_item[2]


    return_value=[
        time_sum_1 / len(time_list_1) if len(time_list_1) else 0,
        time_sum_2 / len(time_list_2) if len(time_list_2) else 0,
        time_sum_3 / len(time_list_3) if len(time_list_3) else 0
        ]


    return round((return_value[0]+return_value[1]+return_value[2])/3,3)



# How long did they maintain correct posture? (percentage of total time)
def get_time_of_maintaining_correct_posture(data_list, calibration_values):
    """
    :param data_list
    :param calibration_values
    """

    # These are data_list_counter variables which will hold the frequency of how many times a user has been
    # corrected withing
    # a session
    # These arrays holds logical values which work as helpers to calculate the frequency
    correction_flex_sensor = [False, False]

    correct_posture_duration = 0

    time_list = []

    # Loop through the data list to be able to collect the needed data
    data_list_counter = 1
    for item in data_list:
        if data_list_counter == len(data_list):
            if correction_flex_sensor[0]:
                time_list[-1] = [time_list[-1][0], item[0], item[0] - time_list[-1][0]]
        else:
            # Check if it's incorrect posture
            if (item[1] < pattern2[0] or item[1] > pattern2[1]) and (item[2] < pattern2[0] or item[2] > pattern2[1]) \
                    and item[3] < pattern2[0] or item[3] > pattern2[1]:
                if correction_flex_sensor[0] == False:
                    time_list.append([item[0], 0, 0])
                correction_flex_sensor = [True, False]

            else:
                if correction_flex_sensor[0]:
                    # correction_flex_sensor = [True, True]
                    correction_flex_sensor = [False, False]
                    time_list[-1] = [time_list[-1][0], item[0], item[0] - time_list[-1][0]]
            data_list_counter += 1

    # Calculate the time (duration of how long the user maintained a correct posture)
    for time_item in time_list:
        correct_posture_duration = correct_posture_duration + time_item[2]

    total_time = data_list[-1][0]-data_list[0][0]
    return correct_posture_duration /total_time


# How many times did the user has to be corrected?
def get_correct_values(data_list, calibration_values):
    """
    How many times did the user has to be corrected?
    :type data_list: object
    :param data_list: a list of time in milliseconds and three flexSensors values
    :param calibration_values: the calibration values which must be captured at the beginning.
    """

    # These are temp variables which will hold the frequency of how many times a user has been corrected withing
    # a session
    correction_frequency_1 = 0
    correction_frequency_2 = 0
    correction_frequency_3 = 0

    # These arrays holds logical values which work as helpers to calculate the frequency
    correction_flex_sensor_1 = [False, False]
    correction_flex_sensor_2 = [False, False]
    correction_flex_sensor_3 = [False, False]

    # Loop through the data list to be able to collect the needed data
    for item in data_list:
        if item[1] < pattern2[0] or item[1] > pattern2[1]:
            correction_flex_sensor_1 = [True, False]
        else:
            if correction_flex_sensor_1[0]:
                correction_flex_sensor_1 = [False, False]
                correction_frequency_1 += 1

        if item[2] < pattern2[0] or item[1] > pattern2[1]:
            correction_flex_sensor_2 = [True, False]
        else:
            if correction_flex_sensor_2[0]:
                correction_flex_sensor_2 = [False, False]
                correction_frequency_2 += 1

        if item[3] < pattern2[0] or item[1] > pattern2[1]:
            correction_flex_sensor_3 = [True, False]
        else:
            if correction_flex_sensor_3[0]:
                correction_flex_sensor_3 = [False, False]
                correction_frequency_3 += 1

        # correctedList.append(item)

    return [correction_frequency_1, correction_frequency_2, correction_frequency_3]


def read_file_func(file_name):
    calibration_values = []
    sensors_values = []
    data = []
    with open(file_name, encoding='utf8', buffering=1024) as inputFile:
        temp = False
        for line in csv.reader(inputFile, delimiter=","):
            if temp == False:
                calibration_values = [int(i) for i in line]
                temp = True
            else:
                sensors_values.append([int(i) for i in line])
        data.append(calibration_values)
        data.append(sensors_values)
    return data


def write_file_func(file_name):
    outFile = open(file_name, 'w')
    print('42', '\t', '55', '\t', '33', '\t', '3', file=outFile, end='\n')
    for x in range(0, 10000):
        print(rand.randint(1, 1512462370064), '\t', rand.randint(25, 120), '\t', rand.randint(30, 120), '\t',
              rand.randint(33, 120)
              , file=outFile, end='\n')


if __name__ == "__main__": main()
