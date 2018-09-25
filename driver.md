[Back to index](index.md)

### Driver details (Class 0, Types 7-16)

The current gear is calculated by subtracting 8 from event type. -1 is Reverse, 0 is Neutral, etc.

Size|Type|Comment
-|-|-
4|Unsigned Integer|Steer Yaw, Throttle, Engine RPM and Pit Status (see below for details)
4|Unsigned Integer|Detachable Part State (wings, wheels)
5|Bytes|Speed info
25|Unknown|
1|Integer|Traction control and brakes
4|Float|X position
4|Float|Y position
4|Float|Z position
4|Float|X rotation
4|Float|Y rotation
4|Float|Z rotation

### Info 1 details (first unsigned int)
Bytes|Info
-|-
`XXXXXXXX XXXXXX00 00000000 00000000`|Current RPS (14 bits)
`00000000 000000X0 00000000 00000000`|In pit lane flag (1 bit)
`00000000 0000000X XXXXX000 00000000`|Throttle (6 bits)
`00000000 00000000 00000X00 00000000`|Horn (1 bit)
`00000000 00000000 000000XX XXXXXXXX`|Steer yaw (10 bits)

```python
steer_yaw = info1 & 127
throttle = info1 >> 11 & 63
engine_rpm = info1 >> 18
in_pit = (info1 >> 17 & 0x1) != 0
horn = (info1 >> 10 & 0x1) != 0
```

### Info 2 details (second unsigned int)
Bytes|Info
-|-
`XXXXXXXX 00000000 00000000 00000000`|Acceleration
`00000000 X0000000 00000000 00000000`|Properly following
`00000000 0X000000 00000000 00000000`|Warning light flag
`00000000 00X00000 00000000 00000000`|Driver visible flag
`00000000 000X0000 00000000 00000000`|Head light flag
`00000000 0000XX00 00000000 00000000`|Current driver (2 bits)
`00000000 000000X0 00000000 00000000`|Detachable Part Damage State (DPART_DEBRIS11)
`00000000 0000000X 00000000 00000000`|Detachable Part Damage State (DPART_DEBRIS10)
`00000000 00000000 X0000000 00000000`|Detachable Part Damage State (DPART_DEBRIS9)
`00000000 00000000 0X000000 00000000`|Detachable Part Damage State (DPART_DEBRIS8)
`00000000 00000000 00X00000 00000000`|Detachable Part Damage State (DPART_DEBRIS7)
`00000000 00000000 000X0000 00000000`|Detachable Part Damage State (DPART_DEBRIS6)
`00000000 00000000 0000X000 00000000`|Detachable Part Damage State (DPART_DEBRIS5)
`00000000 00000000 00000X00 00000000`|Detachable Part Damage State (DPART_DEBRIS4)
`00000000 00000000 000000X0 00000000`|Detachable Part Damage State (DPART_DEBRIS3)
`00000000 00000000 0000000X 00000000`|Detachable Part Damage State (DPART_DEBRIS2)
`00000000 00000000 00000000 X0000000`|Detachable Part Damage State (DPART_DEBRIS1)
`00000000 00000000 00000000 0X000000`|Detachable Part Damage State (DPART_DEBRIS0)
`00000000 00000000 00000000 00X00000`|Detachable Part Damage State (DPART_RWING)
`00000000 00000000 00000000 000X0000`|Detachable Part Damage State (DPART_FWING)
`00000000 00000000 00000000 0000X000`|Detachable Part Damage State (DPART_RR)
`00000000 00000000 00000000 00000X00`|Detachable Part Damage State (DPART_RL)
`00000000 00000000 00000000 000000X0`|Detachable Part Damage State (DPART_FR)
`00000000 00000000 00000000 0000000X`|Detachable Part Damage State (DPART_FL)

### Speed Info
```python
'xxxxxxxx yyXxxxxx yyyyyyyy zzzzzzYy Zzzzzzzz'

# x is a bit of Vx, X is the Sign bit of Vx
# y is a bit of Vy, Y is the Sign bit of Vy
# z is a bit of Vz, Z is the Sign bit of Vz
``` 

### Info 3 details (single int after speed info)
Bytes|Info
-|-
`XX000000`|Traction control level (2 bits)
`00XXXXXX`|Brakes (6 bits)
