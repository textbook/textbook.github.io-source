Title: Publishing npm packages with service accounts 
Date: 2019-01-14 19:40
Tags: code, javascript, ci, npm 
Authors: Jonathan Sharpe
Summary: 2FA adds security to your npm account but complicates the process of publishing from CI; here's one way around that

Since October 2017, npm has supported [2-factor authentication][1] (2FA). This
is good for security, and I've enabled it for both authorisation and publication
on my main account, but it's difficult to use if you want to publish packages
automatically from CI (e.g. using [Travis CI][3]):

```
npm ERR! publish Failed PUT 401
npm ERR! code E401
npm ERR! This operation requires a one-time password from your authenticator.
npm ERR! You can provide a one-time password by passing --otp=<code> to the command you ran.
npm ERR! If you already provided a one-time password then it is likely that you either typoed
npm ERR! it, or it timed out. Please try again.
```

I have found [one proof of concept][2] method using Hashicorp's [Vault][4] to
provide a TOTP code as needed, but this requires a lot of external setup if
you're not already using Vault as part of your workflow.

Instead, I've set up a second, "service" account to use when publishing
from CI. Here's how:

1.  First, you need to create a new npm user to act as the service user for
    automated deploys. Unfortunately, npm doesn't currently give you a way to
    add a description to a user, but I've set the service user up with the same
    GitHub and Twitter handles as my main account, so it's hopefully clear who
    it belongs to. I've also given it a spiffy robot avatar via Gravatar. Enable
    2FA, but make sure it's only for _Authorization_, not _Authorization and
    Publishing_.

2.  Next, create a token for use in the CI environment. Switch to the _Tokens_
    tab (or navigate directly to `https://www.npmjs.com/settings/{user}/tokens`)
    and click _Create New Token_. This will need to be set to the _Read and
    Publish_ level.

3.  Finally, log in with your main account, visit the package you want to give
    the service account access to and switch to the _Admin_ tab (or navigate
    directly to `https://www.npmjs.com/package/{package}/access`). In the
    **Invite maintainer** section, type the name of your service account and
    click _Invite_. You should then see something like this:

    ![fauxauth maintainers list]({static}/images/fauxauth-maintainers.png)

You can use the service account token in your CI environment for automated
deploys, without needing to reduce the security of your main account. I'd
recommend creating one service account per package so a breach doesn't impact
multiple different projects (and, as always, using a password manager to create
long, secure passwords that aren't reused).

One major downside is that you can't enable the _"Require Two Factor
Authentication to publish or modify settings"_ option for your package while
you're using non-2FA service accounts. If you have other maintainers, make sure
they _are_ using full 2FA on their main accounts.

[1]: https://blog.npmjs.org/post/166039777883/protect-your-npm-account-with-two-factor
[2]: https://medium.com/@sgyio/how-to-deploy-npm-package-with-2fa-enabled-on-write-49843bf493a8
[3]: https://docs.travis-ci.com/user/deployment/npm/
[4]: https://www.vaultproject.io/
