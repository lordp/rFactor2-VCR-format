[Back to index](index.md)

### Pit lane events (Class 5, Type 2)

Most often a single byte, which maps to the following table.

Value|Meaning
-|-
0|Unknown, possibly related to the garage (exiting?)
1|Unknown, possibly related to the garage (entering?)
32|Exited pit lane or pit limiter disengaged
33|Requested pit
34|Entered pit lane or pit limiter engaged
35|Entered pit box or car on jacks
36|Exited pit box or car off jacks

If the value is 36, there is an extra 5 bytes of unknown data included. These may refer to fuel taken on, damage fixed, tyres changed.
