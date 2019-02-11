Title: Automation for the people
Date: 2019-02-10 15:30
Modified: 2019-02-11 10:15
Tags: code, javascript, npm
Authors: Jonathan Sharpe
Summary: Making developers' lives easier and more productive with package file automation

If you're working in the JavaScript ecosystem, your project is likely based
around a `package.json` file. This is used by [NPM] for defining the
attributes of your package, including its `"name"` and `"version"`. You may
have noticed that one of the other options in the package file is `"scripts"`.
By default, this contains a single task:

    :::json
    {
        "...": "...",
        "scripts": {
            "test": "echo \"Error: no test specified\" && exit 1"
        }
    }

This is an inauspicious start to what I think is a pretty powerful entry point
to high-level developer automation.

## Why automate?

It's hopefully not controversial to state that developer time is _expensive_
and you only want to spend that expensive, finite resource on things that are
valuable to the business. Automation can minimise the time spent on repeating
simple tasks that happen many times a day, like linting or testing the code.

Package scripts provide a way to do this within the tooling your developers are
likely already using on a daily basis. They don't need to learn a new tool and
all of the existing NPM packages are available to help them out. It's also
easy to expand when you need to, because they can start writing more complex
processes as `.js` Node scripts or `.sh` shell scripts and still invoke them
via `npm run`.

Using the package scripts as an entry point also allows you to keep a
consistent "developer API" across multiple projects. For example, when I
switched [`fauxauth`][fauxauth] over to TypeScript, using package scripts for
all common tasks (running e.g. `npm run lint` rather than calling `eslint`
directly) meant that I could change the meaning of the scripts in [the package
file][fauxauth package] without having to change the commands I was executing
(or update the CI configuration). This could also be beneficial if your
developers work across multiple technologies; `npm run lint` could call
`eslint` for React in some projects and the Angular CLI's `ng lint` in others,
but the developer experience would be consistent.

### Sidebar: linting

One of the least valuable things for your developers to spend time on is what
the code looks like, particularly in the JavaScript ecosystem where you
rarely ship the code you're writing without some kind of transpilation or
bundling. You also don't want them to spend time trading commits back and
forth switching `'` for `"` and vice versa; the smaller the diffs, the easier
it is to figure out what's meaningfully changed when reviewing a commit, the
better (for the same reason I think trailing commas are a good thing!)

In general, the less they have to think about, the better; although the [ASI]
rules are fairly straightforward, for example, using semicolons everywhere means
they *never have to consider it*. Modern tools can generally do this for them;
individuals can write the code how they want to, then auto-fix on type, save or
lint to the agreed shared rules. The team can now focus more of its time on
delivering the things that matter to your users.

I also don't think you should have any warnings when you run linters; things
you actually care about get lost in the noise. Every rule should either be an
error or ignored completely, so it's unambiguous what's important, and any
error should fail the build.

## Hints and tips

- `"task:step"`: this is a very common convention for writing scripts, using
  a colon in the script name to indicate some kind of sub-step or configuration
  option. For example:

        :::json
        {
            "...": "...",
            "scripts": {
                "test": "...",
                "test:cover": "npm run test -- --coverage"
            }
        }

    or

        :::json
        {
            "...": "...",
            "scripts": {
                "start": "npm run start:compile && npm run start:watch",
                "start:compile": "...",
                "start:watch": "..."
            }
        }


- `pre` and `post`: all package scripts get a "free" pre- and post- script hook.
  All you need to do is include another entry with the same name prefixed with
  `pre` or `post` and this script will get run at the appropriate point in the
  lifecycle, assuming everything so far has exited zero.

        :::json
        {
            "...": "...",
            "scripts": {
                "test": "...",
                "posttest": "./collect-coverage.sh"
            }
        }

- `-- <args>`: any arguments to `npm run thing` are passed to `npm run`, _not_
  `thing`. To pass arguments to `thing` you need to include `--`, to indicate
  the end of the arguments to `npm run`. For example, to pass the argument
  `--port=3000` to the `serve` script, you'd do:

        :::bash
        $ npm run serve -- --port=3000

## Helpful libraries

Here are a few great "glue" libraries I've used frequently in other projects:

- [`concurrently`][concurrently]: run multiple processes at once. Very helpful
  for a local [dev setup] with watching processes on both the server and client
  builds, for example.

- [`cross-env`][cross-env]: set environment variables in your package scripts,
  cross-platform. If you're externalising configuration to env vars and want
  your project to run correctly on both Windows and \*nix, this is a must.

    `cross-env` was also the target of the first package discovered in the
    [`hacktask`][hacktask] account, a set of malicious typo-squatting packages
    that sent the user's environment variables to a remote server. Be careful
    to double-check that you're installing what you think you are.

