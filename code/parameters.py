"""
Generates the parameters used in the emulation.

When run on 2017-09-28 20:21:00, the results are:

========== monitor112 ==========
% pings lost: 18.963952%
latency (ms): 300.8604161172856

========== monitor103 ==========
% pings lost: 0.768751%
latency (ms): 14.518184236276454
"""

import argparse

from influxdb import DataFrameClient
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument('user')
parser.add_argument('password')
parser.add_argument('database')
args = parser.parse_args()

influx = DataFrameClient(host=args.host,
                         port=443,
                         username=args.user,
                         password=args.password,
                         database=args.database,
                         ssl=True,
                         verify_ssl=True)

def get_pings_lost(monitor, time):
    query = "SELECT value FROM num WHERE home_id = 'deployment_011' AND entity_id = '{}_local_ping_packet_loss' AND time < now() AND time > now() - {}".format(monitor, time)
    data = influx.query(query)
    loss_data = data['num']

    query = "SELECT value FROM num WHERE home_id = 'deployment_011' AND entity_id = '{}_local_ping_total' AND time < now() AND time > now() - {}".format(monitor, time)
    data = influx.query(query)
    total_data = data['num']

    query = "SELECT value FROM num WHERE home_id = 'deployment_011' AND entity_id = '{}_local_ping_errors' AND time < now() AND time > now() - {}".format(monitor, time)
    data = influx.query(query)
    error_data = data['num']

    # Remove errors from total
    total_data = total_data['value'] - error_data['value']

    # Calculate the number of pings sent
    total_sent = total_data.sum()

    # Calculate the number of pings lost
    total_lost = loss_data.sum().value

    return total_lost / total_sent


def get_pings_latency(monitor, time):
    query = "SELECT MEAN(value) FROM ms WHERE home_id = 'deployment_011' AND entity_id = '{}_local_ping_latency' AND time < now() AND time > now() - {}".format(monitor, time)
    data = influx.query(query)
    return data['ms']['mean'].values[0]


TIME = '30d'

for monitor in ['monitor112', 'monitor103']:
    print("=" * 10, monitor, "=" * 10)

    lost = get_pings_lost(monitor, TIME)
    latency = get_pings_latency(monitor, TIME)

    print("% pings lost: {:%}".format(lost))
    print("latency (ms): {}".format(latency))
    print()
