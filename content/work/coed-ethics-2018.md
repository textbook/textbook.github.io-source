Title: ({=}) Coed:Ethics 2018
Date: 2018-07-17 12:30
Tags: ethics, conferences
Authors: Jonathan Sharpe
Summary: My experience of the inaugural Coed:Ethics conference on ethical issues in the tech industry

Last Friday I travelled (all the way!) to the [Microsoft Reactor][1] community
hub in Shoreditch to attend the first ever [Coed:Ethics conference][2], the
first event of its kind dedicated to exploring the ethical issues that face
software developers and other technologists. The conference consisted of eight
talks, followed by a panel and open discussion.

## Talks

Eight half-hour talks made up the bulk of the day, from a range of speakers
across numerous topics around ethics in technology. The videos should be
available in the near future, but I've written my summary of each talk below.

### When Data Kills

The first ever Coed:Ethics talk was given by [Cori Crider][3], a human rights
lawyer. Her talk focused on tech companies' involvement with the military,
covering topics like machine learning for drone strike targeting. She also
talked about the efforts to draw up principles governing the development and
use of AI, for example prohibiting its usage in weapons systems.

One event she talked about was Google's involvement in Project Maven, a
research program aimed at improving object recognition in miltary drones.
Following an open letter signed by thousands of employees and at least a
dozen resignations, Google announced that it would not be renewing the contract.
This illustrates the power that employees in technology have to affect the
decisions their companies are making, especially if they are willing to stand
up in public for what they believe in. The people who are building these
technologies need to have a say in how it is being used.

For me, a key question from her talk was: _"what is the line between lethal
and non-lethal help?"_ My employer [recently worked][4] with the US Air Force
on a project to improve the efficiency of scheduling aircraft refuelling
flights. Is that far enough removed for comfort?

### What is a Data Citizen?

Next up was [Caitlin McDonald][7], talking about what data citizenship looks
like by drawing parallels between our civic lives in relation to law
and the government and our relationship with data science.

She cited [*"Weapons of Math Destruction"*][5] by Cathy O’Neil, which makes
argues that there are particular *kinds* of application that cause problems;
those that lack feedback cycles for improvement, for example. Caitlin
suggested that we as "data citizens" deserve to know what the rules we are
being evaluated by *are* and have a structure to *challenge* them (just as we
can read the law and appeal a legal decision in civic society).

She introduced several existing tools to support ethical decision making,
including the Open Data Institute's [Data Ethics Canvas][6], but made the
point that you also need a *culture of ethics* in a company. It's not enough
to apply the toolkit, you also need people willing to listen to the results
and act on them.

### Data Science in Action

The third talk was by Emma Prest and Clare Kitching from [DataKind][8], a
group that *"[brings] together top data scientists with leading social change
organizations to collaborate on cutting-edge analytics and advanced algorithms
to maximize social impact"*. In particular, they talked about the need to
embed ethics throughout the data science process, illustrating their points
with an example of working with a food bank to identify individuals in need
of further counselling.

They suggested building ethical concerns into the project right from the
scoping and kick-off stages, beginning by considering what the high-level
risks around worse-case outcomes and data could be. Then, as the project
continues, building bias assessments into the data and algorithm checking.
They highlighted the importance of involving a diverse range of people in the
process; not just the clients and the data scientists, but also the
developers, the users and other stakeholders.

One particularly interesting point they made was the need to consider whether
the model being developed is appropriate for the *"data maturity"* of the
organisation in question. In case study there was a board member with
experience in maths and data science, but what if the model continues to be
applied after they have left? How do you ensure ongoing governance of the
model and embed understandability and transparency into the process, so that
it doesn't end up getting misused or misapplied in the future?

Another was the impact of open sourcing tools and models; their open question
was whether it is better to make these things open source so that the broader
community can gain maximum benefit, or whether it's actually preferable
overall to keep a higher level of control and governance by keeping them
proprietary? Thinking about the context and the value is important here, are
we making things *better enough*?

### Psychology of Ethics 101

The final talk of the morning was by [Andrea Dobson][9], a psychologist
interested in what makes good people make bad decisions. She talked about
Milgram's work on obedience, highlighting the result that around 75% of people
will conform to something that they know is wrong, and that conformance is
actually *more* likely in more ambiguous circumstances. Given that we are
generally taught to defer to figures of authority, how can individual
contributors effectively raise the concerns to management?

This applies to technology, too; Andrea related the results of the [Stack
Overflow survey][10], where nearly 60% of respondents said that upper
management was ultimately most responsible for code that accomplishes something
unethical.

