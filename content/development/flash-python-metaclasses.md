Title: Python metaclasses for CI dashboards
Date: 2016-12-12 23:20
Tags: python, code
Authors: Jonathan Sharpe
Summary: Simplifying configuration with classes' classes.
Status: draft

This article outlines how I used Python's metaclass functionality to simplify
the creation of new services to display in a web application for showing near 
real-time project status. If you're interested in getting beneath the hood of
Python classes, this might be the one for you.

---

[Extreme Programming Explained] outlines as one of XP's primary practices the
**Informative Workspace**, noting that:

 > An interested observer should be able to walk into the team space and get a
 > general idea of how the project is going in fifteen seconds. ... Use your
 > space for important, active information.

As we are all using automated continuous integration, most workspaces in Pivotal
offices have big screens over them for build monitors, showing the progress of
our CI processes so that we can see immediately if there's an issue somewhere.

Pivotal's own CI system, [Concourse], is a popular choice. This has a great
display for complex pipelines, showing the various resources and build steps.
Quite a few projects have [Jenkins], using the [Build Monitor plugin] to give a
display across multiple jobs simultaneously. But for a project where we were
using a hosted CI service without a build monitor, I developed a new dashboard
tool named [Flash], using [Python] and [Flask] (*Flask + dash -> Flash*).

Concourse | Jenkins | Flash
--- | --- | ---
[![Concourse CI][1]][1] | [![Jenkins Build Monitor][2]][2] | [![Flash Dashboard][3]][3]

Flash allows multiple different services to be shown alongside one another; for
example, commits to [GitHub], story points in [Pivotal Tracker] and build status
from [Travis CI] can all be shown together, giving an at-a-glance summary of the
key project components.

---
 
A key part of Flash is the configuration. Services are set up using a JSON
format, provided via either a file (`config.json`) or an environment variable
(`FLASH_CONFIG`). As Flash is Python 3.x only I could use [keyword-only
arguments], keeping the error messages clear if any required configuration is
missed out:

```python
TypeError: __init__() missing 1 required keyword-only argument: 'job'
```

But this only tells you about the *first* `__init__` implementation in the
inheritance chain whose arguments you missed out. It also means that you have to
check the traceback to figure out which service failed, which can be a pain if 
you have several. Instead, by storing a set of the required configuration
parameters for each service class, I can give a more detailed response:

```python
TypeError: missing required config keys (password, job, root, username) from Jenkins
```

Flash is built in an object-oriented fashion. Each service is represented by a
class, with mix-ins for shared functionality like authentication or specifying
a custom root for a service's API. Each class has a `REQUIRED` attribute, a 
set of the required configuration keys. For each subclass, that attribute should
contain all of the required keys from the classes it inherits. This led to me 
trying a couple of different formulations, from simply writing out the
appropriate values to the various forms of set union:

```python
REQUIRED = {'api_token', 'account', 'repo'}

REQUIRED = GitHub.REQUIRED | CustomRootMixin.REQUIRED

REQUIRED = {'job'}.union(
    BasicAuthHeaderMixin.REQUIRED,
    ContinuousIntegrationService.REQUIRED,
    CustomRootMixin.REQUIRED,
)
```

This is all tested to ensure that the results cover the required keys, but it's
pretty awkward and adds an unnecessary layer of friction when creating a new
service. Instead, it would be good for this attribute to be set automatically
based on the classes the service inherits. For this, I turned to metaclasses.

---

In Python, the type of an instance is a class, for example:

```python
>>> type('foo')
<class 'str'>
```

`'foo'` is an instance of the class `str`. But what's `str` an instance of;
what's the type of the class itself?

```python
>>> type(str)
<class 'type'>
```

Classes that inherit from `type` are called *"metaclasses"*, and allow the 
[customisation of class creation]. Probably the most commonly-implemented method
on a metaclass is `__new__`, which is called when a new class is created and
takes the following arguments:

Argument | Type | Meaning
--- | --- | ---
`mcs` | `type` | The metaclass object.
`name` | `str` | The name of the new class.
`bases` | `tuple` | The base classes of the new class.
`attrs` | `dict` | The attributes of the new class.

To show what happens during class creation, here's a simple example:

```python
class VerboseMeta(type):

    def __new__(mcs, name, bases, attrs):
        print('mcs', mcs)
        print('name', name)
        print('bases', bases)
        print('attrs', attrs)
        return mcs

        
class Demo(metaclass=VerboseMeta):

    CLASS_ATTR = 'hello'

    def foo(self):
        pass
```

The output of this is as follows:

```python
mcs <class '__main__.VerboseMeta'>
name Demo
bases ()
attrs {'__qualname__': 'Demo', '__module__': '__main__', 'CLASS_ATTR': 'hello', 'foo': <function Demo.foo at 0x108673b70>}
```

---

Providing a metaclass for the service classes allows Flash to get involved with
the class creation process, updating the `REQUIRED` attribute with the values
from all of the base classes:

```python
class MetaService(ABCMeta):
    """Metaclass to simplify configuration."""

    def __new__(mcs, name, bases, attrs):
        """Update the new class with appropriate attributes. ... """
        attrs['REQUIRED'] = attrs.get('REQUIRED', set()).union(
            *(getattr(base, 'REQUIRED', set()) for base in bases)
        )
        attrs['FRIENDLY_NAME'] = attrs.get('FRIENDLY_NAME', name)
        return super().__new__(mcs, name, bases, attrs)
```

Note that:

 - Metaclasses can be inherited too; `MetaService` inherits `ABCMeta`, the
 metaclass for creating [Abstract Base Classes];
 - `__new__` provides an empty set if the class doesn't define any required
 configuration of its own; and
 - The `FRIENDLY_NAME` is also set if not provided, using the name of the class
 as a default value.
 
Now all a new service class has to do is inherit from the appropriate base and
mix-in classes, and the configuration will be set appropriately. For example:

```python
>>> from flash_services.auth import TokenAuthMixin
>>> from flash_services.core import CustomRootMixin, VersionControlService
>>> class NewService(CustomRootMixin, TokenAuthMixin, VersionControlService):
...     pass
...
>>> NewService.REQUIRED
{'api_token', 'root'}
```

No manual intervention required, and no forgetting to update if the base classes
change.

---

Hopefully that illustrates how Python's class system works in a slightly deeper
way, and demonstrates the value of understanding it. The next step is to try to
pick up the required configuration for each class automatically. This could be
determined by looking at the arguments to `__init__`; those without default
values must be required. In the meantime feel free to give Flash a try as your
project dashboard, and let me know what other services would be useful.

  [1]: {filename}/images/concourse-ci.png
  [2]: {filename}/images/jenkins-build-monitor.png
  [3]: {filename}/images/flash-dashboard.png

  [Abstract Base Classes]: https://docs.python.org/3/library/abc.html
  [Build Monitor plugin]: https://plugins.jenkins.io/build-monitor-plugin
  [Concourse]: https://concourse.ci
  [customisation of class creation]: https://docs.python.org/3/reference/datamodel.html#customizing-class-creation
  [Extreme Programming Explained]: http://www.pearsoned.co.uk/bookshop/detail.asp?item=100000000080182
  [Flash]: https://github.com/textbook/flash
  [Flask]: http://flask.pocoo.org
  [GitHub]: https://github.com
  [keyword-only arguments]: https://www.python.org/dev/peps/pep-3102/
  [Jenkins]: https://jenkins.io/
  [Pivotal Tracker]: https://www.pivotaltracker.com
  [Python]: https://www.python.org
  [Travis CI]: https://travis-ci.org
