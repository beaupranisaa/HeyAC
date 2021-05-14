# Hey AC, it's hot in here!

Classifying AC commands with syntactic parsing on a custom grammar.

## Getting Started:

1. Install the prerequisites
```console
pip install -r requirements.txt
```
2. Try it out!
```python
$ python3
>>> from hey_ac import HeyAC
>>> h = HeyAC()
>>> h.classify('it is too hot in here')
[INDIRECT COMMAND]
[VALUE] HOT
[NEG] False
[OBJ] ENVIRONMENT
[KEY] TEMP_DOWN

[RESPONSE] Decreasing the temperature.
>>> parse_trees = h.parse('it is too hot in here')
>>> parse_trees[0].pretty_print()
                S
                |
            S_INDIRECT
      __________|_______
     NP                 VP
     |           _______|_____
   OBJECT       |            ADJP
     |          |        _____|________
   NN_OBJ      VBZ      |   VALUE      PP
     |          |       |     |     ___|____
ENVIRONMENT     BE     RB_P  HOT   IN     PLACE
     |          |       |     |    |        |
     it         is     too   hot   in      here
>>> h.classify('set the humidity to 50 %')
[DIRECT COMMAND]
[ACT] SET
[PROP] HUMIDITY
[VALUE] [{'CO': '50', 'UNIT': 'PERCENT', 'MODES': None}]
[KEY] SET_HUMIDITY

[RESPONSE] Set humidity to 50 PERCENT.
```

## References

- https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
- https://corenlp.run
