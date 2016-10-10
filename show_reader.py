# -*- coding: utf-8 -*-
import datetime
import os
from subprocess import call
from multiprocessing import Process
import time
import codecs
import jinja2
import traceback
import sys

from visual import show as pg_show
from visual import plot

PY_INTERFACE = 'py_interface.dat'
OUT_FILE = 'out' + os.path.sep + 'out_{0}_{1}.dat'
PERIOD = 0.004
ENERGY_COEFF = 278

TABLE_TEMPLATE = 'table_template.html'
EMPTY_TEMPLATE = 'empty_template.html'
TEAMS_TEMPLATE = 'teams_template.html'
PRICE_TEMPLATE = 'price_template.html'
SHOW_TEMPLATE = 'new_show_template.html'
MAX_POWER_TEMPLATE = 'max_power_template.html'
MIN_COST_TEMPLATE = 'min_cost_template.html'
TOP_PROFIT_TEMPLATE = 'top_profit_template.html'

MAX_POWER = 0.03
POWER_PRICE = 40
PODSTAVA = 1.5

PG_DATA_FILE = os.path.join(os.path.dirname(__file__), 'visual', 'config')

IDLE = False

DEBUG = False

TEAMS = {
    '1': {
        'name': u'Китайская установка «Мао Цзедун»',
        'cost': 5000,
        'power': 53.4,
    },
    '2': {
        'name': u'Тестовая команда 2',
        'cost': 5050,
        'power': 1130,
    },
    '3': {
        'name': u'Тестовая команда 3',
        'cost': 3000,
        'power': 910,
    },
    '4': {
        'name': u'foobar',
        'cost': 3000,
        'power': 910,
    },
    '5': {
        'name': u'Тестовая команда 5',
        'cost': 3000,
        'power': 910,
    },
    '6': {
        'name': u'Тестовая команда 6',
        'cost': 3000,
        'power': 910,
    },
    # '7': {
    #     'name': u'Тестовая команда 3',
    #     'cost': 3000,
    #     'power': 910,
    # },
    # '8': {
    #     'name': u'Тестовая команда 3',
    #     'cost': 3000,
    #     'power': 910,
    # },
    # '9': {
    #     'name': u'Тестовая команда 3',
    #     'cost': 3000,
    #     'power': 910,
    # },
    # '10': {
    #     'name': u'Тестовая команда 3',
    #     'cost': 3000,
    #     'power': 910,
    # },
}

RESISTANCE =1.2
        #На прошлом запуске RESISTANCE=0.47

def get_profit(power, cost):
    if power == '' or cost == '':
        return ''
    return str(round(float(power) * POWER_PRICE - float(cost), 2)) + u' руб'

def render_template(template, **kwargs):
    #print(kwargs)
    loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates'))
    env = jinja2.Environment(loader=loader)
    env.globals.update(get_profit=get_profit)
    template = env.get_template(template)

    with codecs.open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output', 'hardcode.html'), 'wb', 'utf-8') as f:
        f.write(template.render(**kwargs))

def render_table(team_name, power, cost, time):
    print(time)
    render_template(TABLE_TEMPLATE, team_name=team_name, power=power, cost=cost, time=time)

def render_empty():
    render_template(EMPTY_TEMPLATE)

def run_cpp():
    call('ReadData.exe')

def _show():
    pg_show.main()

def battery_picture(team, val):
    with open(PG_DATA_FILE, 'w') as f:
        f.write('\n'.join([team.encode('utf8'), str(val)]))

