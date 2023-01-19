# Stupid Forth

This is a dumb forth implementation I wrote in an hour without doing any research.  It has the following features

- *int1* *int2* **add** - add two numbers
- *int1* *int2* **sub** - subtract two numbers
- *int1* *int2* **mul** - multiply two numbers
- *int1* *int2* **div** - divide two numbers
- *N* **dup** - duplicate the last *N* items on the stack
- **printstack** - print the entire stack
- *N* **repeat** - repeat the last item on the stack *N* times
- **print** - print the last item on the stack

Strings must be surrounded by `"` and cannot contain spaces.  Symbol groups must be surrounded by `{}`

## Examples

Print the first 20 Fibonacci numbers

``` python
1 1
{ 2 dup add } 20 repeat
printstack
```

``` python
>>> %run sforth.py fib.sf
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711]
```
