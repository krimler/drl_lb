# drl_lb: The experimental setup for measuring performance of automatic load balancer for data center environment.

## Traffic Generation:
The repository contains code for following:
1. Generating huge data center web bound traffic(IP and URL). Please see config.ini section.
2. Number of unique IP's in a subnet.
3. probability distribution classes of Alexa's 1 million URL. But can use Cisco's OpenDNS URL's too.
4. how many instances of traffic (combination of IP and URL).

## Traffic execution
The Redis data-store is been used as load balancing server. 
The time-out feature of Redis is used to simulate HTTP persistent sessions and to simulate HTTP sessionprocessing time.
Seperate redis servers are used to measure above timing charactristics.
The redis entries will get removed after timeout.
The timeout values are configurable.

Simple query to Redis for number of live session is useful as measure of load balancer state.

## Trafic Measurement:
1. Can configure different load balancing policies: 
       round_robin, 
       least_connection, 
       source_hash, 
       destination_hash, 
       source_and_destination_hash, 
       deep_reinforcement
2. Reward function parameters for DRL based load balaning policy.
3. HTTP request download time probability distribution can be defined.

All the references used for code development are embedded in the code itself as code comment.
start exploring from driver.py.
