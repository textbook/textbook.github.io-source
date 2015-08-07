Title: Creating a static Polymer site on Divshot
Date: 2015-07-23 20:20
Tags: code, javascript
Authors: Jonathan Sharpe
Summary: An adventure in modern web development; fun with Bower, Node.JS, and more.

I recently acquired a new domain; having decided that `jonathansharpe.me.uk` was
a little unwieldy, I decided to look around for something a little shorter,
settling on `http://jonrshar.pe` (registered in Peru; [Nathan Barley][trashbat],
eat your heart out). However, although I wanted it primarily for email (`mail@...`)
purposes, I thought it would be nice to have something up for people to look at
if they wandered onto the domain.

Having recently become aware of [Polymer], a Web Components library whose `paper`
elements implement Google's ["material design"][md], I thought I would give it
a go; getting a better grip of the front-end technologies (principally HTML,
CSS and JavaScript) is firmly on my to-do list, and it seemed easy enough to
get stuck into. Installing its components was a matter of getting [Node.js], then
[Bower] (the de-facto web package manager), then Polymer itself. Already that's
another two things to add to my list, and that's before we get into the various
things I've (skim-)read about putting together a development workflow with Grunt
and TravisCI (which I've used on a Python project before).

Writing the site itself was actually reasonably straight-forward; Polymer has
extensive documentation (although some of it's a bit of a work-in-progress)
with examples for the majority of the components. Slotting together the various
parts to build a site with a simple, one-page internal navigation system didn't
take too long, although there was a bit of back and forth and trial and (lots
of) error before it looked neat. It's a nicely modular system, at least;
although I'm not yet making best use of it, you can relatively easily create
reusable components to drop in where required. And it does look nice, a very
modern, "flat" approach you might expect from Google.

Local testing also proved a little trickier than expected - now that JS is
involved I can no longer test via `file://`, so had to get Apache properly set
up to host from `~/Sites` That meant more tinkering with config files in `vi`
(one day I will definitely learn more shortcuts than `!q`, aka *"get me out of
here!"*, honest...) and another list item (I really don't like relying on
things I don't understand, but this list's getting longer faster than I can keep
up with it!)

Next I needed somewhere to host it; [Divshot] offers free static site hosting
with a neat web front-end and a command line tool that starts up like an 80s
computer game:

```
_____ _______      _______ _    _  ____ _______
|  __ \_   _\ \    / / ____| |  | |/ __ \__   __|
| |  | || |  \ \  / / (___ | |__| | |  | | | |
| |  | || |   \ \/ / \___ \|  __  | |  | | | |
| |__| || |_   \  /  ____) | |  | | |__| | | |
|_____/_____|   \/  |_____/|_|  |_|\____/  |_|

Application-Grade Static Web Hosting

Host single-page apps and static sites with
all the power of a modern application platform.
```

It also manages multiple versions of the site, allowing a separation between the
development version and staging and live deployments, as well as easy rollbacks
in case I screw something up (which seems all-too-likely at this point).

Unfortunately, after all of that, it only appears to work correctly in Google's
Chrome browser - both Safari and Firefox on my Mac refuse to let the changing
tabs actually change the displayed content (IE on my work PC won't even *show*
the tabs, which is at least consistent!) So now I have to learn how to debug and
troubleshoot a JavaScript application - more new skills! Divshot's split between
development, staging and production versions will hopefully make it easy to play
with variants, at least. Also, I should work out how not to sync the whole of
Polymer to their servers...

  [bower]: http://bower.io/
  [divshot]: https://divshot.com/
  [md]: https://www.google.com/design/spec/material-design/introduction.html
  [node.js]: https://nodejs.org/
  [polymer]: https://www.polymer-project.org/
  [trashbat]: http://www.trashbat.co.ck/
