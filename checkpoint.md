[Back to index](index.md)

### Checkpoint (Class 3, Type 6)

Size|Type|Comment
-|-|-
4|Float|Lap or sector time
4|Float|Timestamp
1|Integer|Lap number
1|Integer|Sector
variable|Unknown|

Sector number calculated with the following code:

```python
num = (sector >> 6) & 3
```
