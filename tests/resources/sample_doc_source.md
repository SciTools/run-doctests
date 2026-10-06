# run-doctests
Self-contained doctest checker using standard-library 'doctests' package.

Sample doctest, OK :

```python
>>> import sys
>>> sys.exit
<built-in function exit>
>>> 
```

Sample doctest, FAIL:

```python
>>> print(None)
none found
>>> 1
2
```