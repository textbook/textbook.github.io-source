workflow "Deploy to gh-pages" {
  resolves = ["Pelican -> GH Pages"]
  on = "push"
}

action "Pelican -> GH Pages" {
  uses = "nelsonjchen/gh-pages-pelican-action@0.1.1"
  secrets = ["GITHUB_TOKEN"]
}
