Title: Meta recursion: meta-post about meta-tags
Date: 2016-12-04 12:00
Tags: pelican, code
Authors: Jonathan Sharpe
Summary: Integrating OpenGraph/Twitter meta-tags into a Pelican blog theme.

Social media networks like Twitter, Facebook and LinkedIn support the use of
`<meta>` tags in your HTML to provide additional information when displaying
links to websites. Facebook and LinkedIn use [OpenGraph][2] tags; Twitter 
accepts some OpenGraph tags plus [a few of its own][7]. Providing these tags
allows you some customisation of how your pages are displayed when people share
links to them through these networks.

I've recently added suport for these tags into [Bulrush][3], the theme currently
used on this blog. What this means is that if you drop the link to one of my
articles, e.g. `http://blog.jonrshar.pe/2015/Jul/06/context-manager-case.html`,
into [the Twitter Cards validator][1], you will see something like the
following:

 ![Twitter Cards Preview]({static}/images/twitter-card-preview.png)
 
You may wonder how this is implemented. I'm using [template inheritance][5],
provided by the Jinja2 template engine, to allow child templates to override
their parents via `block` and `extends` elements, and [the `include`
statement][6] to bring in the defined tags.

There's a single file representing the meta tags (`meta_tags.html`):
 
```html
<meta property="og:title" content="{{ SITENAME }}{% if item.title %} - {{ item.title }}{% endif %}">
{% if item.summary %}
  <meta property="og:description" content="{{ item.summary | striptags | truncate(200, end='...') }}">
{% endif %}
<meta property="og:url" content="{{ SITEURL }}/{{ item.url }}">
{% if AVATAR %}
  <meta property="og:image" content="{{ SITEURL }}/images/{{ AVATAR }}">

  <meta name="twitter:image:alt" content="{{ SITENAME }}{% if SITESUBTITLE %} | {{ SITESUBTITLE }}{% endif %}">
{% endif %}
<meta name="twitter:card" content="summary">
{% if TWITTER_USERNAME %}
  <meta name="twitter:creator" content="@{{ TWITTER_USERNAME }}">
  <meta name="twitter:site" content="@{{ TWITTER_USERNAME }}">
{% endif %}
```

Some of the interpolated variables, like `SITENAME`, are set in the root
`pelicanconf.py` and made available everywhere in the templates. The [`with`
statement extension][4] allows the `item` to be injected from the template
displaying the specific item I want to be tagged when they `include` the 
sub-template, e.g. for the articles (see `article.html`):

```html
{% block tags %}
  {% with item=article %}
    {% include 'meta_tags.html' %}
  {% endwith %}
{% endblock %}
```

the `item` is the [`article` object][8]. Similarly, for generic pages like the
About page, the injected `item` is the [`page` object][9]. These both have
similar properties, like `summary`, `title` and `url`, so it's easy to plug
either of these into the general tag layout. `{% block tags %}` simply means
that the rendered markup will "fill in" the defined block from a parent
template, in this case in `base.html`'s `<head>` element.

Hopefully this demonstrates how useful the template inheritance functionality of
Jinja can be. You can see [the full commit][10] on GitHub; it took under 30
lines of HTML to add automatically-generated meta-tags to the relevant pages.
If you're using Pelican to generate your blog, feel free to give Bulrush a try
and let me know what you think. Alternatively, you can use the above ideas to
add similar functionality to your own Pelican theme, or any other Jinja2-based
site.

  [1]: https://cards-dev.twitter.com/validator
  [2]: http://ogp.me/
  [3]: https://github.com/textbook/bulrush
  [4]: http://jinja.pocoo.org/docs/dev/extensions/#with-statement
  [5]: http://jinja.pocoo.org/docs/dev/templates/#template-inheritance
  [6]: http://jinja.pocoo.org/docs/dev/templates/#include
  [7]: https://dev.twitter.com/cards/markup
  [8]: http://docs.getpelican.com/en/3.6.3/themes.html#article
  [9]: http://docs.getpelican.com/en/3.6.3/themes.html#page
  [10]: https://github.com/textbook/bulrush/commit/78579cb3dba20c52a7f12f98a4e3cfbe2bbac051
