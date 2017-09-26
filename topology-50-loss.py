set ns [new Simulator]
source tb_compat.tcl

# Nodes
set sensor [$ns node]
set gateway [$ns node]

# Lans
set lan0 [$ns make-lan "$sensor $gateway" 1Mb 10ms]

# Add loss to network
tb-set-lan-loss $lan0 0.5

$ns rtproto Static
$ns run
