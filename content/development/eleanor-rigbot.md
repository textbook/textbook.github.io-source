Title: Eleanor Rigbot
Date: 2017-05-14 13:00
Tags: code, python, twitter
Authors: Jonathan Sharpe
Summary: My first Twitter bot, searching Liverpool's tweet stream for new verses to Eleanor Rigby

 > Eleanor Rigby, picks up the rice 
 >
 > In the church where a wedding has been
 >
 > Lives in a dream
 >
 > <small>**Eleanor Rigby**, by the Beatles (*Lennon-McCartney, 1966*).</small>

The song [Eleanor Rigby][2] has a distinctive syllabic pattern and rhyming
scheme, and it's fun to try and come up with additional verses. But what if we
could find them automatically, instead?

Since the people behind Clitoris Vulgaris ([@clitoscope][3]), a Twitter bot
designed to *"generate new species of clitoris by projecting botanical
illustrations onto a 3D model"*, gave a talk at work about how they built it,
I've been interested in the idea of making a bot of my own. Creating something
to look for tweets that could be a new verse seemed doable as a first attempt.

## Libraries
   
I'd initially looked at using [NLTK][4] to do the language processing; one
corpus available for it, the Carnegie Mellon Pronouncing Dictionary, seemed
perfect for the project. However, I wasn't sure how to go about running an 
NLTK-based app on Cloud Foundry, as it needs to download the corpus once `pip
install`-ed. Fortunately, someone else had already done the hard work for me
and wrapped that single corpus in a library named [`pronouncing`][5]; using
this made the bot trivial to deploy. This allows for both determining the
syllables in the words used and whether two given words rhyme.

Using the [Tweepy][6] library made interacting with Twitter simple; I
subclassed the existing `StreamListener` with my own `RetweetListener`, which
takes an `extractor` (for extracting the text to process from a tweet) and a
`filterer` (for filtering out tweets that should be retweeted). This keeps it
very general for reuse later. Tweets are not exactly written in formal English
and contain things like usernames, hashtags and URLs that can't necessarily be
pronounced, so the current extractor takes the longest string of *"clean
characters"* (the letters A-Z plus some basic punctuation characters, not
including characters like `@` and `#` with Twitter-specific meanings) from each
tweet to pass to the filtering.

## Classification

The actual classification happens in [`PhraseMatcher.__call__`][1], and the
overall process is pretty straightforward:

 1. Given a phrase string, e.g. `'here are some example words'`;
 1. Create a list of the individual words and their lengths in syllables, e.g.
    `[('here', 1), ('are', 1), ('some', 1), ('example', 3), ('words', 1)]`
 1. If any word couldn't be processed or the total syllable count doesn't match
    the pattern we're looking for, return `False`;
 1. Try to fit the words into the required syllable pattern, assuming that we
    want lines to break on words;
 1. If the phrase doesn't fit into the syllable pattern, return `False`; and
 1. Return whether or not the phrase matches the required rhyming scheme.
 
The scheme is defined with two sequences: one of the number of syllables in
each line; and one of the required rhyming scheme. For example, the scheme to
match a verse of Eleanor Rigby is:

```python
ELEANOR_RIGBY = PhraseMatcher(
    syllable_pattern=(5, 4, 9, 4),
    rhyming_scheme=(None, None, 0, 0),
)
```

This means:

 - there should be four lines, with five, four, nine and four syllables
   respectively (for a total of 22); and
 - the third and fourth lines must rhyme (but we don't care whether or not the
   first two lines rhyme with anything).

This representation makes the bot configurable for different phrases, including
the other example I give in the README (note that here the rhyme scheme is
marked with letters - it gets converted to a dictionary mapping group ID to
line indices, so anything hashable is fine):

```python
# https://www.flickr.com/places/info/12591829
napoli = [13.8509, 40.5360, 14.6697, 41.0201]

# "when the moon hits your eye like a big pizza pie"
that_is_amore = PhraseMatcher((3, 3, 3, 3), (None, 'a', None, 'a'))

start_listening(napoli, that_is_amore)
```

## Results

The very first retweet is probably still the best so far:

 > It's kinda shitty when people say they care then act like they don't give
 > two shits about you
 >
 > <small>Charley Emmett (@Ch4rl3y_B0y) [April 6, 2017][7]</small>
 
which becomes:

 > It's kinda shitty, when people say
 > 
 > They care then act like they don't give two
 > 
 > Shits about you

Aside from an overly-strict definition of rhyming (some rhymes from the actual
song, like *"grave"* and *"saved"*, aren't considered valid), the
classification seems to be working pretty effectively. The extraction is not as
good; it doesn't necessarily find the real content of the status correctly. For
example, one of the weakest matches so far is:

 > Away to [@NewportSarries][13] tomorrow 
 >
 > End of the season is in sight 
 >
 > And it's going to be a glorious day 🌞just what you want as a front row
 > 
 > <small>Malpas RFC (@MalpasRugbyClub) [April 7, 2017][8]</small>
 
This is being classified as:

 > Tomorrow end of, the season is
 >
 > In sight and it's going to be a
 >
 > Glorious day

Most of the content of the tweet is being discarded, so it's not obvious from
reading it where the verse is.

## Next steps

A few improvements I've thought of:

 1. To make it more obvious what the matched "verse" is, I could switch from
    retweeting to quoting, so the bot can include the match in its response.
    However, that might make it seem more invasive.
    
 1. Instead of the separate extraction and classification steps, the extraction
    could be based on the longest series of pronounceable words in the tweet.
    This would mean using the default no-op `_all_text` extractor in the 
    `RetweetListener` and moving the extraction into the `PhraseMatcher` class.
    
 1. It might be nice to include pronounceable user names and hashtags in the
    match, although splitting those with multiple words in may prove tricky.

 [![Eleanor Rigby - geograph.org.uk - 1457024.jpg][9]][10]

<small>By john driscoll, [CC BY-SA 2.0][11], [Link][12].</small>

  [1]: https://github.com/textbook/eleanor-rigbot/blob/9bedfdce7def83cb13021e3751f55716d9a3a307/eleanorrigbot/classify.py#L42
  [2]: https://en.wikipedia.org/wiki/Eleanor_Rigby
  [3]: https://twitter.com/clitoscope
  [4]: http://www.nltk.org/index.html
  [5]: https://pypi.python.org/pypi/pronouncing
  [6]: http://docs.tweepy.org/en/latest/
  [7]: https://twitter.com/Ch4rl3y_B0y/status/850067453761773569
  [8]: https://twitter.com/MalpasRugbyClub/status/850270568066588672
  [9]: https://upload.wikimedia.org/wikipedia/commons/d/d7/Eleanor_Rigby_-_geograph.org.uk_-_1457024.jpg
  [10]: https://commons.wikimedia.org/wiki/File:Eleanor_Rigby_-_geograph.org.uk_-_1457024.jpg#/media/File:Eleanor_Rigby_-_geograph.org.uk_-_1457024.jpg ""
  [11]: http://creativecommons.org/licenses/by-sa/2.0 "Creative Commons Attribution-Share Alike 2.0"
  [12]: https://commons.wikimedia.org/w/index.php?curid=14199222
  [13]: https://twitter.com/NewportSarries
