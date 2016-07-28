# Setup

## Experiments to Run
- One message sent
- 10 minutes with no loss
- 10 minutes with 30% loss

## Protocols
- CoAP
- HTTP
- MQTT (QoS 0)
- MQTT (QoS 2)

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
| HTTP                |            14 |             1414 |
| MQTT (QoS 0)        |             9 |              873 |
| MQTT (QoS 2)        |               |                  |


## 10 Minutes, No Loss

| Protocol              | Total Messages | Total Packets | Cumulative Bytes |
|-----------------------|----------------|---------------|------------------|
| CoAP                  |             11 |            22 |             2585 |
| HTTP                  |             11 |           132 |            14124 |
| MQTT (QoS 0)          |             11 |            65 |             5793 |
| MQTT (QoS 2)          |             11 |           77† |             6730 |

† MQTT QoS 2 uses the PING messages to piggyback TCP ACKS.


## 10 Minutes, 30% Loss

| Protocol              | Total Messages | Total Packets | Cumulative Bytes |
|-----------------------|----------------|---------------|------------------|
| CoAP                  |             10 |            24 |             2820 |
| HTTP                  |             10 |           144 |            16770 |
| MQTT (QoS 0)          |             11 |            90 |             8480 |
| MQTT (QoS 2)          |             11 |           113 |             9756 |
