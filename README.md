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
One message is sent every 60 seconds. Messages contain a payload of 121 bytes (`data.json` file without newlines). For MQTT, the keep alive time is 60 seconds.

## Metrics to measure
- Success rate (number of messages received vs sent)
- Number of packets transmitted
- Cumulative bytes transmitted

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

| Protocol     | Messages Sent | Messages Received | Total Packets | Cumulative Bytes |
|--------------|---------------|-------------------|---------------|------------------|
| CoAP         |            11 |                11 |            22 |             2585 |
| HTTP         |            11 |                11 |           132 |            14124 |
| MQTT (QoS 0) |            11 |                11 |            65 |             5793 |
| MQTT (QoS 2) |            11 |                11 |            77 |             6730 |


## 10 Minutes, 30% Loss

| Protocol     | Messages Sent | Messages Received | Total Packets | Cumulative Bytes |
|--------------|---------------|-------------------|---------------|------------------|
| CoAP         |           10† |                10 |            24 |             2820 |
| HTTP         |           10† |                10 |           144 |            16770 |
| MQTT (QoS 0) |            11 |                11 |            90 |             8480 |
| MQTT (QoS 2) |            11 |                11 |           113 |             9756 |


† This is due to how the sender was programmed. The network delays caused other packets to be delayed.