- [`husky`][husky]: turn package scripts into [git hooks]. Never again will you
  accidentally break the build by pushing code that doesn't pass the tests!

- [`rimraf`][rimraf]: `rm -rf` for Node. Handy for clearing out output
  directories to ensure a clean state before running a build.

- [`wait-on`][wait-on]: wait for things to be ready. I've used this to run E2E
  tests against a local dev server, making sure the server is actually spun up
  and providing responses before kicking off the test suite.

## Downsides

There are a couple of downsides I've noticed to doing automation predominantly
through the package file.

One is simply _length_; as you add more complexity to your automation, either
you have very long lines, or lots of sub-steps, or sometimes both. For
example, [this project][project flamingo] that I worked on has 43 scripts,
steps and pre-/post- hooks for performing various tasks. This led to having a
separate [wiki page] listing what they are and what they do, as putting
comments in a JSON file is not straightforward (see [_"How do I add comments to
package.json for npm install?"_][package comments] for one option). Now there
is a risk that, as the scripts are updated and added to, the wiki page does not
stay up-to-date with what they currently do. You could move the steps out to
shell or Node scripts, or use an additional tool like [`nps`][nps], but that's
yet another thing to think about.

Another is the difficulty of handling arguments when _combining_ scripts. As
mentioned above you can split a complex process into multiple steps and call
each of them in turn:

    :::json
    {
        "...": "...",
        "scripts": {
            "process:first": "...",
            "process:second": "...",
            "process": "npm run process:first && npm run process:second"
        }
    }

But what if you want to pass an argument down to one of the sub-steps? `npm run
process -- --something` won't do it, so you often end up writing several
scripts to call the same processes with different arguments.

## Bonus round: Yarn

The other major packaging option in the Node ecosystem is [Yarn]. This uses
the same `package.json` file as NPM, so switching over is relatively
straightforward. I won't go into the pros and cons here, but one thing to
note is that running scripts and passing arguments is a little simpler in Yarn
than in NPM; to run a script and pass arguments, instead of:

    :::bash
    $ npm run thing -- --arg

you can just do:

    :::bash
    $ yarn thing --arg

## Further reading

Here are some useful articles and references:

- [NPM CLI flags] from the official documentation
- [NPM scripts: tips everyone should know] by [Corgibytes]
- [How to use NPM as a build tool] by Keith Cirkel
- [Helpers and tips for NPM run scripts] by Michael Kuehnel

[ASI]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#Automatic_semicolon_insertion
[concurrently]: https://www.npmjs.com/package/concurrently
[cross-env]: https://www.npmjs.com/package/cross-env
[corgibytes]: https://corgibytes.com/
[dev setup]: https://github.com/textbook/cyf-app-starter/blob/7ed846f0cfea766b7136368ef78f9f1d1650ead4/package.json#L16
[fauxauth]: https://www.npmjs.com/package/fauxauth
[fauxauth package]: https://github.com/textbook/fauxauth/commit/135376876aca5c16f9fbe2d89a3389f3ddf9f2d8#diff-b9cfc7f2cdf78a7f4b91a753d10865a2
[git hooks]: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
[hacktask]: https://blog.npmjs.org/post/163723642530/crossenv-malware-on-the-npm-registry
[Helpers and tips for NPM run scripts]: https://michael-kuehnel.de/tooling/2018/03/22/helpers-and-tips-for-npm-run-scripts.html
[How to use NPM as a build tool]: https://www.keithcirkel.co.uk/how-to-use-npm-as-a-build-tool/
[husky]: https://www.npmjs.com/package/husky
[NPM]: https://docs.npmjs.com/cli-documentation/
[NPM CLI flags]: https://docs.npmjs.com/misc/config#shorthands-and-other-cli-niceties
[NPM scripts: tips everyone should know]: https://corgibytes.com/blog/2017/04/18/npm-tips/
[nps]: https://www.npmjs.com/package/nps
[package comments]: https://stackoverflow.com/q/14221579/3001761
[project flamingo]: https://github.com/HelpRefugees/project-flamingo/blob/93011e309ac3026b995c95e9dc1241fb05b5c553/package.json#L6-L51
[rimraf]: https://www.npmjs.com/package/rimraf
[wait-on]: https://www.npmjs.com/package/wait-on
[wiki page]: https://github.com/HelpRefugees/project-flamingo/wiki/Package-Scripts
[Yarn]: https://yarnpkg.com/
