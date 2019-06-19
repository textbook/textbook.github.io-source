workflow "Deploy to gh-pages" {
  on = "push"
  resolves = ["Publish to gh-pages"]
}

action "Checkout submodules" {
  uses = "./.github/submodules"
}

action "Publish to gh-pages" {
  uses = "nelsonjchen/gh-pages-pelican-action@0.1.1"
  needs = ["Checkout submodules"]
  secrets = ["GITHUB_TOKEN"]
}
