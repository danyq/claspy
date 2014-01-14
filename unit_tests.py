#!/usr/bin/env python
#
# Unit tests for claspy.

from claspy import *

########## BoolVars ##########

#### invert

a = BoolVar()
b = ~a
require(a)
solve()
assert a.value() == True
assert b.value() == False

reset()
a = BoolVar()
b = ~a
require(b)
solve()
assert a.value() == False
assert b.value() == True

#### equals

reset()
a = BoolVar()
b = BoolVar()
c = a == b
require(c)
require(a)
solve()
assert a.value() == True
assert b.value() == True
assert c.value() == True

reset()
a = BoolVar()
b = BoolVar()
c = a == b
require(c)
require(~a)
solve()
assert a.value() == False
assert b.value() == False
assert c.value() == True

reset()
a = BoolVar()
b = BoolVar()
c = a == b
require(a)
require(~b)
solve()
assert a.value() == True
assert b.value() == False
assert c.value() == False

#### not-equal

reset()
a = BoolVar()
b = BoolVar()
c = a != b
require(a)
require(~b)
solve()
assert a.value() == True
assert b.value() == False
assert c.value() == True

#### and

reset()
a = BoolVar()
b = BoolVar()
c = a & b
require(~a)
require(~b)
solve()
assert c.value() == False

reset()
a = BoolVar()
b = BoolVar()
c = a & b
require(a)
require(~b)
solve()
assert c.value() == False

reset()
a = BoolVar()
b = BoolVar()
c = a & b
require(a)
require(c)
solve()
assert c.value() == True

#### or

reset()
a = BoolVar()
b = BoolVar()
c = a | b
require(a)
require(~b)
solve()
assert c.value() == True

reset()
a = BoolVar()
b = BoolVar()
c = a | b
require(a)
require(b)
solve()
assert c.value() == True

reset()
a = BoolVar()
b = BoolVar()
c = a | b
require(~a)
require(~b)
solve()
assert c.value() == False

#### xor

reset()
a = BoolVar()
b = BoolVar()
c = a ^ b
require(a)
require(~b)
solve()
assert c.value() == True

reset()
a = BoolVar()
b = BoolVar()
c = a ^ b
require(a)
require(b)
solve()
assert c.value() == False

reset()
a = BoolVar()
b = BoolVar()
c = a ^ b
require(~a)
require(~b)
solve()
assert c.value() == False

#### greater-than

reset()
a = BoolVar()
b = BoolVar()
c = a > b
require(a)
require(b)
solve()
assert c.value() == False

reset()
a = BoolVar()
b = BoolVar()
c = a > b
require(a)
require(~b)
solve()
assert c.value() == True

#### less-than

reset()
a = BoolVar()
b = BoolVar()
c = a < b
require(~a)
require(b)
solve()
assert c.value() == True

#### greater or equal

reset()
a = BoolVar()
b = BoolVar()
c = a >= b
require(a)
require(b)
solve()
assert c.value() == True

#### less or equal

reset()
a = BoolVar()
b = BoolVar()
c = a <= b
require(a)
require(b)
solve()
assert c.value() == True

#### constructors

reset()
a = BoolVar(True)
solve()
assert a.value() == True

reset()
a = BoolVar(22)
solve()
assert a.value() == True

reset()
a = BoolVar(0)
solve()
assert a.value() == False


########## IntVars ##########

#### eq
reset()
a = IntVar()
b = IntVar()
c = a == b
require(a == 22)
require(c)
solve()
assert a.value() == 22
assert b.value() == 22
assert c.value() == True

#### ne
reset()
a = IntVar()
b = IntVar()
c = a != b
require(a == 22)
require(b == 23)
solve()
assert c.value() == True

#### add
reset()
a = IntVar()
b = IntVar()
c = a + b
require(a == 22)
require(b == 15)
solve()
assert c.value() == 37

#### sub
reset()
a = IntVar()
b = IntVar()
c = a - b
require(a == 22)
require(b == 15)
solve()
assert c.value() == 7

#### gt
reset()
a = IntVar()
b = IntVar()
c = a > b
require(a == 22)
require(b == 15)
solve()
assert c.value() == True

reset()
a = IntVar()
b = IntVar()
c = a > b
require(a == 4)
require(b == 5)
solve()
assert c.value() == False

#### lt
reset()
a = IntVar()
b = IntVar()
c = a < b
require(a == 22)
require(b == 15)
solve()
assert c.value() == False

reset()
a = IntVar()
b = IntVar()
c = a < b
require(b == 1)
require(c)
solve()
assert a.value() == 0

#### ge
reset()
a = IntVar()
b = IntVar()
c = a >= b
require(a == 100)
require(b == 13)
solve()
assert c.value() == True

reset()
a = IntVar()
b = IntVar()
c = a >= b
require(a == 13)
require(b == 13)
solve()
assert c.value() == True

