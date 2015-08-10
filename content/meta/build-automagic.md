Title: Setting up a Travis build
Date: 2015-08-07 22:13
Tags: code, travis, pelican
Authors: Jonathan Sharpe
Summary: Making my own life easier, one shell script at a time

The one downside of using Pelican to build the site, as opposed to the Tumblr 
blog I was previously using, is that I have to *actually build the site*. This
means that I need to have software installed to write a new article which, 
while not really a huge problem, is slightly awkward. However, I'd read a few 
things about using online automated build/continuous integration services to 
build the site for me when I push to the source repo. This means I can write a 
new article on GitHub [*Ed*: it was right around this point that I thought *"oh 
yeah, I __can__ write this on GitHub!"*, and did so], and can therefore write
from pretty much anywhere.

So, I read a couple of posts about it, specifically:

 - [How to automatically build your Pelican blog and publish it to Github Pages][3]
 - [Publish your Pelican blog on Github pages via Travis-CI][4]
 - [Deploying Pelican Sites Using Travis CI][5]
 
I particularly liked this approach as some of the other posts I read use 
`ghp-import` and it seemed unnecessary to add a new dependency to the project 
when `git` provides the tools for pretty much everything that I want. Initially
I implemented it more-or-less as-is, using `rsync` to copy the changes from the
output folder to a fresh checkout of the deployment repo.

Once I had that working, I had a bit of a rethink. I figured that there might be 
something cleverer that I could do based on the structure I'm using; because the 
`output` folder is a submodule, it is already linked to the correct repo for 
publishing. The first problem I had is that, as I'm not now separately checking 
out the site repo, I'm relying on Travis's checkout. That isn't authenticated for
pushing, and a bit of research suggested that it isn't possible to modify the 
clone process, but you can add the correct origin back manually. Based on [this 
(criminally underrated) SO post][1], I added the following to `deploy.sh`:

```
:::shell
git remote rm origin
git remote add origin https://${GH_PAGES}@github.com/$TARGET_REPO
```

This caused my second problem, that I was now pushing to a detached `HEAD`, so
the changes weren't actually ending up in the `master` branch. To fix this took
[another SO question][2], which suggested committing to a temporary branch, 
committing the changes then switching that back into `master` before the push,
so I added:

```
:::shell
git checkout -b temp
...
git checkout -B master temp
```

And that did it! I'm planning to set this all up as a neat Pelican starter 
project that anyone can easily fork, so keep an eye out for that if you're 
interested in setting up your own Pelican site with minimal fuss.

  [1]: http://stackoverflow.com/q/19845679/3001761
  [2]: http://stackoverflow.com/q/5772192/3001761
  [3]: http://zonca.github.io/2013/09/automatically-build-pelican-and-publish-to-github-pages.html
  [4]: http://blog.mathieu-leplatre.info/publish-your-pelican-blog-on-github-pages-via-travis-ci.html
  [5]: http://kevinyap.ca/2014/06/deploying-pelican-sites-using-travis-ci/
