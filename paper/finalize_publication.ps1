[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$paperDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repositoryDir = Split-Path -Parent $paperDir
$auditPath = Join-Path $repositoryDir "artifacts\certificate\verification.json"
$manifestPath = Join-Path $repositoryDir "artifacts\certificate\manifest.json"
$resultsPath = Join-Path $paperDir "certificate-results.tex"
$buildCommand = Join-Path $paperDir "build.cmd"
$pdfPath = Join-Path $repositoryDir "output\pdf\berry_esseen_045_publication.pdf"
$archiveDir = Join-Path $repositoryDir "output\arxiv"
$archivePath = Join-Path $archiveDir "berry_esseen_045_arxiv.zip"

function Require-Equal {
    param(
        [Parameter(Mandatory = $true)]$Actual,
        [Parameter(Mandatory = $true)]$Expected,
        [Parameter(Mandatory = $true)][string]$Label
    )
    if ($Actual -ne $Expected) {
        throw "$Label is '$Actual'; expected '$Expected'."
    }
}

function Require-Sha256 {
    param(
        [Parameter(Mandatory = $true)]$Value,
        [Parameter(Mandatory = $true)][string]$Label
    )
    if (($Value -isnot [string]) -or ($Value -cnotmatch '^[0-9a-f]{64}$')) {
        throw "$Label is not a lowercase SHA-256 digest."
    }
}

function File-Sha256 {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Format-TexDigest {
    param([Parameter(Mandatory = $true)][string]$Value)
    Require-Sha256 $Value "digest"
    return $Value.Substring(0, 32) + "\allowbreak{}" + $Value.Substring(32, 32)
}

function Require-Property {
    param(
        [Parameter(Mandatory = $true)]$Object,
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Context
    )
    if ($null -eq $Object -or $Object.PSObject.Properties.Name -notcontains $Name) {
        throw "$Context is missing field '$Name'."
    }
    return $Object.$Name
}

function Convert-ToTexText {
    param([Parameter(Mandatory = $true)][string]$Value)
    $escaped = $Value.Replace('\', '\textbackslash{}')
    $escaped = $escaped.Replace('{', '\{').Replace('}', '\}')
    $escaped = $escaped.Replace('$', '\$').Replace('&', '\&')
    $escaped = $escaped.Replace('#', '\#').Replace('_', '\_')
    $escaped = $escaped.Replace('%', '\%')
    $escaped = $escaped.Replace('~', '\textasciitilde{}')
    $escaped = $escaped.Replace('^', '\textasciicircum{}')
    return $escaped
}

if (-not (Test-Path -LiteralPath $auditPath -PathType Leaf)) {
    throw "No accepted audit exists at $auditPath. Run verify.cmd to completion first."
}
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw "The certificate manifest is missing: $manifestPath"
}

$audit = Get-Content -LiteralPath $auditPath -Raw -Encoding UTF8 | ConvertFrom-Json
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json

Require-Equal (Require-Property $audit "status" "audit") "ACCEPTED_FULL" "audit.status"
Require-Equal (Require-Property $audit "format" "audit") "berry-esseen-045-certificate-bundle-v2" "audit.format"
Require-Equal (Require-Property $audit "target" "audit") "9/20" "audit.target"
Require-Equal (Require-Property $audit "python_flint" "audit") "0.9.0" "audit.python_flint"
Require-Equal (Require-Property $audit "flint" "audit") "3.6.0" "audit.flint"

$scope = Require-Property $audit "scope" "audit"
Require-Equal (Require-Property $scope "n_start" "audit.scope") 2 "audit.scope.n_start"
Require-Equal (Require-Property $scope "n_end" "audit.scope") 8123 "audit.scope.n_end"

Require-Equal (Require-Property $manifest "format" "manifest") "berry-esseen-045-certificate-bundle-v2" "manifest.format"
Require-Equal (Require-Property $manifest "target" "manifest") "9/20" "manifest.target"
Require-Equal (Require-Property $manifest "python_flint" "manifest") "0.9.0" "manifest.python_flint"
Require-Equal (Require-Property $manifest "flint" "manifest") "3.6.0" "manifest.flint"

$manifestDigest = File-Sha256 $manifestPath
Require-Sha256 (Require-Property $audit "manifest_sha256" "audit") "audit.manifest_sha256"
Require-Equal $audit.manifest_sha256 $manifestDigest "audit.manifest_sha256"

$certificateSetDigest = Require-Property $audit "certificate_set_sha256" "audit"
Require-Sha256 $certificateSetDigest "audit.certificate_set_sha256"
Require-Equal $certificateSetDigest (Require-Property $manifest "certificate_set_sha256" "manifest") "certificate-set digest"

$sourcePaths = [ordered]@{
    checker_sha256 = "proof\check_certificate.py"
    core_sha256 = "proof\berry_core.py"
    proof_package_sha256 = "proof\__init__.py"
    constructor_sha256 = "construction\generate_certificate.py"
    parameter_bank_loader_sha256 = "construction\parameter_bank.py"
    construction_package_sha256 = "construction\__init__.py"
    verification_launcher_sha256 = "construction\verify.py"
}
foreach ($entry in $sourcePaths.GetEnumerator()) {
    $field = $entry.Key
    $sourcePath = Join-Path $repositoryDir $entry.Value
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        throw "Source bound by the audit is missing: $($entry.Value)"
    }
    $actualDigest = File-Sha256 $sourcePath
    $auditDigest = Require-Property $audit $field "audit"
    $manifestSourceDigest = Require-Property $manifest $field "manifest"
    Require-Sha256 $auditDigest "audit.$field"
    Require-Equal $auditDigest $manifestSourceDigest "$field in audit and manifest"
    Require-Equal $auditDigest $actualDigest "$field in audit and repository"
}

$summaries = @(Require-Property $audit "n_summaries" "audit")
Require-Equal $summaries.Count 8122 "audit.n_summaries count"
[long]$summedCells = 0
for ($index = 0; $index -lt $summaries.Count; $index++) {
    $summary = $summaries[$index]
    $expectedN = $index + 2
    Require-Equal (Require-Property $summary "n" "audit.n_summaries[$index]") $expectedN "audit.n_summaries[$index].n"
    $cells = Require-Property $summary "cells" "audit.n_summaries[$index]"
    if (($cells -isnot [int]) -and ($cells -isnot [long])) {
        throw "audit.n_summaries[$index].cells is not an integer."
    }
    if ($cells -lt 1 -or $cells -gt 4096) {
        throw "audit.n_summaries[$index].cells is outside 1,...,4096."
    }
    $summedCells += [long]$cells
}
$totalCells = Require-Property $audit "total_cells" "audit"
Require-Equal ([long]$totalCells) $summedCells "audit.total_cells"

$worstLocation = Require-Property $audit "worst_location" "audit"
$worstN = [int](Require-Property $worstLocation "n" "audit.worst_location")
$worstCell = [int](Require-Property $worstLocation "cell" "audit.worst_location")
$worstRho = @(Require-Property $worstLocation "rho" "audit.worst_location")
if ($worstN -lt 2 -or $worstN -gt 8123 -or $worstCell -lt 0 -or $worstRho.Count -ne 2) {
    throw "audit.worst_location has an invalid shape."
}
foreach ($endpoint in $worstRho) {
    if (($endpoint -isnot [string]) -or ($endpoint -notmatch '^-?[0-9]+(?:/[1-9][0-9]*)?$')) {
        throw "audit.worst_location.rho contains a noncanonical rational."
    }
}

$worstUpper = [string](Require-Property $audit "worst_upper" "audit")
$worstUpperExact = [string](Require-Property $audit "worst_upper_exact" "audit")
if ($worstUpper -notmatch '^[0-9]+(?:\.[0-9]+)?$') {
    throw "audit.worst_upper is not a directed decimal."
}
if ($worstUpperExact -notmatch '^-?[0-9]+(?:/[1-9][0-9]*)?$') {
    throw "audit.worst_upper_exact is not a canonical rational."
}

$completedAt = [string](Require-Property $audit "completed_at_utc" "audit")
if ($completedAt -notmatch '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$') {
    throw "audit.completed_at_utc is not an ISO-8601 UTC timestamp."
}
$elapsed = [double](Require-Property $audit "elapsed_seconds" "audit")
if ([double]::IsNaN($elapsed) -or [double]::IsInfinity($elapsed) -or $elapsed -le 0) {
    throw "audit.elapsed_seconds must be finite and positive."
}
$elapsedText = [string]::Format(
    [Globalization.CultureInfo]::InvariantCulture,
    "{0:F3}",
    $elapsed
)

$runtimeText = Convert-ToTexText ([string](Require-Property $audit "platform" "audit"))
$worstLocationText = "\(n=$worstN\), cell \($worstCell\), on \(\rho\in[$($worstRho[0]),$($worstRho[1])]\)"
$manifestDigestTex = Format-TexDigest $manifestDigest

$resultLines = @(
    "% Generated by paper/finalize_publication.ps1 from the accepted bundle-v2 audit.",
    "% Do not edit this file by hand.",
    "\newif\ifcertificateaccepted",
    "\certificateacceptedtrue",
    "",
    "\newcommand{\CertifiedConstant}{\(\frac{9}{20}=0.45\)}",
    "\newcommand{\CertificateBundleFormat}{berry-esseen-045-certificate-bundle-v2}",
    "\newcommand{\CertificateScopeStart}{2}",
    "\newcommand{\CertificateScopeEnd}{8123}",
    "\newcommand{\CertificateTarget}{9/20}",
    "\newcommand{\CertificatePythonFlint}{0.9.0}",
    "\newcommand{\CertificateFlint}{3.6.0}",
    "\newcommand{\CertificateDate}{$completedAt}",
    "\newcommand{\CertificateTotalCells}{$totalCells}",
    "\newcommand{\CertificateWorstUpper}{$worstUpper}",
    "\newcommand{\CertificateWorstUpperExact}{$worstUpperExact}",
    "\newcommand{\CertificateWorstLocation}{$worstLocationText}",
    "\newcommand{\CertificateElapsedSeconds}{$elapsedText}",
    "\newcommand{\CertificateSetDigest}{$certificateSetDigest}",
    "\newcommand{\CertificateManifestDigest}{$manifestDigestTex}",
    "\newcommand{\CertificateCheckerDigest}{$($audit.checker_sha256)}",
    "\newcommand{\CertificateCoreDigest}{$($audit.core_sha256)}",
    "\newcommand{\CertificateRuntime}{\code{$runtimeText}}",
    ""
)
$resultText = $resultLines -join "`n"

$originalResults = [IO.File]::ReadAllBytes($resultsPath)
$originalPdf = if (Test-Path -LiteralPath $pdfPath -PathType Leaf) {
    [IO.File]::ReadAllBytes($pdfPath)
} else {
    $null
}
$temporaryResults = "$resultsPath.tmp"
$utf8WithoutBom = New-Object Text.UTF8Encoding($false)
[IO.File]::WriteAllText($temporaryResults, $resultText, $utf8WithoutBom)
Move-Item -LiteralPath $temporaryResults -Destination $resultsPath -Force

try {
    Push-Location $paperDir
    try {
        & cmd.exe /d /c "build.cmd"
        $buildExitCode = $LASTEXITCODE
    } finally {
        Pop-Location
    }
    if ($buildExitCode -ne 0) {
        throw "The LaTeX build failed with exit code $buildExitCode."
    }
} catch {
    [IO.File]::WriteAllBytes($resultsPath, $originalResults)
    if ($null -ne $originalPdf) {
        [IO.File]::WriteAllBytes($pdfPath, $originalPdf)
    } elseif (Test-Path -LiteralPath $pdfPath -PathType Leaf) {
        Remove-Item -LiteralPath $pdfPath -Force
    }
    throw
}

if (-not (Test-Path -LiteralPath $pdfPath -PathType Leaf)) {
    throw "The manuscript build did not create $pdfPath."
}

New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
Push-Location $paperDir
try {
    Compress-Archive `
        -LiteralPath "berry_esseen_045.tex", "certificate-results.tex" `
        -DestinationPath $archivePath `
        -CompressionLevel Optimal `
        -Force
} finally {
    Pop-Location
}

Write-Host "PUBLICATION READY: $pdfPath"
Write-Host "ARXIV SOURCE READY: $archivePath"
