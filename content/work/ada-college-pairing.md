Title: Introduction to Pair Programming
Date: 2017-10-13 10:20
Modified: 2017-10-16 10:20
Tags: pivotal, pairing, xp
Authors: Jonathan Sharpe
Summary: Why do we pair program at Pivotal, and could you be doing it too?

As part of Pivotal London's grassroots diversity and inclusion efforts, a
colleague and I have recently been talking to the team at [Ada College][1],
the UK's National College for Digital Skills, about their apprenticeship
program.

They invited us to lead an introductory session on pair programming to around
40 of their higher level digital apprentices. This is the material from that
session, rewritten as a blog post.

 ![Pairing Table in San Francisco]({static}/images/Process-Pairing-01.jpg)

<small>*"Pairing Table in San Francisco"*, &copy; Pivotal</small>

## Why do you pair?

Pair programming is one of the core practices of Extreme Programming (XP), a
software development methodology based on the principles laid out in [the
agile manifesto][3]. A major part of XP, and any agile methodology, is feedback:

 > XP teams strive to generate as much feedback as they can handle as quickly
 > as possible.
 >
 > <small>from *Extreme Programming Explained: Embrace Change* by Kent Beck
 > with Cynthia Andres</small>

With pair programming, you're getting immediate feedback on your code, as
you're writing it. This also aligns with the idea of Extreme Programming being
good practices taken to extremes - it's code review, turned all the way up.
The specific practice is described as follows:

 > Write all production programs with two people sitting at one machine...
 > Pair programmers:
 >
 > - Keep each other on task.
 > - Brainstorm refinements to the system.
 > - Clarify ideas.
 > - Take initiative when their partner is stuck, thus lowering frustration.
 > - Hold each other accountable to the team's practices.
 >
 > <small>from *Extreme Programming Explained: Embrace Change* by Kent Beck
 > with Cynthia Andres</small>

In a similar vein the Pivotal Labs [website][2] lists four benefits of
pairing, for all of the roles in a balanced product team, which I'll address in
turn in the following sections:

 - Boost efficiency through collaboration
 - Knowledge share and skill transfer
 - Prevent knowledge silo
 - 100% transparency

However, perhaps the most succinct response to the question is the following
quote from Rob Mee, Pivotal Labs founder and current Pivotal CEO:

 > It's more efficient, and it produces better code.
 >
 > <small>from [This Company Believes You Should Never Hack Alone][4]</small>

Specifically for new developers, pairing can be an effective way to ramp up
quickly, avoiding impostor syndrome and the stress of feeling abandoned to fend
for yourself in an unfamiliar codebase. [Amy Simmons][8] recently gave at
talk at Pivotal's public lunch and learn series on [the care and feeding of
new devs][9], discussing the results of a survey that found that 81% of
respondents thought that junior devs could be better supported; one of her
recommendations was to adopt code reviews and pair programming with senior
devs, at least on a weekly basis.

**Boost efficiency through collaboration**

The immediate benefit to pairing is how infrequently you find yourself stuck.
If there's something you don't know how to do, or you aren't sure where to go
next, nine times out of ten your pair will be able to get you moving again.
It's like rubber duck debugging, except that now the rubber duck can provide
additional ideas!

In addition pairing is great for maintaining focus; whereas it's easy to get
sidetracked when you're working alone (especially with a high-speed
connection to social networks, news websites and TV Tropes...), having a second
person looking at your screen keeps you honest about what you're supposed to
be working on. In my experience the "flow state" of pairing is different to
the one you get into when working alone; it's easier to get into and more
resilient to interruptions.

**Knowledge share and skill transfer**

As an engineer in Pivotal Labs, the majority of my job consists of pair
programming with our client's engineers, with the aim being to help them
develop the software they're working on and build an effective team that can
continue collaborate effectively once the engagement ends and they return to
their usual offices. I have found pair programming to be a very effective way
to teach the other practices we follow, like test-driven development (TDD)
and continuous integration and deployment (CI/CD).

It's also a productive way to introduce someone to a new technology or
codebase. Pairing with someone with less experience helps to identify where
the code could be clearer or easier to follow, which is easy to overlook when
you're more comfortable with the language or domain.

**Prevent knowledge silo**

Have you ever started trying to work on something only to be told *"Oh,
that's so-and-so's part, you should leave it to them"*? Or, even worse, *"the
person who did that left, so we try not to touch it"*? Pairing helps to avoid
this by ensuring that no single person is the only one with knowledge of any
specific part of the product.

