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

Class|Type|Comment
-|-|-|-
0|7 - 16|Driver positions and info
1|7|Driver enters or leaves their garage
1|10|Number of lights shown
1|23|Countdown to race start
2|5|Penalty given to a driver
2|7|Driver served a penalty
2|8|Admin removed a penalty from a driver
2|19|Session type (race, qualifying, etc)
3|6|Checkpoint event - usually when a sector is completed
3|5|Rank event
3|15|Garage related event
3|16|Driver DNF
3|18|Driver DSQ
3|19|Driver Kicked
3|48|Driver Overtake
