import datetime as dt

from collections import defaultdict, Counter


log = []
with open('input_data') as in_f:
    for row in in_f:
        timestamp, action = row.strip().split(']')
        _time = dt.datetime.strptime(timestamp[1:], "%Y-%m-%d %H:%M")

        log.append((_time, action.strip()))

log.sort()

guard_id = None
start = None
sleep_time = None
sum_sleep = defaultdict(int)
sleep_periods = defaultdict(list)
for _time, action in log:

    if 'Guard' in action:
        guard_id = action.split()[1]
        start = None

    if 'falls' in action:
        start = _time

    if 'wakes' in action:
        sleep_time = int((_time - start).total_seconds() / 60.0)
        start_minute = start.minute

        sum_sleep[guard_id] += sleep_time
        sleep_periods[guard_id].append([start_minute + i for i in range(sleep_time)])

lazy_guard = sorted(sum_sleep.items(), key=lambda x: -x[1])[0]

sleep_pattern = Counter(minute for night in sleep_periods[lazy_guard[0]] for minute in night)
quiet_minute = sleep_pattern.most_common(1)[0][0]

plan = int(lazy_guard[0][1:]) * quiet_minute

all_quiet_minutes = []
for guard, sleep_patterns in sleep_periods.items():
    sleep_pattern = Counter(minute for night in sleep_patterns for minute in night)
    quiet_minute, times = sleep_pattern.most_common(1)[0]
    all_quiet_minutes.append((guard, quiet_minute, times))

laziest_guard, quiet_minute, zzz_times = sorted(all_quiet_minutes, key=lambda x: -x[2])[0]
second_plan = int(laziest_guard[1:]) * quiet_minute

print(f'P4-1: {plan}')
print(f'P4-2: {second_plan}')