This is especially powerful when you're regularly rotating pairs. Generally
we rotate on a daily basis, using tools like [Parrit][5] to make sure that
every possible combination is occurring. If a story is still in flight from
the previous day we *"stick and twist"*, with one person staying with the
story to pass along the context and the other moving on to something else.
This has the natural side effect that the more complex stories, the ones that
take multiple days, get more people's input.

**100% transparency**

On your own you might be tempted to rush, to cut corners; *"I'll just skip
writing this test"*, or *"this isn't great but we can refactor it later"*.
All-too-frequently, later never comes! Your pair can be your conscience,
keeping the code quality high and suggesting tweaks or possible edge cases as
you go along. They can also point out when you're overthinking something [you
aren't gonna need][15].

## Anatomy of a pairing station

There are a few crucial things you need to pair effectively:

 1. **Shared desk**: sit close enough that you can easily talk about what
    you're working on. If you have access to them, sit-stand desks allow more
    flexibility to change your position throughout the day. If the two people
    are different heights, monitor risers can be useful to keep them both
    comfortable.

 2. **Separate peripherals**: while it's possible to pair by passing a single
    keyboard and mouse back and forth, it isn't ideal. It's much easier to
    work with a set each, although you have to be careful not to jump in and
    use them at the same time! Each developer should also have their own
    mirrored monitor.

    This is particularly important when the pairing station is a laptop -
    having two people trying to look at the same relatively small screen, in
    close proximity to where one of them is trying to type, is very awkward.
    At the very least have an external monitor, mouse and keyboard, either so
    one can use those while the other uses the laptop, or so you can swap
    back and forth more easily.

 3. **Pen and paper**: whether you're discussing potential architectures,
    explaining a workflow, or just want to take a quick TODO note, nothing is
    as low friction as simply writing it down. A Post-It note on the bottom
    edge of a monitor can help record valuable information without
    interrupting the flow of pairing, and a quick sketch in a notebook is
    often the easiest way to share a complex idea.

 4. **Standard config**: to keep both partners efficient, you need to agree
    on consistent tooling and settings up-front. The pair should adopt a
    specific IDE or editor, key bindings, shortcuts, etc. This will likely mean
    compromise on some preferred tools, but is all part of taking collective
    ownership of everyone's productivity, as well as of the code. Similarly,
    agree on styling conventions, and strongly consider making linting part of
    your continuous integration process to keep everyone honest.

    If you're working in a team across multiple machines, it can be useful to
    create scripts to set up each machine identically without manual work.
    For example, the standard configuration for a Pivotal workstation is
    provided by a set of Bash scripts, available [on GitHub][6]. Another
    useful tool some of my colleagues have been working with recently is
    [Ansible][7], which can be used to automate a wide range of tasks
    including workstation setup.

## Pairing roles

Each person in the pair has a specific role. Note that this isn't a permanent
role; you can (and should!) switch frequently between the two.

  - **Driver**: the driver is responsible for actually implementing the ideas
    being discussed as code. They write out all production and test code,
    refactor existing code as required and regularly run the tests to get the
    automated feedback on how it is going.

  - **Navigator**: the navigator is responsible for aligning the driver's
    progress towards the overall goal. They provide suggestions on possible
    directions or course corrections. They can also point out any minor typo,
    but note that they should give the driver a few seconds to spot it
    themselves first!

Both people should be continually vocalising their thought processes; how do
you think the task is going? What should you be trying to do next. It's also
important to remain patient and kind when working so closely with someone for
long periods of time.

## Different methods of pairing

Within the basic principles outlined above, there are many specific variations.
Here are a couple you can try out:

  - **Switch on red**: named for the Red step of test-driven development's
    Red-Green-Refactor process. Each person writes the code to pass the
    current failing test, then the next failing test, so you switch roles
    when the test status is "red".

  - **Blitz**: this is a time-based exercise, where you set an overall time
    for a task (e.g. ten minutes) and allot each person half of it. Have a
    countdown running while each person is driving - once their time is up,
    they can't drive any more. This is a good way to even up the driving and
    navigating time, and can be done with a physical chess clock. You can
    increase the total time as you get more comfortable with it.

  - **Evil coder**: one person writes all of the tests, and the other then
    tries to make each test pass in an unexpected (or even actively
    counter-productive) way. This forces the test writer to drive out the actual
    behaviour they are looking for by constraining the code through
    additional tests. This can be carried out silently, with the pair
    communicating their intentations solely through the code they're writing.

  - **Mobbing**: more than two programmers working on the same task is
    referred to as "mobbing". This can be done with a single big screen and
    shared peripherals (ideally wireless, to make it easier to pass them
    around), as it's much harder to make sure no two people are typing at the
    same time in a larger group. I've found this particularly useful early in a
    project, where there isn't much surface area for multiple pairs to cover,
    or when introducing multiple new people to an existing codebase.

