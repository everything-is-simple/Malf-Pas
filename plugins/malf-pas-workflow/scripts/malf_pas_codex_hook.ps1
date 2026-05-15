param(
    [string]$Event = "Unknown"
)

$repoRoot = "H:\Malf-Pas"
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$script = Join-Path $repoRoot "scripts\governance\check_malf_pas_workflow.py"

if (Test-Path -LiteralPath $venvPython) {
    & $venvPython $script --repo-root $repoRoot --hook-event $Event
    exit $LASTEXITCODE
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $script --repo-root $repoRoot --hook-event $Event
    exit $LASTEXITCODE
}

Write-Output "Malf-Pas workflow hook: Python not found; run governance checks manually."
exit 0
