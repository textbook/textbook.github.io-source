Title: Setting up static files in Django
Date: 2015-08-15 18:47
Tags: code, python, django
Authors: Jonathan Sharpe
Summary: Avoiding duplication of static files by using Mercurial hooks.

I've recently been working on a project to port a web application that I wrote 
at work in .NET to Python, using the Django framework. I wanted to see what the
advantages of using a language I'm more familiar with and adopting an agile, 
test-driven development methodology would be. I'm hosting it on [Python 
Anywhere][anywhere], which offers a great (and free, if your needs are 
relatively small) hosting service for Python web apps.

One thing to be aware of with Django is its handling of static files; there's 
a [whole manual page][static] on how to go about dealing with CSS and other
assets in testing and deployment, but the short version is that the deployed
version really needs to have all of the static files collected from their apps
(`/app/static/app/...`) to a central directory (`/static/app/...`). This is
easily achieved using `./manage.py collectstatic`, but means two copies of those
files in the working copy.

I already had [an open issue][issue] on another Django-based project to avoid 
this kind of duplication; I used a commit hook there to run `collectstatic` on 
the development side, then push everything, which means that there are two copies 
of the site's static files in the repository. Instead, I decided for this new 
project to move the automated static collection to the `hg update` command (it's 
hosted on a private BitBucket repo using Mercurial, rather than Git, as I wanted 
to try out the other option). This means that it runs on the server side, and 
required two changes:

 1. Adding `^static/` (the static file directory in the root folder, which I'd 
 set up as `STATIC_ROOT` for the project) to the `.hgignore`, so that its 
 contents weren't being tracked by Mercurial; and
 
 2. Adding an `update` hook to `.hg/hgrc` to perform the static file collection
 when I update the repository.
 
The latter looks like:

```
:::bash
...
[hooks]
update = ./manage.py collectstatic --noinput 
```

which I think is pretty self-explanatory! Now only one copy of the CSS is kept
in the central repository, but the deployed site is set up automatically when
I pull down the changes from that repo and update the working copy.
  
  [anywhere]: https://www.pythonanywhere.com/
  [issue]: https://bitbucket.org/jonrsharpe/dj_cv/issues/3/reduce-duplication-of-static-files
  [static]: https://docs.djangoproject.com/en/1.8/howto/static-files/
