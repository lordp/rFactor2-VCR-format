[Back to index](index.md)

### Checkpoint

Size|Type|Comment
-|-|-
4|Float|Lap time
4|Float|Timestamp
1|Integer|Lap number
1|Integer|Sector

Sector number calculated with the following code:

```python
num = (sector >> 6) & 3
```
