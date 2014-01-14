Claspy is a python constraint solver based on the answer set solver 'clasp'. It allows you to quickly solve many kinds of logic puzzles.

It requires the program 'clasp' from: http://www.cs.uni-potsdam.de/clasp/
On Debian/Ubuntu:
apt-get install clasp

After installing clasp, put claspy.py in your python path or in your working directory.

If you need to change the path to the binary or the arguments to clasp, you can modify the CLASP_COMMAND variable in claspy.py.

To verify that all is working, run unit_tests.py.


#### Introduction ####

In a claspy program, you construct a problem in python, call solve(), then print the results.

In the construction phase, you declare special variables that can take on many possible values, and you place constraints on them. These variables have no actual value until solve() is called. Once a solution is found, the variables take on concrete values and you can print them out.

For example:

>>> from claspy import *
>>> a = IntVar()

Here we have created a variable 'a' representing a number. It has no value right now, and if we print it out it will just show '0'.

>>> b = IntVar()
>>> c = a + b

Here's another number, and 'c' is the sum of the two. But there's no addition happening. The addition operator simply creates a new variable with the constraint that it must equal the sum of 'a' and 'b'. Here's an explicit constraint:

>>> require(c == 22)

require() is the most basic way to express a constraint. It asserts that a variable or expression must be true. Now try solving:

>>> solve()
SATISFIABLE
>>> print a, b
10 12

After solving, 'a' and 'b' take on values satisfying the constraints. There are multiple answers, so your values may differ. We can continue adding constriants and solve again:

>>> require(a * b == 85)
>>> require(a < b)
>>> solve()
SATISFIABLE
>>> print a, b
5 17

Now we have a unique solution. We can verify its uniqueness like this:

>>> require((a != 5) | (b != 17))
>>> solve()
UNSATISFIABLE


#### Concepts ####

When writing code, it's important to distinguish between claspy variables and regular python variables. These must be treated differently because claspy variables do not take on a value until solve() is called, so only certain operations can be performed with them. For example, the following would not make sense:

x = BoolVar()
if x:
  y = 22
else:
  y = 17

'x' can't be used like a regular boolean because it has no concrete value yet, so this code will produce unexpected results. To create an 'if' statement like that, use the following function:

y = cond(x, 22, 17)

Now 'y' is an IntVar, and there is a constraint between 'x' and 'y'.

With these statements we are forming a network of constraints, and the program that constructs the network can't use any values within the network until the whole thing is finished and a solution is found.


#### Main interface ####

BoolVar() -- creates a boolean variable
IntVar() -- creates an integer variable (>= 0)
MultiVar(a,b,..) -- creates a variable with one of the given values
Atom() -- creates an atom, useful for connectivity problems
cond(pred, cons, alt) -- creates an "if" statement
require(x) -- constrains a variable to be true
solve() -- runs clasp and returns True if satisfiable

To get the value of a variable x after solving, use:
x.value()
or just 'print x'


#### BoolVar ####

BoolVar() creates a boolean variable.
BoolVar(b) converts a regular boolean to a BoolVar.

Supported operations:
==, !=, <, >, <=, >=, ^, &, |, ~, +

You must use &, |, ~ for AND, OR, and NOT instead of the python operations 'and' 'or' and 'not'.

The + operator returns an IntVar.


#### IntVar ####

IntVar() creates an integer variable.
IntVar(4) converts a regular integer to an IntVar.
IntVar(1,9) creates a variable in the range 1 to 9, inclusive.
IntVar([1,3,5]) creates a variable with one of the given values.

Supported operations:
==, !=, +, -, *, >, <, >=, <=, <<, >>


The values of an IntVar are non-negative and bounded by the number of bits used in the internal representation, 16 by default. To change the number of bits, use:
set_bits(8)

You can alternatively use set_max_val to set a sufficient number of bits to represent a specific value:
set_max_val(100)

set_bits and set_max_val must be called before any variables are created.


