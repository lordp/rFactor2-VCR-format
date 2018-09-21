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
Session Info|1|Integer
Unknwon|67|Bytes|Unknown chunk of data

**Session Info**
* Session Type = session_info & 0xF
* Private Session = session_info >> 7 & 1
