workflow "Deploy to gh-pages" {
  on = "push"
  resolves = ["Publish to gh-pages"]
}

action "Checkout submodules" {
  uses = "textbook/git-checkout-submodule-action@1.0.1"
}

action "Publish to gh-pages" {
  uses = "nelsonjchen/gh-pages-pelican-action@0.1.1"
  needs = ["Checkout submodules"]
  secrets = [
    "GIT_DEPLOY_KEY",
  ]
}