Be careful of the non-negative constraint when using subtraction. For example, if you have an IntVar x and write:
cond(y == x - 1, ...)
Then x becomes constrained to be >= 1, because the result of 'x - 1' must be a non-negative IntVar. In many cases, you can rearrange an expression to avoid this issue:
cond(y + 1 == x, ...)
Now x can still be zero.

Also be careful of the maximum value limits when adding numbers. For example, if you have:
cond(y == x + 1, ...)
Then x is no longer allowed to take on the maximum possible value.


For << and >>, an IntVar can only be shifted left or shifted right by a normal integer value, not another IntVar.


Efficiency note: IntVar is implement as a series of BoolVars representing the bits of the number. Addition and especially multiplication with a large number of bits can generate a large number of rules, so it's best to restrict the number of bits to the minimum necessary for your problem.


#### MultiVar ####

MultiVar(...) creates a variable of a generic type which can take on the value of one of its arguments.

Supported operations:
==, !=, +, -, *, /, >, <, >=, <=, []

For example, you can create a MultiVar of strings:
x = MultiVar('cat', 'dog', 'rabbit')
Then perform operations such as:
require(x[1] == 'a')

When performing operations on MultiVars, the operation must be valid for all possible values of the variable. For example, attempting to test x[3] would return an error. The same applies for x[y] where y is a MultiVar; y must not have numbers greater than 2 as possible values.

Operations can involve two MultiVars, or regular python variables, but not a MultiVar and a BoolVar or IntVar. For example, you cannot add a MultiVar and an IntVar.

Efficiency note: MultiVar is implemented as a series of BoolVars, one for each possible value of the variable. Although MultiVars are very flexible, binary operations between two MultiVars can create an exponential number of rules, so use them carefully.


#### Atom ####

Atom() creates a kind of boolean variable useful for testing connectivity in a graph.

It supports all the operations of a BoolVar, plus:
x.prove_if(y)
where x is an Atom and y is a BoolVar, Atom, or expression.

*** An Atom is only true if proven. ***

For example, if you have a directed graph:
a -> b -> c
And you would like to know if there is a path from a to c:
a, b, c = Atom(), Atom(), Atom()
a.prove_if(True)
b.prove_if(a)
c.prove_if(b)
require(c)

Atoms are very efficient and work for large graphs and complex conditions. See examples/hitori.py for an example of their use.


#### Convenience functions ####

These convenience functions are generally more efficient than the equivalent using regular operations, so they should be used if possible:

require_all_diff(lst) constrain all vars in a list to be different
sum_vars(lst)        sum a list of variables
at_least(n, bools)   whether at least n of the booleans are true
at_most(n, bools)    whether at most n of the booleans are true
sum_bools(n, bools)  whether exactly n of the booleans are true
var_in(v, lst)       whether var v is equal to some element in lst


#### Debugging your program ####

If your program produces multiple solutions where you expect only one, it's usually clear from the solutions which constraints are not being applied correctly. But if it produces no solutions, it can be pretty hard to debug.

A convenience function, required(), is provided to help with this case:
required(expr, name)
expr is a BoolVar or expression, and name is a string.

required() does not create any constraints. It stores the expression under the given name, and after solve() finishes, the names of any 'required' expressions that are false are printed out.

Here's one way to use it. Say you have an example problem for which you know the answer, but your program isn't finding it:
...
require(a)  # first constraint
require(b)  # second constraint
require(c)  # third constraint
solve()  # unsatisfiable! why?

You can change all 'require' statements to 'required' and constrain the answer to a known solution:
...
required(a, 'first constraint')
required(b, 'second constraint')
required(c, 'third constraint')
require(solution)  # just for debugging
solve()

Then the solver will print something like "Failed constraint: second constraint" showing you where the bug is.

For additonal convenience 'require' will accept a second argument as well, which is ignored. So you can reactivate a constraint by changing 'required' back to 'require' without deleting the name.


#### Reminders ####

* Do not use 'and', 'or', 'not', or 'if' with BoolVars.
* Subtraction constrains the minimum value of the input.
* Addition constraints the maximum value of the input.
