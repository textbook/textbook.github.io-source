Title: A context manager-based case statement
Date: 2015-07-06 12:00
Tags: code, python
Authors: Jonathan Sharpe
Summary: Use of Python's context manager syntax to ape a switch-case statement.

I wanted to have a post with some code in, for testing purposes, so here is a little
something I put together based on [this Programmers.SE question][1]. `Switch` (ab?)uses
Python's context manager `with` statement syntax to implement a rough approximation
of the `switch` available in some other languages.

Also available [as a Gist][2].

```
:::python
class Switch(object):
	"""A class for faking switch syntax with a context manager.

	Args:
	  value (object): The stored value to compare any cases to.

	Example:

		>>> with Switch(1) as case:
		...     if case(1):
		...         print('unity')
		...
		unity
		>>> with Switch(3) as case:
		...     if case(1):
		...         print('unity')
		...     elif case(2, 3, 4):
		...         print('small')
		...
		small
		>>> with Switch(5) as case:
		...     if case(1):
		...         print('unity')
		...     elif case(2, 3, 4):
		...         print('small')
		...     else:
		...         print('more than four')
		...
		more than four

	"""

	def __init__(self, value):
		"""Create a new Switch instance."""
		self.value = value

	def __call__(self, *cases):
		"""Do any of the supplied cases match the stored value?"""
		return any(case == self.value for case in cases)

	def __enter__(self):
		"""Enter the context manager."""
		return self

	def __exit__(self, typ, value, traceback):
		"""Don't do anything when leaving the context manager."""
		pass
```

  [1]: http://programmers.stackexchange.com/questions/287218/i-wrote-a-python-switch-statement
  [2]: https://gist.github.com/textbook/5e83044f637fda1a63fe
