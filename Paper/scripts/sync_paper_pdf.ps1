param(
    [Parameter(Mandatory = $true)][string]$RootFile,
    [Parameter(Mandatory = $true)][string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'
$documentPath = (Resolve-Path -LiteralPath $RootFile).Path
$documentName = [System.IO.Path]::GetFileNameWithoutExtension($documentPath)
$compiledPdf = Join-Path $OutputDirectory ($documentName + '.pdf')
if (-not (Test-Path -LiteralPath $compiledPdf -PathType Leaf)) {
    throw "Compiled PDF not found: $compiledPdf"
}

$documentPdf = [System.IO.Path]::ChangeExtension($documentPath, '.pdf')
Copy-Item -LiteralPath $compiledPdf -Destination $documentPdf -Force

$paperDirectory = Split-Path -Parent $PSScriptRoot
if ($documentPath -ieq (Join-Path $paperDirectory 'main.tex')) {
    $publicationDirectory = Join-Path $paperDirectory 'output/pdf'
    New-Item -ItemType Directory -Path $publicationDirectory -Force | Out-Null
    Copy-Item -LiteralPath $compiledPdf -Destination (Join-Path $publicationDirectory 'stereoqueereval-qwen35-lora-draft.pdf') -Force
}
Write-Output "Updated PDF: $documentPdf"