She advised listening to your emotions: do you feel guilty about what you're
doing? Why are you doing it? What matters to you personally?

 > Companies become ethical one person and one decision at a time.

One thing that can help this is providing an environment of psychological
safety, where individuals feel comfortable speaking up and voicing their
concerns. If you don't feel you have that, she suggested speaking to other
people (HR, regulatory bodies, friends, family, ...) who can help you figure
it out.

### Thinking Ethically at Scale

After lunch [Yanqing Cheng][11] talked about how and why we might care about
ethics, and how we can manage to both make the world a better place *and*
feel like we're doing so.

She highlighted the issue of human intuition and its failure to scale - for
example, people would donate roughly $80 dollars to help birds in oil slicks
whether they were told it affected 2,000, 20,000 or 200,000 birds. Part of the
problem is simply being bad at imagining large numbers; when she reframed
worldwide road traffic deaths as being more than every British Airways flight
from London to New York for a year crashing into the sea, that really brought
home the magnitude in a way the number alone didn't. The key lesson in that the
most effective actions are not always the most intuitive.

She talked about the Effective Altruism movement, trying to measure the
impact of different charities so that individuals can maximise the impact of
their personal donations. The **Who** (can have an impact on your goal),
**How** (can they help or obstruct), **What** (can I do to affect their
behaviour) model, a useful brainstorming technique, can be used to try to
identify the actions that give the biggest payoff for the largest number of
people and focus on what you can achieve as an individual.

*(Bonus points for being the only conference talk I've ever seen that included
lessons from Harry Potter fan fiction.)*

### Ethical Design

[Harry Trimble][12] was next, talking about the power that designers hold in
a world where software is everywhere, and their responsibility to give power
to those without it. He commented that ethical decisions are unavoidable,
even if the only option you may have is refusing to do the work or quitting
entirely. In particular, he talked about the issues around authentication and
consent in data management.

Two topics stood out for me:

 1. Informed, shared and delegated consent, allowing groups and communities to
    participate effectively in decision making or involve other parties that
    might have more appropriate information; and

 2. Accountability and transparency in automated decision making, for example
    providing a "snapshot" that identifies the version of the system and its
    state so that you can review and appeal the decision.

One interesting tool he talked about was the [Data Permissions Catalogue][13],
a collection of design patterns for sharing data. The idea of tools like this
is to bring a shared language to ethical issues, making them easier to
describe and discuss. This reminded me of one of the core ideas of
domain-driven design (DDD), the importance of having a shared, consistent
vocabulary (the *"ubiquitous language"*) within teams and projects.

### A Responsible Dev Process?

This was a two-part talk, starting with [Adam Sándor][14] talking about how
the idea of breaking down silos within companies and giving responsibility
and autonomy to teams can help people move from the idea that they're just a
small cog in a large machine to actually having ownership of what they are
building. These multi-disciplinary teams are more inclusive and having the
responsibility means you're more likely to make the right ethical decisions.

Next [Sam Brown][15] from Doteveryone talked about their work in [Responsible
Technology][17], defined as technologies that:

  - Do not knowingly create or deepen existing inequalities;

  - Recognise and respect everyone’s rights and dignity; and

  - Give people confidence and trust in their use.

She talked about the power that technologists have as people with the skills
to turn ideas into reality and introduced the "3C model", framing ethical
conversations around Context, Consequence and Contribution. Doteveryone are
working on assessments and tools to support the discussion, providing a model
for responsible practice and making responsibility the new normal, a key
business driver for growth and innovation rather than a side concern.

One question from the audience was whether adding more regulation and
associated cost to conform with security and other standards would entrench the
positions of larger companies and discourage smaller companies and startups.
One suggestion in response was being open about products' status, giving users
information about what has been done and what is planned. But as a company or
group and as individuals it's important to know your limits; if you're a
bridge-building startup, your bridges still have to *work*.

### How to Build a Good Product

The final talk of the conference was from Steve Worswick, creator of the
[Mitsuku][16] chatbot (and possibly the only man to have both three Loebner
prizes and two tracks on Scottish Clubland 3). He talked about some of the
ethical decisions he made when developing the bot, which is a general-purpose
chatbot rather than a virtual assistant like Siri or Alexa.

One specific decision was to train Mitsuku using supervised learning, rather
than allowing unsupervised learning like the infamous [Tay chatbot][18]. This
is extremely time-consuming, especially when trying to keep up-to-date with
current affairs so Mitsuku can respond appropriately, but allows him to keep
the bot family-friendly (despite the revenue temptation from more "romantic"
users). It can learn from a specific user, but *only for that user*, then
Steve chooses which rules to add to the general set.

