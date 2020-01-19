import datetime

def calc_diff(last_week, today):
    lw = datetime.datetime.strptime(last_week, '%H:%M')
    t = datetime.datetime.strptime(today, '%H:%M')
    delta_min = abs((t - lw).total_seconds() / 60)

    if delta_min == 0:
        return '-'

    prefix = '+'

    # this is a funny hack
    if datetime.datetime.now().month > 7:
        prefix = '-'

    stringified = str(int(delta_min))

    return "{}{}".format(prefix, stringified)
