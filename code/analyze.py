import json

import pyshark


def mqtt_total_packets(packets):
    return len([p for p in packets if 'tcp' in p])


def mqtt_total_bytes(packets):
    return sum(int(packet.length) for packet in packets)


def mqtt_time_taken(packets, num_packets=100):
    packets = (p for p in packets if 'mqtt' in p)
    start_packet = None
    last_packet = None
    sent_packets = 0

    for packet in packets:
        message_type = int(packet.mqtt.msgtype)

        # Look for connect packets
        if message_type == 1 and start_packet is None:
            start_packet = packet

        if message_type == 3:
            sent_packets += 1
            last_packet = packet

        if sent_packets >= num_packets:
            start_time = float(start_packet.frame_info.time_epoch)
            end_time = float(last_packet.frame_info.time_epoch)

            return end_time - start_time


def coap_total_packets(packets):
    return len([p for p in packets if 'coap' in p])


def coap_total_bytes(packets):
    return sum(int(packet.length) for packet in packets)


def coap_time_taken(packets, num_packets=100):
    packets = (p for p in packets if 'coap' in p)
    start_packet = None
    last_packet = None
    sent_packets = 0

    for packet in packets:
        message_type = int(packet.coap.type)

        # Look for connect packets
        if message_type == 0 and start_packet is None:
            start_packet = packet

        if message_type == 2:
            data = bytearray.fromhex(packet.coap.payload.raw_value)
            data = json.loads(data.decode())

            sent_packets += len(data)
            last_packet = packet

        if sent_packets >= num_packets:
            start_time = float(start_packet.frame_info.time_epoch)
            end_time = float(last_packet.frame_info.time_epoch)

            return end_time - start_time

mqtt_files = ['../results/30_loss/mqtt_1/mqtt_30_loss.pcap',
              '../results/30_loss/mqtt_2/mqtt_30_loss.pcap',
              '../results/30_loss/mqtt_3/mqtt_30_loss.pcap']

coap_files = ['../results/30_loss/coap_1/coap_30_loss.pcap',
              '../results/30_loss/coap_2/coap_30_loss.pcap']

print("MQTT")
for file in mqtt_files:
    cap = pyshark.FileCapture(file)
    print(file)
    print("Total bytes: {}".format(mqtt_total_bytes(cap)))
    print("Total packets: {}".format(mqtt_total_packets(cap)))
    print("Time to send 100 packets: {}".format(mqtt_time_taken(cap, 100)))
    print()


print("\n")
print("CoAP")
for file in coap_files:
    cap = pyshark.FileCapture('../results/30_loss/coap_1/coap_30_loss.pcap')
    print(file)
    print("Total bytes: {}".format(coap_total_bytes(cap)))
    print("Total packets: {}".format(coap_total_packets(cap)))
    print("Time to send 100 packets: {}".format(coap_time_taken(cap, 100)))
    print()
