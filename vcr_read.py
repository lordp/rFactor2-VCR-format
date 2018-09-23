import sys
from pathlib import Path
import os
from struct import unpack
from pprint import pprint
import json
import csv


class Driver:
    def __init__(self):
        self.number = 0
        self.name = ""
        self.co_driver = ""
        self.vehicle = ""
        self.vehicle_version = 0.0
        self.vehicle_id = ""
        self.vehicle_file = ""
        self.unknown = ""
        self.entry_time = 0.0
        self.exit_time = 0.0

        self.running = True
        self.detachable_part_state = 0
        self.last_detachable_part_state = 0
        self.in_pit = False
        self.in_garage = True
        self.garage_position = None
        self.first_loc_at = -1

    def driver_name(self):
        return self.name if self.name else 'Safety Car'


# header = b''
drivers = {}
session_types = {
    0: 'Test Day',
    1: 'Practice',
    2: 'Practice',
    3: 'Practice',
    4: 'Practice',
    5: 'Qualifying',
    6: 'Qualifying',
    7: 'Qualifying',
    8: 'Qualifying',
    9: 'Warmup',
    10: 'Race',
    11: 'Race',
    12: 'Race',
    13: 'Race',
}

bounds = {
    'min_x': 0,
    'max_x': 0,
    'min_y': 0,
    'max_y': 0,
    'min_z': 0,
    'max_z': 0,
}

penalties = {
    0: 'Stop/Go',
    1: 'Drive Thru'
}

pit_events = {
    32: 'exited pit lane',
    33: 'requested pit',
    34: 'entered pit lane',
    35: 'entered pit box',
    36: 'exited pit box',
}

checkpoints = {}


def format_time(seconds):
    minute, second = divmod(seconds, 60)
    if minute > 60:
        hour, minute = divmod(minute, 60)
        return '{h:0.0f}h{m:02.0f}m{s:06.3f}'.format(h=hour, m=minute, s=second)
    elif minute > 0:
        return '{m:0.0f}m{s:06.3f}'.format(m=minute, s=second)
    else:
        return '{s:0.3f}'.format(s=second)


def read_integer(file, length=4, signed=True):
    if length == 4:
        if signed:
            return unpack('i', file.read(length))[0]
        else:
            return unpack('I', file.read(length))[0]
    elif length == 2:
        return unpack('h', file.read(length))[0]
    elif length == 1:
        return unpack('b', file.read(length))[0]


def read_float(file):
    return unpack('f', file.read(4))[0]


def read_string(file, int_length=1, str_length=0):
    if str_length == 0:
        str_length = read_integer(file, int_length)
    string = file.read(str_length)

    return string.decode('utf-8')


def read_until(file, char):
    b = b''
    while True:
        read_byte = file.read(1)
        if read_byte != char:
            b = b + read_byte
        else:
            break
    return b


def debug(tag, evt_size, evt_type, evt_class, driver, file_pos):
    print(f"({tag}) size: {evt_size}, class: {evt_class}, type: {evt_type}, driver: {driver}, file: {file_pos}")


