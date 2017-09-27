# Setup

For these set of experiments we are comparing the reliable data transfer protocol I developed over CoAP and MQTT, publishing data after each sample is recorded from a sensor.

## Configuration
To speed of the emulation, data points will be generated every 10 seconds. This means that MQTT messages will be published every 10 seconds and the CoAP client will request data every 10 seconds. Messages contain a payload of 121 bytes (`data.json` file without newlines).

To make MQTT reliable, QoS 1 is used.

The amount of latency added to the network will be 14 ms.

```
SELECT MEAN(value) FROM ms WHERE home_id = 'deployment_011' AND entity_id =~ /local_ping_latency/ AND time < now() AND time > now() - 30d GROUP BY entity_id
```

## Topology
![](https://docs.google.com/drawings/d/1xVOIl3BIuMeQ5QgydhWK08T0ZDoUSoQXhWUuikdbUfE/pub?w=409&amp;h=193)


## Experiments
1. Run protocols under normal operation
2. Add some loss to link (~10%)
3. Add lots of loss to link (~50%)
4. Disconnected (queue has things in it) and then reconnected


## Metrics to measure
???


# Results

## Configuration
CoAP puts configuration in the gateway
MQTT puts configuration in the sensor
MQTT requires a third entity (a broker) to be running
To ensure no data loss, MQTT requires careful configuration. For example, you must set QoS to 1, but also set the clean_session flag to false. You must also configure the broker to save messages persistently on disk.
