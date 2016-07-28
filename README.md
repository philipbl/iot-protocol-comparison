# Setup

## Experiments to Run
- One message sent
- 10 minutes of messages being sent every minute with no loss
- 10 minutes of messages being sent every minute with 30% loss

## Protocols
- MQTT (QoS 0)
- MQTT (QoS 2)
- CoAP
- HTTP

## Configuration
One message is sent every 60 seconds. The message contains a payload of 121 bytes (`data.json` without newlines). For MQTT, the keep alive time is 60 seconds.

## Metrics to measure
- Success rate (number of packets received vs sent)
- Number of packets sent
- Cumulative bytes

## Topology

![](https://docs.google.com/drawings/d/1xVOIl3BIuMeQ5QgydhWK08T0ZDoUSoQXhWUuikdbUfE/pub?w=409&amp;h=193)

# Results

## One message sent

| Protocol            | Total Packets | Cumulative Bytes |
|---------------------|---------------|------------------|
| CoAP                |             2 |              233 |
| MQTT (QoS 0)        |             9 |              873 |
| MQTT (QoS 2)        |               |                  |
| HTTP                |            14 |             1414 |


## 10 Minutes, No Loss

| Protocol              | Total Messages | Total Packets | Cumulative Bytes |
|-----------------------|----------------|---------------|------------------|
| CoAP                  |             11 |            22 |             2585 |
| MQTT (QoS 0)          |             11 |            65 |             5793 |
| MQTT (QoS 2)          |             11 |        77[^1] |             6730 |
| HTTP                  |             11 |           132 |            14124 |

[^1]: MQTT QoS 2 uses the PING messages to piggyback TCP ACKS.


## 10 Minutes, 30% Loss

| Protocol              | Total Messages | Total Packets | Cumulative Bytes |
|-----------------------|----------------|---------------|------------------|
| CoAP                  |             10 |            24 |             2820 |
| MQTT (QoS 0)          |             11 |            90 |             8480 |
| MQTT (QoS 2)          |             11 |           113 |             9756 |
| HTTP                  |             10 |           144 |            16770 |
