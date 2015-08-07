Title: Switching Meadowlark to Less CSS
Date: 2015-08-03 22:00
Tags: code, pelican, css
Authors: Jonathan Sharpe
Summary: In which I faff around with webassets and reduce duplication

As [Atom], the primary IDE I'm using to develop and maintain this site, uses
[Less CSS][less] in its stylesheets, I thought I'd adopt it to reduce the style
duplication in the site's Meadowlark theme. However, this did not turn out to
be as easy as initially anticipated, so I thought I'd write down the steps in
case it helps someone else.

First, an introduction: Less is one of a number of CSS preprocessors that has
popped up to address some of the features lacking in vanilla CSS, such as
defining variables and nesting styles. This allows the reduction of duplication,
while still providing backwards compatibility and not giving the browser yet
another task to do before the user gets to see the page they asked for.

In case it took longer than expected to switch to Less I created a `less`
branch in Git for both the root website repo and the `meadowlark` submodule. I'd
already installed [webassets] (`pip install webassets`), which [Pelican] can use
to handle Less and other, similar tools (JavaScript minifiers, alternative CSS
preprocessors, *et al.*), and Less itself (`npm install -g less`), but I still
needed to ensure that Pelican and [Jinja] had the appropriate extension
installed. This entailed adding another Git submodule to the project, the
[`pelican-plugins` repository][plugins], to get access to the `assets` plugin.
Then I added:

```
:::python
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['assets']
JINJA_EXTENSIONS = ['webassets.ext.jinja2.AssetsExtension']
```

to the `pelicanconf.py`. This enables use of the `{% assets %}` statement in
templates, which will be used to process the `.less` files to `.css` as follows:

```
:::html
{% assets filters="less", output="css/main.css", "css/main.less" %}
<link rel="stylesheet" href="{{ SITEURL }}/{{ ASSET_URL }}">
{% endassets %}
```

This tells Jinja to take the `main.less` file, run it through the `less` filter,
save it as `main.css` and use it in the template. Initially I started by
simply renaming the former `main.css`, but once the process was working I was
able to start using Less's syntax to rearrange it; leaving, crucially, one
single, canonical definition of the three main site colours.

So that's *one* of the [things I claimed I would do][meta] ticked off, which
isn't bad going!

  [atom]: https://atom.io/
  [jinja]: http://jinja.pocoo.org/
  [less]: http://lesscss.org/
  [meta]: {filename}meta-meadowlark.md
  [pelican]: http://docs.getpelican.com/
  [plugins]: https://github.com/getpelican/pelican-plugins.git
  [webassets]: https://webassets.readthedocs.org/en/latest/