def read_driver_data(file, driver_id, slice_time):
    info1 = read_integer(file, signed=False)
    info2 = read_integer(file, signed=False)
    speed_info = binary_file.read(5)
    unknown = binary_file.read(25)
    info3 = read_integer(file, 1)
    x = read_float(binary_file)
    y = read_float(binary_file)
    z = read_float(binary_file)
    rot_x = read_float(binary_file)
    rot_y = read_float(binary_file)
    rot_z = read_float(binary_file)

    steer_yaw = info1 & 127
    throttle = info1 >> 11 & 63
    engine_rpm = info1 >> 18
    in_pit = (info1 >> 17 & 0x1) != 0

    detachable_part_state = info2 & 0x3ff

    if driver_id in drivers:
        driver = drivers[driver_id]
        if driver.running:
            if detachable_part_state != driver.detachable_part_state:
                driver.last_detachable_part_state = driver.detachable_part_state
                driver.detachable_part_state = detachable_part_state
                print(f'{drivers[driver_id].driver_name()} damaged part #{detachable_part_state} ({slice_time})')
            if in_pit != driver.in_pit:
                driver.in_pit = in_pit
                if driver.garage_position is None:
                    print(f'{drivers[driver_id].driver_name()} entered garage ({slice_time})')
            if driver.garage_position is None and driver.in_pit:
                driver.garage_position = (x, y, z)
                driver.in_garage = True
                driver.first_loc_at = slice_time
                print(f'Garage position set for {drivers[driver_id].driver_name()} ({slice_time})')
            if driver.garage_position is not None:
                in_garage = abs(x - driver.garage_position[0]) < 1 and \
                            abs(y - driver.garage_position[1]) < 1 and \
                            abs(z - driver.garage_position[2]) < 1
                if in_garage and not driver.in_garage:
                    print(f'{drivers[driver_id].driver_name()} pressed esc ({slice_time})')
                driver.in_garage = in_garage

    # print(x, y, z)
    if x < bounds['min_x']:
        bounds['min_x'] = round(x, 3)
    if bounds['max_x'] < x < 10000000000:
        bounds['max_x'] = round(x, 3)
    if y < bounds['min_y']:
        bounds['min_y'] = round(y, 3)
    if bounds['max_y'] < y < 10000000000:
        bounds['max_y'] = round(y, 3)
    if z < bounds['min_z']:
        bounds['min_z'] = round(z, 3)
    if bounds['max_z'] < z < 10000000000:
        bounds['max_z'] = round(z, 3)

    # if driver_id not in checkpoints:
    #     checkpoints[driver_id] = set()
    #
    # checkpoints[driver_id].add((round(x, 3), round(y, 3), round(z, 3), slice_time))


