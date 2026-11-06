<#
.SYNOPSIS
  Installe les règles, skills et hooks communs dans $env:USERPROFILE\.claude.
.DESCRIPTION
  Relie le dossier de l'agent à ce dépôt, pour qu'un git pull suffise à mettre à jour :
  une jonction par skill (.claude\skills\<skill> -> global\skills\<skill>), et une jonction
  pour le dossier des hooks (.claude\hooks -> global\hooks). Une jonction ne demande pas de
  droits d'administrateur, contrairement à un lien symbolique ; un lien physique, lui, garde
  l'ancienne version dès que git réécrit le fichier. Déplacer le dépôt casse les jonctions :
  relancer alors l'installateur.
  global\CLAUDE.md est copié, pas relié : sa section Environnement est propre au poste.
  Tout fichier ou dossier remplacé est d'abord sauvegardé dans .claude\sauvegardes\.
  Le dossier .claude\hooks n'est remplacé que s'il ne contient que des hooks de global\hooks.
  Un CLAUDE.md existant n'est jamais écrasé sans -Remplacer : le modèle est posé à côté,
  sous le nom CLAUDE.vibe-coding.md, pour fusion à la main (la section Environnement est personnelle).
.EXAMPLE
  .\global\installer.ps1 -Simulation
  .\global\installer.ps1
#>
param(
  [string]$Destination = (Join-Path $env:USERPROFILE '.claude'),
  [switch]$Simulation,
  [switch]$Remplacer
)
$ErrorActionPreference = 'Stop'
$source = $PSScriptRoot
$horodatage = Get-Date -Format 'yyyyMMdd-HHmmss'
$sauvegarde = Join-Path $Destination "sauvegardes\vibe-coding-$horodatage"
$n = 2
while (Test-Path -LiteralPath $sauvegarde) { $sauvegarde = Join-Path $Destination "sauvegardes\vibe-coding-$horodatage-$n"; $n++ }

function Agir([string]$message, [scriptblock]$action) {
  if ($Simulation) { Write-Host "[simulation] $message" } else { Write-Host $message; & $action }
}

function Sauvegarder([string]$cible) {
  if (-not (Test-Path -LiteralPath $cible)) { return }
  $relatif = $cible.Substring($Destination.Length).TrimStart('\', '/')
  $copie = Join-Path $sauvegarde $relatif
  Agir "Sauvegarde : $relatif" {
    New-Item -ItemType Directory -Force -Path (Split-Path $copie) | Out-Null
    Copy-Item -LiteralPath $cible -Destination $copie -Recurse -Force
  }
}

function Est-JonctionVers([string]$cible, [string]$vers) {
  $item = Get-Item -LiteralPath $cible -Force -ErrorAction SilentlyContinue
  if ($null -eq $item -or $item.LinkType -ne 'Junction') { return $false }
  $actuelle = [string]($item.Target | Select-Object -First 1)
  return $actuelle.TrimEnd('\') -ieq $vers.TrimEnd('\')
}

function Lier([string]$cible, [string]$vers, [string]$nom) {
  if (Est-JonctionVers $cible $vers) { Write-Host "Déjà relié : $nom"; return }
  Sauvegarder $cible
  Agir "Jonction : $nom -> $vers" {
    $item = Get-Item -LiteralPath $cible -Force -ErrorAction SilentlyContinue
    if ($null -ne $item) {
      # Un lien se retire seul : Remove-Item -Recurse viderait aussi le dossier qu'il vise.
      if ($item.LinkType) { [IO.Directory]::Delete($cible) } else { Remove-Item -LiteralPath $cible -Recurse -Force }
    }
    New-Item -ItemType Directory -Force -Path (Split-Path $cible) | Out-Null
    New-Item -ItemType Junction -Path $cible -Target $vers | Out-Null
  }
}

$refus = 0
if (-not $Simulation) { New-Item -ItemType Directory -Force -Path $Destination | Out-Null }

# Règles communes
$claude = Join-Path $Destination 'CLAUDE.md'
if ((Test-Path -LiteralPath $claude) -and -not $Remplacer) {
  $aCote = Join-Path $Destination 'CLAUDE.vibe-coding.md'
  Agir "CLAUDE.md existe déjà : modèle posé à côté, $aCote. Fusionner à la main." {
    Copy-Item -LiteralPath (Join-Path $source 'CLAUDE.md') -Destination $aCote -Force
  }
} else {
  Sauvegarder $claude
  Agir "CLAUDE.md installé. Remplir la section Environnement." {
    Copy-Item -LiteralPath (Join-Path $source 'CLAUDE.md') -Destination $claude -Force
  }
}

# Skills : une jonction par skill ; les autres skills du poste ne sont pas touchées
$skills = Join-Path $source 'skills'
if (Test-Path -LiteralPath $skills) {
  foreach ($skill in Get-ChildItem -LiteralPath $skills -Directory) {
    Lier (Join-Path $Destination "skills\$($skill.Name)") $skill.FullName "skills\$($skill.Name)"
  }
}

# Hooks : une jonction pour le dossier entier, s'il ne porte que des hooks de ce dépôt
$hooks = Join-Path $source 'hooks'
if (Test-Path -LiteralPath $hooks) {
  $cible = Join-Path $Destination 'hooks'
  $autres = @()
  if ((Test-Path -LiteralPath $cible) -and -not (Est-JonctionVers $cible $hooks)) {
    $connus = @(Get-ChildItem -LiteralPath $hooks -File | ForEach-Object { $_.Name })
    $autres = @(Get-ChildItem -LiteralPath $cible -Force | Where-Object { $connus -notcontains $_.Name -and $_.Name -ne '__pycache__' })
  }
  if ($autres.Count -gt 0) {
    Write-Host "REFUS : $cible contient des fichiers absents de global\hooks : $(($autres | ForEach-Object { $_.Name }) -join ', '). Les déplacer, puis relancer."
    $refus = 1
  } else {
    Lier $cible $hooks 'hooks'
  }
  # Déclaration dans settings.json, avec la commande Python de Windows : python (python3 y est souvent un raccourci vers le Store).
  $options = @((Join-Path $source 'declarer_hooks.py'), $Destination, 'python')
  if ($Simulation) { $options += '--simulation' }
  & python @options
  if ($LASTEXITCODE -ne 0) { throw "Déclaration des hooks en échec (code $LASTEXITCODE)" }
}

if (-not $Simulation -and (Test-Path -LiteralPath $sauvegarde)) {
  Write-Host "Anciennes versions sauvegardées dans $sauvegarde"
}
exit $refus