def read_data(team_id='dry', podstava=False):
    pointer = 0
    power = 0

    points = []
    cumulative = []

    if os.path.isfile(PY_INTERFACE):
        os.remove(PY_INTERFACE)
    # if os.path.isfile(OUT_FILE.format(team_id)):
        # os.remove(OUT_FILE.format(team_id))

    with open(PY_INTERFACE, 'w'):
        pass
    cpp = Process(target=run_cpp)
    err = ''
    now = datetime.datetime.now().strftime('%d-%m-%y %X').replace(':', '-')
    try:
        with open(OUT_FILE.format(team_id, now), 'w') as outf:
            outf.write('count\tvoltage\tpower\tenergy\n')
            cpp.start()
            now = time.time() + 10
            start_time = None
            update_time = None
            point_energy = 0
            while True:
                with open(PY_INTERFACE, 'r') as f:
                    info = f.readlines()
                    info = info[2:]
                    if len(info) > pointer + 1:
                        curinfo = info[pointer:-1]
                        for i, volt in enumerate(curinfo):
                            point_energy = (float(volt) ** 2 / RESISTANCE) * PERIOD * ENERGY_COEFF
                            if podstava:
                                point_energy *= PODSTAVA
                            power += point_energy
                            battery_picture(TEAMS[team_id]['name'], power)
                            points.append(point_energy)
                            cumulative.append(power)
                            outf.write('{p}\t{v}\t{pe}\t{power}\n'.format(p=(pointer + i + 1), v=volt.strip(), pe=point_energy, power=power))
                        pointer = len(info) - 1
                        now = time.time()
                    cur_time = time.time()
                    if point_energy > 0.001:
                        if start_time is None:
                            start_time = time.time()
                            update_time = time.time()
                    if update_time is not None:
                        if cur_time - update_time >= 1:
                            update_time = cur_time
                            render_table(TEAMS[team_id]['name'], power, TEAMS[team_id]['cost'], int(cur_time - start_time))
                    if cur_time - now > 1:
                        break
    except Exception as e:
        print('Fuck you')
        err = e
    finally:
        cpp.join()
        print('======================')
        print(power)
        print(err)
        # raw_input('<>')
        plot.plot(points, cumulative, TEAMS[team_id]['name'])
        return(power)


def show():
    while True:
        comm = raw_input('show --> ')
        if comm == '0':
            render_template(PRICE_TEMPLATE, cost=POWER_PRICE)
        elif comm == '1':
            rows = [{'place': '', 'name': v['name'], 'cost': round(v['cost'], 2), 'power': '', 'id': k} for k, v in TEAMS.iteritems()]
            rows = sorted(rows, key=lambda me: int(me['id']), reverse=False)
            render_template(SHOW_TEMPLATE, rows=rows)
        elif comm == '2':
            rows = [{'place': '', 'name': v['name'], 'cost': round(v['cost'], 2), 'power': round(v['power'], 2), 'id': k} for k, v in TEAMS.iteritems()]
            rows = sorted(rows, key=lambda me: int(me['id']), reverse=False)
            render_template(SHOW_TEMPLATE, rows=rows)
        elif comm == '3':
            rows = [{'place': '', 'name': v['name'], 'cost': round(v['cost'], 2), 'power': round(v['power'], 2), 'id': k} for k, v in TEAMS.iteritems()]
            rows = sorted(rows, key=lambda me: get_profit(float(me['power']), float(me['cost'])), reverse=True)
            place = 1
            for row in rows:
                row['place'] = place
                place += 1
            render_template(SHOW_TEMPLATE, rows=rows)
        elif comm == 'clear':
            render_empty()
        elif comm == 'fi':
            return
        else:
            print('Unknown command.')


def main(dry_run=False):
    if not dry_run:
        s = Process(target=_show)
        s.start()
        battery_picture('', '0')
    try:
        while True:
            try:
                comm = raw_input('--> ')
                if comm == 'restart':
                    s.join()
                    del(s)
                    s = Process(target=_show)
                    s.start()
                elif comm.startswith('r'):
                    team_params = comm.split(' ')
                    if len(team_params) < 2:
                        print('Tell me the team id.')
                        continue
                    team_id = team_params[1]
                    if team_id not in TEAMS:
                        print('No such team.')
                        continue
                    render_table(TEAMS[team_id]['name'], 0, TEAMS[team_id]['cost'], 0)
                    battery_picture(TEAMS[team_id]['name'], '0')
                    raw_input('Press ENTER:')
                    power = read_data(team_id, podstava=('!' in team_params))
                    TEAMS[team_id]['power'] = power

                elif comm == 'show':
                    render_empty()
                    show()
                elif comm == 'clear':
                    battery_picture('', '0')
                    render_empty()
                elif comm == 'fi':
                    battery_picture('fi', '0')
                    return
                else:
                    print('Unknown command.')
            except Exception as e:
                print('Something is wrong.')
                print(e)
                print(traceback.print_exc())
    finally:
        if not dry_run:
            s.join()


if __name__ == '__main__':
    dry_run = 'dry-run' in sys.argv
    main(dry_run)

