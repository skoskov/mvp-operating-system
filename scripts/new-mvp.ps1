param(
  [Parameter(Mandatory=$true)]
  [string]$ProjectName,

  [string]$DevRoot = "C:\Users\skoskov\Documents\_DEV",
  [ValidateSet("private", "public", "internal")]
  [string]$Visibility = "private",
  [bool]$PushToGitHub = $true
)

$ErrorActionPreference = "Stop"

if ($ProjectName -notmatch '^[a-zA-Z0-9._-]+$') {
  throw "Invalid project name: $ProjectName. Use only letters, numbers, dot, underscore, hyphen."
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OsRoot = Split-Path -Parent $ScriptDir
$TemplateDir = Join-Path $OsRoot "template\mvp-project-template"
$ProjectDir = Join-Path $DevRoot $ProjectName

if (-not (Test-Path $TemplateDir)) {
  throw "Template not found: $TemplateDir"
}

if (Test-Path $ProjectDir) {
  Write-Host "Project already exists: $ProjectDir"
  Write-Host "Open it in Codex and run bootstrap/recovery from there."
  exit 2
}

New-Item -ItemType Directory -Force -Path $DevRoot | Out-Null
Copy-Item -Recurse -Path $TemplateDir -Destination $ProjectDir
Set-Location $ProjectDir

Get-ChildItem -Recurse -Filter ".gitkeep" | Remove-Item -Force -ErrorAction SilentlyContinue

if (-not (Test-Path "README.md")) {
@"
# $ProjectName

MVP project initialized from mvp-operating-system template.

## Operating flow

Use the mvp-operating-system skill before implementation:
memory preflight → decision cards → token budget → OpenSpec → independent review → Codex implementation → verification → learning update.
"@ | Set-Content -Encoding UTF8 "README.md"
}

if (-not (Test-Path ".gitignore")) {
@"
.venv/
__pycache__/
*.pyc
.env
.env.*
.DS_Store
.vscode/
.idea/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
node_modules/
"@ | Set-Content -Encoding UTF8 ".gitignore"
}

git init | Out-Null
git branch -M main

git add .
git commit -m "Initial MVP operating system bootstrap" | Out-Null

Write-Host "Created local Git repo: $ProjectDir"
Write-Host "Branch: main"

if ($PushToGitHub) {
  $gh = Get-Command gh -ErrorAction SilentlyContinue
  if ($gh) {
    try {
      gh auth status | Out-Null
      gh repo create $ProjectName --$Visibility --source=. --remote=origin --push
      Write-Host "GitHub repo created and pushed: $ProjectName ($Visibility)"
    } catch {
      Write-Host "GitHub CLI is installed but not authenticated or repo create failed."
      Write-Host "Local repo is ready. GitHub push skipped."
    }
  } else {
    Write-Host "GitHub CLI not found. Local repo is ready. GitHub push skipped."
  }
}

Write-Host "Next: open $ProjectDir in Codex App and choose Worktree for the first implementation slice."
