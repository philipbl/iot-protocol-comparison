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

| Protocol            | Total Packets | Cumulative Bytes | % Decrease |
|---------------------|---------------|------------------|------------|
| CoAP                |             2 |              233 | 83         |
| MQTT (QoS 0)        |             9 |              873 | 38         |
| MQTT (QoS 2)        |               |                  |            |
| HTTP                |            14 |             1414 | 0          |

## 10 Minutes, No Loss

| Protocol     | Messages Sent | Messages Received | Total Packets | Cumulative Bytes | % Decrease |
|--------------|---------------|-------------------|---------------|------------------|------------|
| CoAP         |            11 |                11 |            22 |             2585 | 82         |
| MQTT (QoS 0) |            11 |                11 |            65 |             5793 | 59         |
| MQTT (QoS 2) |            11 |                11 |            77 |             6730 |            |
| HTTP         |            11 |                11 |           132 |            14124 | 0          |

## 10 Minutes, 30% Loss

| Protocol     | Messages Sent | Messages Received | Total Packets | Cumulative Bytes | % Decrease |
|--------------|---------------|-------------------|---------------|------------------|------------|
| CoAP         |           10† |                10 |            24 |             2820 | 83         |
| MQTT (QoS 0) |            11 |                11 |            90 |             8480 | 49         |
| MQTT (QoS 2) |            11 |                11 |           113 |             9756 |            |
| HTTP         |           10† |                10 |           144 |            16770 | 0          |

## Loss overhead

CoAP = (2820 - 2585) / 2585 = 9.09%
HTTP = (16770 - 14124) / 14124 = 18.73%
MQTT (QoS 0) = (8480 - 5793) / 5793 = 46.38%
MQTT (QoS 2) = (9756 - 6730) / 6730 = 44.96%

# To Do

- Try with different parameters
- Try with different loss characteristics
- What metrics to collect?
    - Protocol overhead (just data compared to headers and retries)
    - Loss overhead (how does the protocol handle loss)
- Implement on a real network?
- What is the fundamental questions?
    - When do you use each of these protocols?



† This is due to how the sender was programmed. The network delays caused other packets to be delayed.
