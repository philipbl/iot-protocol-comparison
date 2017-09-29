import json

import pyshark


def mqtt_stats(packets, num_data_points):
    packets = (p for p in packets if 'tcp' in p)  # Only TCP

    start_packet = None
    last_packet = None
    total_data_points = 0
    total_packets = 0
    total_bytes = 0

    for packet in packets:

        if 'mqtt' in packet:
            message_type = int(packet.mqtt.msgtype)

            # Look for connect packets
            if message_type == 1 and start_packet is None:
                start_packet = packet

            # Look for data points
            if message_type == 3:
                total_data_points += 1  # Keep track of data points seen so far
                last_packet = packet

        # Update stats
        total_packets += 1
        total_bytes += int(packet.length)

        if total_data_points >= num_data_points:
            start_time = float(start_packet.frame_info.time_epoch)
            end_time = float(last_packet.frame_info.time_epoch)

            return total_packets, total_bytes, end_time - start_time

    raise Exception("Not enough data points")


def mqtt_total_data_points(packets):
    packets = (p for p in packets if 'mqtt' in p)  # Get MQTT
    packets = (p for p in packets if int(p.mqtt.msgtype) == 3)  # Get PUB packets

    return sum(1 for _ in packets)


def coap_stats(packets, num_data_points):
    packets = (p for p in packets if 'coap' in p)  # Get CoAP

    start_packet = None
    last_packet = None
    total_data_points = 0
    total_packets = 0
    total_bytes = 0

    for packet in packets:
        message_type = int(packet.coap.type)

        # Look for CON packets
        if message_type == 0 and start_packet is None:
            start_packet = packet

        # Look for data points
        if message_type == 2:
            data = bytearray.fromhex(packet.coap.payload.raw_value)
            data = json.loads(data.decode())

            total_data_points += len(data)
            last_packet = packet

        # Update stats
        total_packets += 1
        total_bytes += int(packet.length)

        if total_data_points >= num_data_points:
            start_time = float(start_packet.frame_info.time_epoch)
            end_time = float(last_packet.frame_info.time_epoch)

            return total_packets, total_bytes, end_time - start_time



def coap_total_data_points(packets):
    packets = (p for p in packets if 'coap' in p)  # Get CoAP
    packets = (p for p in packets if int(p.coap.type) == 2)  # Get ACK packets

    total = 0
    for packet in packets:
        data = bytearray.fromhex(packet.coap.payload.raw_value)
        data = json.loads(data.decode())
        total += len(data)

    return total


def calc_goodput(data_points, time_taken):
    with open('../data.json') as f:
        data_point_size = len(f.read())

    size = data_points * data_point_size

    return size / time_taken  # bytes / second


def compare(mqtt_file, coap_file):
    cap = pyshark.FileCapture(coap_file)
    coap_data_points = coap_total_data_points(cap)
    cap = pyshark.FileCapture(mqtt_file)
    mqtt_data_points = mqtt_total_data_points(cap)

    total_data_points = min(coap_data_points, mqtt_data_points)
    print("Looking at {} data points.".format(total_data_points))

    print()
    print("=" * 10, "MQTT", "=" * 10)
    cap = pyshark.FileCapture(mqtt_file)
    stats = mqtt_stats(cap, total_data_points)
    print("Total packets: {}".format(stats[0]))
    print("Total bytes: {}".format(stats[1]))
    print("Time taken: {}".format(stats[2]))
    print("Total goodput: {}".format(calc_goodput(total_data_points, stats[2])))

    print()
    print("=" * 10, "CoAP", "=" * 10)
    cap = pyshark.FileCapture(coap_file)
    stats = coap_stats(cap, total_data_points)
    print("Total packets: {}".format(stats[0]))
    print("Total bytes: {}".format(stats[1]))
    print("Time taken: {}".format(stats[2]))
    print("Total goodput: {}".format(calc_goodput(total_data_points, stats[2])))


print("\n")
print("*" * 10, "Normal experiment -- Low Loss", "*" * 10)
compare('../results/emulation/normal_low_loss/mqtt.pcap',
        '../results/emulation/normal_low_loss/coap.pcap')

print("\n")
print("*" * 10, "Normal experiment -- High Loss", "*" * 10)

print("\n")
print("*" * 10, "Backlog experiment -- Low Loss", "*" * 10)
compare('../results/emulation/backlog_low_loss/mqtt.pcap',
        '../results/emulation/backlog_low_loss/coap.pcap')

print("\n")
print("*" * 10, "Backlog experiment -- High Loss", "*" * 10)
compare('../results/emulation/backlog_high_loss/mqtt.pcap',
        '../results/emulation/backlog_high_loss/coap.pcap')
