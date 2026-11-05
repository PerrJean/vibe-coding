<#
.SYNOPSIS
  Installe les règles, skills et hooks communs dans $env:USERPROFILE\.claude.
.DESCRIPTION
  Copie global\CLAUDE.md, global\skills\ et global\hooks\ vers le dossier de l'agent.
  Tout fichier ou dossier remplacé est d'abord sauvegardé dans .claude\sauvegardes\.
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

# Skills : un dossier par skill, remplacé en bloc
$skills = Join-Path $source 'skills'
if (Test-Path -LiteralPath $skills) {
  foreach ($skill in Get-ChildItem -LiteralPath $skills -Directory) {
    $cible = Join-Path $Destination "skills\$($skill.Name)"
    Sauvegarder $cible
    Agir "Skill installée : $($skill.Name)" {
      if (Test-Path -LiteralPath $cible) { Remove-Item -LiteralPath $cible -Recurse -Force }
      New-Item -ItemType Directory -Force -Path (Split-Path $cible) | Out-Null
      Copy-Item -LiteralPath $skill.FullName -Destination $cible -Recurse -Force
    }
  }
}

# Hooks : fichier par fichier
$hooks = Join-Path $source 'hooks'
if (Test-Path -LiteralPath $hooks) {
  foreach ($hook in Get-ChildItem -LiteralPath $hooks -File) {
    $cible = Join-Path $Destination "hooks\$($hook.Name)"
    Sauvegarder $cible
    Agir "Hook installé : $($hook.Name)" {
      New-Item -ItemType Directory -Force -Path (Split-Path $cible) | Out-Null
      Copy-Item -LiteralPath $hook.FullName -Destination $cible -Force
    }
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