unknown_data = []
unknown_filenames = set()
# log_file = open(sys.argv[1].replace('Vcr', 'log'), 'w')
with open(sys.argv[1], "rb") as binary_file:
    binary_file.seek(0)
    header = read_until(binary_file, b'\n')

    irsr = binary_file.read(4)
    version = read_float(binary_file)

    rfm = read_string(binary_file, 4)

    unknown1 = read_integer(binary_file)

    mod_info = read_string(binary_file, 4)
    scene_info = read_string(binary_file, 4)
    aiw_info = read_string(binary_file, 4)
    mod_name = read_string(binary_file, 2)
    mod_version = read_string(binary_file, 2)
    mod_uid = read_string(binary_file, 2)
    track_path = read_string(binary_file, 2)

    unknown2 = binary_file.read(1)
    session_info = read_integer(binary_file, 1)
    # log_file.write(f"Session Type: {session_types.get(session_info & 0xF)}\n")
    # log_file.write(f"Private Session: {True if session_info >> 7 & 1 else False}\n")

    unknown3 = binary_file.read(67)

    number_of_drivers = read_integer(binary_file)
    # log_file.write(f"{number_of_drivers} drivers\n")
    for _ in range(0, number_of_drivers):
        num = read_integer(binary_file, 1)
        if num not in drivers:
            drivers[num] = Driver()

        drivers[num].number = num
        drivers[num].name = read_string(binary_file)
        drivers[num].co_driver = read_string(binary_file)
        drivers[num].vehicle = read_string(binary_file, 2)
        drivers[num].vehicle_version = read_string(binary_file, 2)
        drivers[num].vehicle_id = read_string(binary_file, 2)
        drivers[num].vehicle_file = binary_file.read(32).partition(b'\0')[0]
        drivers[num].unknown = binary_file.read(48)
        drivers[num].entry_time = read_float(binary_file)
        drivers[num].exit_time = read_float(binary_file)

        print(f'#{num}: {drivers[num].driver_name()}')

    # for i, d in drivers.items():
    #     print(f'{i}: {d.name}')
    #     print(f'{i}: {d.vehicle}')
    #     print(f'{i}: {d.vehicle_id}')
    #     print(f'{i}: {d.vehicle_version}')
    #     print(f'{i}: {d.vehicle_file}')
    # exit()

    time_slice_count = read_integer(binary_file)
    total_event_count = read_integer(binary_file)
    start_time = read_float(binary_file)
    end_time = read_float(binary_file)

    slices = {}

    print(f"{time_slice_count} time slices")
    for n in range(0, time_slice_count):
        if n not in slices:
            slices[n] = {}

        # log_file.write(f"----------------------\nFile location: {binary_file.tell()}\n")
        slice_time = read_float(binary_file)
        event_count = read_integer(binary_file, 2, signed=False)
        if event_count > 1000:
            break
        # log_file.write(f"Time slice #{n} ({slice_time}) has {event_count} events\n")
        # print(f"----------------------\nTime slice #{n} ({slice_time}) has {event_count} events\n")

        for m in range(0, event_count):
            # log_file.write(f"----------------------\nEvent #{m}\n----------------------\n")
            event_header = read_integer(binary_file, signed=False)
            # log_file.write("header: {0:x}\n".format(event_header))

            event_size = (event_header >> 8) & 0x1ff
            event_class = (event_header >> 29)
            event_type = (event_header >> 17) & 0x3f
            event_driver = event_header & 0xff
            # log_file.write("size: {}\n".format(event_size))
            # log_file.write("class: {}\n".format(event_class))
            # log_file.write("type: {}\n".format(event_type))
            # log_file.write("driver: {}\n".format(event_driver))

            wut = binary_file.read(1)
            current_file_pos = binary_file.tell()
            next_file_pos = current_file_pos + event_size
            if event_driver in drivers:
                driver_name = drivers[event_driver].driver_name()

            data = binary_file.read(event_size)
            unknown_data.append([slice_time, event_size, event_class, event_type, event_driver, data])
            unknown_filenames.add(f'{event_class}_{event_type}')
            binary_file.seek(current_file_pos)

            # print(binary_file.tell())
            if event_class == 0 and event_type >= 7 and event_type <= 16:
                # debug("Not Driver", event_size, event_type, event_class, event_driver, current_file_pos)
                read_driver_data(binary_file, event_driver, slice_time)
            elif event_class == 1 and event_type in [7, 10, 23]:
                if event_type == 7:
                    timestamp = read_float(binary_file)
                    # print(f'{driver_name} entered/exited their garage ({timestamp} / {slice_time})')
                if event_type == 10:
                    # debug("Lights", event_size, event_type, event_class, event_driver, current_file_pos)
                    num_lights = read_integer(binary_file, 1)
                    if 1 <= num_lights <= 6:
                        print(f"Lights: {num_lights} ({slice_time})")
                    binary_file.read(2)
                    current_file_pos = binary_file.tell()
                if event_type == 23:
                    countdown_value = read_integer(binary_file, 4)
                    print(f'Countdown: {countdown_value} ({slice_time})')
            elif event_class == 2 and event_type in [5, 7, 8]:
                if event_type == 5:
                    penalty_given_id = read_integer(binary_file, 1)
                    penalty_unknown = read_integer(binary_file, 2)
                    penalty_text = read_string(binary_file, str_length=event_size - 3)
                    print(f'{driver_name} given penalty - "{penalty_text}" [{penalty_given_id}/{penalty_unknown}] ({slice_time})')
                if event_type == 7:
                    penalty_type = read_integer(binary_file, 1)
                    print(f'{driver_name} served {penalties[penalty_type]} penalty ({slice_time})')
                if event_type == 8:
                    penalty_type = read_integer(binary_file, 1)
                    print(f'Admin removed {penalties[penalty_type]} penalty from {driver_name} ({slice_time})')
                if event_type == 16:
                    unknown = binary_file.read(event_size)
                if event_type == 19:
                    session_type = read_string(binary_file, str_length=4)
                    print(f'Session type: {session_type}')
            elif event_class == 3 and event_type in [6, 15, 48, 49]:
                # debug("Class 3", event_size, event_type, event_class, event_driver, current_file_pos)
                if event_type == 6:  # Checkpoint event
                    cp_laptime = read_float(binary_file)
                    cp_time = read_float(binary_file)
                    cp_lap = read_integer(binary_file, 1)
                    cp_raw = read_integer(binary_file, 1)
                    cp_sector = ((cp_raw >> 6) & 3)
                    # print(f"Lap: {cp_lap}, Sector: {cp_sector}, Time: {cp_laptime} ({slice_time})")
                    binary_file.read(event_size - 10)
                elif event_type == 15:  # Garage event
                    # print(f'Garage event ({slice_time})')
                    binary_file.read(5)
                elif event_type == 16:  # DNF event
                    print(f'DNF event ({slice_time})')
                    binary_file.read(event_size)
                elif event_type == 18:  # DSQ event
                    print(f'DSQ event ({slice_time})')
                    binary_file.read(event_size)
                elif event_type == 19 and event_driver != 255:  # KICK event
                    print(f'KICK event {driver_name} ({slice_time})')
                    binary_file.read(event_size)
                elif event_type == 5:  # Rank event
                    print(f'Rank event #1 ({slice_time})')
                    print(event_size)
                    binary_file.read(10)
                    info = binary_file.read(event_size - 10)
                    print(info)
                elif event_type == 38:  # Unknown event
                    # print(f'Rank event #2 ({slice_time})')
                    # driver_id = binary_file.read(1)
                    # binary_file.read(21)
                    # driver_name = read_string(binary_file)
                    # driver_id = binary_file.read(1)
                    # info = bytearray(binary_file.read(event_size - 21))
                    binary_file.read(event_size)
                elif event_type == 48:  # Rank event
                    # print(f'Rank event #2 ({slice_time})')
                    binary_file.read(21)
                    info = bytearray(binary_file.read(event_size - 21))
                    # binary_file.read(event_size)
                elif event_type == 49:  # Pit event
                    pit_event = read_integer(binary_file, 1)
                    # if pit_event == 3:
                    #     print(f"{driver_name} entered pit lane ({slice_time})")
                    # elif pit_event == 4:
                    #     print(f"{driver_name} entered garage ({slice_time})")
                else:
                    # debug("Wut", event_size, event_type, event_class, event_driver, current_file_pos)
                    binary_file.read(event_size)
            elif event_class == 5 and event_type == 2:
                if event_type == 2:
                    # pit lane events - request pit, enter lane, on jacks, off jacks, exit lane
                    pit_event = read_integer(binary_file, 1)
                    if pit_event == 36:
                        pit_data = binary_file.read(event_size - 1)  # unknown data, maybe fuel, damage repaired, something else
                        print(f'{driver_name} {pit_data} [{event_size}] ({slice_time})')
                    event_desc = pit_events.get(pit_event, pit_event)
                    # print(f'{driver_name} {event_desc} [{pit_event}/{event_size}] ({slice_time})')
            else:
                # debug("Unknown Class/Type", event_size, event_type, event_class, event_driver, current_file_pos)
                data = binary_file.read(event_size)
            #     unknown_data.append([slice_time, event_size, event_class, event_type, event_driver, data])
            #     unknown_filenames.add(f'{event_class}_{event_type}')

            current_file_pos = binary_file.tell()
            if current_file_pos != next_file_pos:
                diff = binary_file.tell() - next_file_pos
                debug("ERROR!", event_size, event_type, event_class, event_driver, diff)
                binary_file.seek(next_file_pos)
                exit()

# pprint(drivers)
# log_file.close()
# ud = sorted(unknown_data, key=lambda row: row[0])  # slice time
# ud = sorted(ud, key=lambda row: row[1])  # size
# ud = sorted(ud, key=lambda row: row[3])  # type
# ud = sorted(ud, key=lambda row: row[2])  # class

unknown_data_directory = Path(sys.argv[2])
if not unknown_data_directory.is_dir():
    os.mkdir(unknown_data_directory)

files = {k:open(f'{unknown_data_directory}/{k}.csv', 'w+', newline='') for k in unknown_filenames}

for row in unknown_data:
    if row[1] > 0:
        csv_data = csv.writer(files[f'{row[2]}_{row[3]}'])
        csv_data.writerow(row)

for k in unknown_filenames:
    if k in files:
        files[k].close()

# print(bounds)
# for d in checkpoints:
#     checkpoints[d] = list(checkpoints[d])
#
# with open('checkpoints.json', 'w') as outfile:
#     json.dump(checkpoints[20], outfile)
# with open('slices.csv', 'w') as outfile:
#     w = csv.writer(outfile)
#     for row in slices:
#         w.writerow(slices[row])