Another set of interesting decisions was in dealing with the ~30% of users
who are abusive in some way (50% are "normal" users, the other 20% skeptics
and academics). Tame responses only seemed to encourage bullies, so the bot
currently uses a "5 strikes and you're out" system, combined with a flag on
the user that allows the bot to respond more strongly to abusive users
(although it never swears back at them).

## Discussion

The day finished with a panel and open discussion. A lot of different points
were talked about, I've summarised a few below:

  - **Education vs. regulation** - where do we start? We need to educate
    politicians in the issues before we can talk sensibly about regulation. But
    laws are often behind the times, and in a fast-moving industry we have a
    responsibility to do something.

  - **Ethics as a product** - can companies use ethics as a competitive
    advantage? Are there any downsides to doing so? People want to engage
    with ethical companies, but misuse can lead to cynicism if those
    principles aren't seen to be upheld.

  - **Not Invented Here** - what prior art is there, is this really something
    we need to figure out outselves? Psychologists and doctors, for example,
    already have mandatory ethics training and advice panels. We don't
    currently ask about ethics in interviews, so even where CS students have
    ethics modules they aren't seeing the benefit when it comes to entering
    the profession.

  - **Is Apple ethical** - should I get a different phone? The most ethical
    smartphone available is keeping the one you already have. Issues exist
    around the supply chain, e.g. conflict minerals, but Apple are doing good
    work around privacy and federated machine learning. There is a bottom
    line below which we won't accept a company, but it's hard to have a
    binary yes or no for most, especially when their products give a lot of
    utility.

## Summary

A few key thoughts:

 1. **Understanding power**: it's important for tech workers of all kinds to
    understand the power they hold. Software is, as we're often reminded,
    "eating the world", and as the industry grows skilled people will continue
    to be in high demand and have power as a result.

 2. **Collective action**: it would be easy to think that, because the
    working conditions and benefits in tech companies are already generally
    good, we have less need of unions and professional bodies, but it was clear
    from the discussion that there is a role for these groups in driving issues
    like ethics across the community. For example, the [Tech Workers
    Coalition][19] is working toward an inclusive and equitable tech industry,
    covering all kinds of workers involved in the industry. In a timely
    fashion, as I write this, the [ACM][20] is about to publish an updated
    ethical standard for the computing profession.

 3. **Diverse groups**: a few of the talks touched on the idea of involving
    more people, and more diverse groups, in discussions and decision making.
    This helps make sure we aren't missing simple problems that are just not
    obvious from our own point of view. Especially when building consumer
    products it's important to build groups that reflect broader populations
    and can bring more ideas and ways of solving problems to the table.

Finally, I'd like to thank the organisers for their work; the day went very
smoothly and it was great to see such a diverse group of speakers and
attendees talking about this important issue. Hopefully this is just the
start of something much bigger!

 > **Disclosure**: Pivotal paid for my attendance of this conference as part of
 > my professional development budget, and were a Gold level sponsor of the
 > conference. However, I have written this article as an individual; it
 > reflects my position and opinions, not necessarily those of my employer.

  [1]: https://developer.microsoft.com/en-us/reactor/
  [2]: https://www.coedethics.org/
  [3]: https://www.coricrider.com/
  [4]: https://www.fastcompany.com/40588729/the-air-force-learned-to-code-and-saved-the-pentagon-millions
  [5]: https://weaponsofmathdestructionbook.com/
  [6]: https://theodi.org/article/data-ethics-canvas/
  [7]: https://inamerryhour.com/
  [8]: http://www.datakind.org/
  [9]: https://twitter.com/andrea_kock
  [10]: https://insights.stackoverflow.com/survey/2018/
  [11]: https://twitter.com/YanqingCheng
  [12]: http://www.harrytrimble.co.uk/
  [13]: https://catalogue.projectsbyif.com/
  [14]: https://twitter.com/adamsand0r
  [15]: https://twitter.com/samcatbrown
  [16]: https://pandorabots.com/mitsuku/
  [17]: https://medium.com/doteveryone/introducing-the-three-cs-of-responsible-technology-5e1d7fae558
  [18]: https://www.technologyreview.com/s/601111/why-microsoft-accidentally-unleashed-a-neo-nazi-sexbot/
  [19]: https://techworkerscoalition.org/
  [20]: https://www.acm.org/
