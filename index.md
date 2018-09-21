## rFactor 2 VCR (replay) file format

This is an attempt to document the file format of the rFactor 2 replay files (.vcr). The basis for this is Gerald Jacobson's [wiki](http://rf2-vcr-replay-format.wikia.com/wiki/RF2_VCR_Replay_Format_Wiki) and rf2ReplayOffice application source code.

All of the information is based on version 1.08 of the replay file.

### Header

Description|Length|Type|Comment
-|-|-|-
Header text|variable|String|Read bytes until 0x0A is encountered
Separator|1|Byte|0x0A
IRSR tag|4|String|"IRSR"
Version|4|Float|1.08

### Replay Information

Description|Length|Type|Comment
-|-|-|-
RFM string length|4|Integer|
RFM string|variable|String|
Unknown|4|Integer|
Mod Info length|4|Integer|
Mod Info|variable|String|Info about the mod - name, version, track info, drivers, points, etc
SCN Filename length|4|Integer|
SCN Filename|variable|String|File name for the track used
AIW Filename length|4|Integer|
AIW Filename|variable|String|Filename for the AIW file (info for AI drivers)
Mod name length|2|Integer|
Mod name|variable|String|Name of the mod
Mod version length|2|Integer|
Mod version|variable|String|Version of the mod
Mod UID length|2|Integer|
Mod UID|variable|String|UID of the mod (MD5 or similar hash)
Track path length|2|Integer|
Track path|variable|String|Full path to the track file
Unknown|1|Integer|
Session Info|1|Integer|
Unknwon|67|Bytes|Unknown chunk of data

**Session Info**
* Session Type = session_info & 0xF
* Private Session = session_info >> 7 & 1

### Driver list

Description|Length|Type|Comment
-|-|-|-
Driver count|1|Integer|

For each driver, the following structure applies

Description|Length|Type|Comment
-|-|-|-
Number|1|Integer|Driver number, used later in the file
Name length|1|Integer|
Name|variable|String|
Co-driver name length|1|Integer|
Co-driver name|variable|String|
Vehicle name length|2|Integer|
Vehicle name|variable|String|eg FSR2018
Vehicle version length|2|Integer|
Vehicle version|variable|String|eg 1.07
Vehicle ID length|1|Integer|
Vehicle ID|variable|String|64 character string
Vehicle filename|32|String|Read up to the first \x00 character, discard the rest
Unknown|48|Unknown|Unknown chunk of data
Entry time|4|Float|
Exit time|4|Float|

### Events and Time Slices

The rest of the file describes the replay in 'slices' of time. These are variable length blocks of data, each one with a header that, when decoded, describes the content and size of the slice/block.

Description|Length|Type|Comment
-|-|-|-
Slice count|4|Integer|
Total event count|4|Integer|The total number of events in the replay
Start time|4|Float|
End time|4|Float|

Each time slice uses the following structure.

Description|Length|Type|Comment
-|-|-|-
Slice time|4|Float|
Event count|4|Unsigned Integer|Number of events in this slice

Each slice then has a number of events of variable size, with an unsigned integer header at the start that describes the content and size. This header is decoded as follows:

```python
event_size = (header >> 8) & 0x1ff
event_class = (header >> 29)
event_type = (header >> 17) & 0x3f
event_driver = header & 0xff
```

What follows is what Gerald and I have figured out of the format, organised into class and type.

Class|Type|Link|Comment
-|-|-|-
0|7 - 16|[Link](driver.md)|Driver positions and info
1|7|[Link](garage.md)|Driver enters or leaves their garage
1|10|[Link](lights.md)|Number of lights shown
1|23|[Link](countdown.md)|Countdown to race start
2|5|[Link](penalty_given.md)|Penalty given to a driver
2|7|[Link](penalty_served.md)|Driver served a penalty
2|8|[Link](penalty_removed.md)|Admin removed a penalty from a driver
2|19|[Link](session_type.md)|Session type (race, qualifying, etc)
3|6|[Link](checkpoint.md)|Checkpoint event - usually when a sector is completed
3|5|[Link](rank_event.md)|Rank event
3|9|[Link](countdown_period.md)|When the countdown begins and ends
3|15|[Link](garage_event.md)|Garage related event
3|16|[Link](dnf.md)|Driver DNF
3|18|[Link](dsq.md)|Driver DSQ
3|19|[Link](kicked.md)|Driver Kicked
3|48|[Link](overtake.md)|Driver Overtake

The next set of classes/types is what I've observed, but haven't figured out their meanings (partially or completely).

Class|Type|Link|Comment
-|-|-|-
0|1|[Link](0_1.md)|
0|3|[Link](0_3.md)|
0|4|[Link](0_4.md)|
0|5|[Link](0_5.md)|Related to engine damage events
1|4|[Link](1_4.md)|
1|6|[Link](1_6.md)|
1|11|[Link](1_11.md)|Same as 2-17 I think
1|26|[Link](1_26.md)|
2|9|[Link](2_9.md)|
2|15|[Link](2_15.md)|
2|17|[Link](incidents.md)|Incidents - collisions with cars, signs, posts, wheels, etc
2|23|[Link](engine_damage.md)|Engine damage events
2|26|[Link](suspension_damage.md)|Suspension damage events
2|28|[Link](2_28.md)|
2|29|[Link](sector_1.md)|Sector 1 events
2|30|[Link](sector_2.md)|Sector 2 events
2|31|[Link](sector_3.md)|Sector 3 events
3|8|[Link](3_8.md)|
3|22|[Link](formation.md)|Formation lap
3|38|[Link](3_38.md)|
3|49|[Link](pitlane.md)|Pit events
5|2|[Link](5_2.md)|
5|3|[Link](5_3.md)|
