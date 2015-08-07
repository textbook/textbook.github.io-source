Title: Creating a blog in Pelican
Date: 2015-07-11 16:00
Tags: code, python, pelican
Authors: Jonathan Sharpe
Summary: The one you're reading right now, in fact!

Welcome to version 1.0 of my new blog site! I thought I'd start with a bit
of a meta-post about the creating of the blog and its current `meadowlark`
theme. A few particular comments on the process:

 * The combination of a static site generator like Pelican and simple hosting
 like GitHub pages does make it very easy to get a site up and running - I have
 the source hosted in one repository, set to ignore the `output` directory,
 then the actual site in `output` in a second repo, a push on the latter and
 the live site is updated.

 * GitHub's [Atom IDE][atom] is perfect for this level of project - I really
 like JetBrains' [PyCharm][pyc] for projects with more substantial development, but it
 can be a little heavy for smaller projects like these, and the fact that Atom
 is based on [Less CSS][less] gives me another technology to learn; and

 * I really do not get CSS yet - the easiest way for me to develop is way closer
 to trial and error than I'd like! Also: IE support is tricky, so I haven't
 bothered, and [GhostCSS][ghost] is a very handy tool for unbreaking my own
 errors.

So what's next? I have the following vague ambitions for improvements in the
coming weeks/months (*note to self: revise this to reflect whenever I get them
done!*):

 * I really like the way Campo Santo's website changes colour as you sit and
 watch it - I'm thinking of using the colour to reflect the time of year/day
 (e.g. split into spring/summer/autumn/winter and morning/afternoon/evening/night
 and having a suitable colour gradient for each one);

 * Rethink the code block theme - I've currently just taken the basic IDLE theme
 (the IDE that comes built-in with Python), it might be nice to do something
 a bit better matched with the rest of the site theme; and

 * Switch the theming to Less CSS (see above), which will hopefully also make the
 above tasks easier.

[atom]: http://atom.io/
[ghost]: http://wernull.com/2013/04/debug-ghost-css-elements-causing-unwanted-scrolling/
[less]: http://lesscss.org/
[pyc]: https://www.jetbrains.com/pycharm/
