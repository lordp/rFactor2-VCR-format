[Back to index](index.md)

### Overtakes (Class 3, Type 48)

Size|Type|Comment
-|-|-
21|Unknown|
event_size - 21|Bytes|One byte per driver, referencing the driver number

Each time slice that contains this event contains the current positions of the drivers in order (1st to last). These
are stored as a byte array of the driver number collected near the start.

To figure out if an overtake has happened, compare this event's data with the one immeditately before. The replay file
doesn't weed out duplicates, so you'll need to do that yourself.

**Example**
```python
initial = [11, 21, 9, 7, 5, 28, 10, 13, 35, 15, 20, 22, 19, 8, 4, 2, 34, 16, 24, 12, 33, 3, 29, 27, 14, 31]
first = [21, 11, 9, 7, 5, 28, 10, 13, 35, 15, 20, 22, 19, 8, 4, 2, 34, 16, 24, 12, 33, 3, 29, 27, 14, 31]
# drivers 21 and 11 swap places, 2nd place overtakes 1st

second = [21, 11, 9, 7, 5, 28, 13, 10, 35, 15, 20, 22, 19, 8, 4, 2, 34, 16, 24, 12, 33, 3, 29, 27, 14, 31]
# drivers 13 and 10 swap places, 8th place overtakes 7th

third = [11, 21, 9, 7, 5, 28, 13, 10, 35, 15, 20, 22, 19, 8, 4, 2, 34, 16, 24, 12, 33, 3, 29, 27, 14, 31]
# drivers 11 and 21 swap places, 2nd place overtakes 1st

fourth = [11, 21, 9, 7, 5, 28, 10, 13, 35, 15, 20, 22, 19, 8, 4, 34, 2, 16, 24, 12, 33, 3, 29, 27, 14, 31]
# drivers 10 and 13 swap places, 8th place overtakes 7th
# drivers 34 and 2 swap places, 17th place overtakes 16th
```