#### le
reset()
a = IntVar()
b = IntVar()
c = a <= b
require(a == 13)
require(b == 13)
solve()
assert c.value() == True

reset()
a = IntVar()
b = IntVar()
c = a <= b
require(a == 14)
require(b == 13)
solve()
assert c.value() == False

#### initializers

reset()
a = IntVar(4)
b = a - 1
solve()
assert a.value() == 4
assert b.value() == 3

reset()
a = IntVar(3,5)
b = IntVar(1,3)
require(a == b)
solve()
assert a.value() == 3
assert b.value() == 3

reset()
a = IntVar([4,5,6])
b = IntVar([2,6,3])
require(a == b)
solve()
assert a.value() == 6
assert b.value() == 6

#### set bits
reset()
set_bits(3)
a = IntVar()
require(a > 6)
solve()
assert a.value() == 7

## shift
reset()
a = IntVar()
b = a << 2
require(a == 3)
solve()
assert b.value() == 12

reset()
a = IntVar()
b = a >> 2
require(a == 15)
solve()
assert b.value() == 3

reset()
a = IntVar()
b = IntVar()
c = a * b
require(a == 3)
require(b == 5)
solve()
assert c.value() == 15



######### cond ##########

reset()
a = IntVar(5)
b = IntVar(22)
c = BoolVar()
d = cond(c, a, b)
require(c)
solve()
assert d.value() == 5

reset()
a = IntVar(5)
b = IntVar(22)
c = BoolVar()
d = cond(c, a, b)
require(~c)
solve()
assert d.value() == 22

#### all diff

reset()
a = IntVar(0,2)
b = IntVar(0,2)
c = IntVar(0,2)
require_all_diff([a,b,c])
solve()
assert a.value() != b.value()
assert a.value() != c.value()
assert b.value() != c.value()

#### sum_vars

reset()
a = sum_vars([IntVar(x) for x in [0,3,22,17,4]])
solve()
assert a.value() == 46


######## MultiVars ########

reset()
a = MultiVar('a','b','c')
b = MultiVar('b','d','f')
require(a == b)
solve()
assert a.value() == 'b'
assert b.value() == 'b'

reset()
a = MultiVar('a','b')
b = MultiVar('a','b')
require(a != b)
require(a == 'a')
solve()
assert a.value() == 'a'
assert b.value() == 'b'

reset()
a = MultiVar('a','b')
b = MultiVar('a','b')
c = a + b
require(a == 'a')
require(b == 'b')
solve()
assert c.value() == 'ab'

reset()
a = MultiVar(4,5,6)
b = MultiVar(4,5,6)
c = a - b
require(a == 4)
require(b == 6)
solve()
assert c.value() == -2

reset()
a = MultiVar('a','b','c')
b = MultiVar('b','c','d')
require(a > b)
solve()
assert a.value() == 'c'
assert b.value() == 'b'

reset()
a = MultiVar('b','c','d')
b = MultiVar('a','b','c')
require(a < b)
solve()
assert a.value() == 'b'
assert b.value() == 'c'

reset()
a = MultiVar('a','b','c')
b = MultiVar('c','d','e')
require(a >= b)
solve()
assert a.value() == 'c'
assert b.value() == 'c'

reset()
a = MultiVar('c','d','e')
b = MultiVar('a','b','c')
require(a <= b)
solve()
assert a.value() == 'c'
assert b.value() == 'c'

reset()
a = MultiVar(1,2,3)
b = IntVar()
require(a == b)
require(b == 2)
solve()
assert a.value() == 2

reset()
a = MultiVar(1,2,3)
b = IntVar()
require(b == a)
require(b == 2)
solve()
assert a.value() == 2

reset()
a = MultiVar((1,2,3),(4,5,6),(7,8,9))
b = IntVar()
require(a[1] == b)
require(b == 5)
solve()
assert a.value() == (4,5,6)

reset()
a = MultiVar(1,2)
b = MultiVar(3,4)
c = BoolVar()
d = cond(c, a, b)
require(~c)
solve()
assert d.value() > 2

reset()
a = MultiVar(1,2)
b = MultiVar(3,4)
require(a + b == 4)
solve()
assert a.value() == 1
assert b.value() == 3

reset()
a = MultiVar(1,2)
b = MultiVar(3,4)
require(b - a == 3)
solve()
assert a.value() == 1
assert b.value() == 4

reset()
a = MultiVar(1,2)
b = MultiVar(3,4)
require(a * b == 6)
solve()
assert a.value() == 2
assert b.value() == 3

reset()
a = MultiVar(1.0,2.0)
b = MultiVar(3.0,4.0)
require(a / b == 0.5)
solve()
assert a.value() == 2
assert b.value() == 4

# catch a problem with python behavior of ~True
reset()
a = MultiVar('x')
require(a != 'x')
assert not solve()


print 'ALL TESTS PASSED'
