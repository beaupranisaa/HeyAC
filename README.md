# Hey AC, it's hot in here!

Classifying AC commands with syntactic parsing and a custom grammar.

## Getting Started:

1. Install the prerequisites
```console
pip install -r requirements.txt
```
2. Try it out!
```python
>>> from hey_ac import HeyAC
>>> h = HeyAC()
>>> h.classify('it is too hot in here')
[INDIRECT COMMAND]
[VALUE] HOT
[NEG] False
[OBJ] USER
[RESPONSE] Decreasing the temperature.
>>> h.classify('set the humidity to 50 %')
[DIRECT COMMAND]
[PROP] HUMIDITY
[VALUE] [{'CO': '50', 'UNIT': 'PERCENT', 'MODES': None}]
[RESPONSE] Set humidity to 50 PERCENT.
```

## References

- https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
- https://corenlp.run