## Things to avoid

  - **Loud noises**: try not to talk too loudly, and get away from any loud
    noise sources before starting. There's a hum to a roomful of people
    pairing, but it shouldn't feel like you need to shout over what's going
    on around you. Equally you shouldn't be talking over your pair; pairing
    is about reaching a consensus on the approach to take.

  - **Strong smells**: it should go without saying that personal hygiene is
    important when you're sitting right next to someone all day. But it's
    also worth bearing in mind that some people are sensitive to smells that
    you think are nice; consider unscented toiletries and avoid strong
    perfume or aftershave.

  - **Taking over**: Don't start using the mouse and keyboard while your pair
    is trying to, it's very frustrating when the cursor suddenly runs away
    from you. Ask explicitly or make a clear move when you want to try
    something out. It can be helpful to push the peripherals away from you,
    to avoid nudging them accidentally and also give you a clear way to
    signal that you want to drive.

  - **Mobile phones**: it's just too easy to get distracted by your phone.
    Consider turning on a do-not-disturb mode, or at the very least ensure
    it's on silent. Try to take breaks mindfully - use short pauses in your
    pairing (e.g. running a test suite) to discuss what you've been working
    on, rather than immediately picking up your phone. It's useful to have a
    second computer for separate research, but keep it shut - open email is
    another distraction.

## When not to pair

Like many of the practices of XP, pair programming is a good default but
doesn't fit every situation. For example, you might find it more effective to
split up and solo when:

  - **Researching a problem you’re stuck on**: people read at different rates
    and absorb new ideas in different ways;

  - **Trying out new technology**: libraries, frameworks, new paradigms; or

  - **Taking breaks**: constant pairing can be tiring, especially when you’re
    new to it; don’t be afraid to ask for some time alone if you need it.

In general, you should agree specific end goals and time limits when you
split up, so you can both be working towards the same thing, and you should
bring *ideas*, rather than specific code or implementations, back to work on
with your pair.

## Additional resources

  - *“Pair Programming Illuminated”* by Laurie Williams and Robert Kessler

  - *“Strengthening the Case for Pair Programming”* by Williams, Kessler,
    Cunningham and Jeffries [[PDF][10]]

  - *“The Costs and Benefits of Pair Programming”* by Cockburn and Williams
    [[PDF][11]]

  - *“Pair Programming Configurations”* by Fred Mastropasqua [[Blog][12]]

  - *“Is pair programming worth the trade off in engineering resources?”* by
    Kent Beck [[Quora][13]]

  - *“Pair Programming: When and Why it Works”* by Chong, Plummer, Leifer,
    Klemmer, Eris and Toye [[PDF][14]]

 > **Update**: this post was revised to separate the *roles* of pairing (driver
 > and navigator) from the *methods* (e.g. blitz), as the presentation was
 > similarly updated.

 [1]: https://ada.ac.uk
 [2]: https://pivotal.io/labs
 [3]: http://agilemanifesto.org
 [4]: https://www.wired.com/2013/11/pivotal-one/
 [5]: http://parrit.cfapps.io
 [6]: https://github.com/pivotal/workstation-setup
 [7]: https://www.ansible.com/
 [8]: https://twitter.com/amesimmons
 [9]: http://amysimmons.github.io/a-guide-to-the-care-and-feeding-of-new-devs/
 [10]: https://collaboration.csc.ncsu.edu/laurie/Papers/ieeeSoftware.PDF
 [11]: https://collaboration.csc.ncsu.edu/laurie/Papers/XPSardinia.PDF
 [12]: https://www.clearlyagileinc.com/blog/2016/5/20/pair-programming-configurations
 [13]: https://www.quora.com/Is-pair-programming-worth-the-trade-off-in-engineering-resources/answer/Kent-Beck?srid=uL5a
 [14]: http://hci.stanford.edu/publications/2005/pairs/PairProgramming-WhenWhy.pdf
 [15]: https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it
