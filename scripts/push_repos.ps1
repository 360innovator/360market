# MARINER Push Script – Sync All Repos for 360innovator

# Set your GitHub token securely before running
# Example:
# $env:GITHUB_TOKEN = "YOUR_TOKEN_HERE"

$githubUsername = "360innovator"

$repos = @(
    "mariner-core",
    "360market",
    "logger-engine",
    "deepseek-module",
    "grant-tracker",
    "youth-workforce-ai"
)

foreach ($repo in $repos) {
    git init
    git remote add origin "https://$env:GITHUB_TOKEN@github.com/$githubUsername/$repo.git"
    git add .
    git commit -m "Mariner sync: Pushing $repo" -q
    git branch -M main
    git push -u origin main
}
