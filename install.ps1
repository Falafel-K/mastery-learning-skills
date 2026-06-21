# Windows PowerShell installer to link Deep Skills packages.

param (
    [string]$Dest = "$Home\.agents\skills",
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: .\install.ps1 [-Dest <TargetDirectory>]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Dest <dir>    Set the target destination directory (default: $Home\.agents\skills)"
    Write-Host "  -Help          Show this help message"
    exit
}

$SrcDir = $PSScriptRoot

Write-Host "----------------------------------------"
Write-Host "Deep Skills Windows Installer"
Write-Host "----------------------------------------"
Write-Host "Source directory: $SrcDir"
Write-Host "Target directory: $Dest"
Write-Host ""

# Ensure target directory exists
if (-not (Test-Path -Path $Dest)) {
    Write-Host "Creating directory: $Dest"
    New-Item -ItemType Directory -Path $Dest -Force | Out-Null
}

$Skills = @("deep-skills", "skill-scaffolder")

foreach ($Skill in $Skills) {
    $SkillSrc = Join-Path $SrcDir "skills\$Skill"
    $SkillDest = Join-Path $Dest $Skill

    if (Test-Path -Path $SkillSrc) {
        Write-Host "Linking: $Skill -> $SkillDest"
        
        # Remove existing symlink or folder at destination
        if (Test-Path -Path $SkillDest) {
            # Check if it is a directory symlink or folder
            $Item = Get-Item $SkillDest
            if ($Item.Attributes -match "ReparsePoint") {
                [System.IO.Directory]::Delete($SkillDest)
            } else {
                Remove-Item -Path $SkillDest -Recururse -Force
            }
        }
        
        # Create symbolic link
        New-Item -ItemType SymbolicLink -Path $SkillDest -Target $SkillSrc -Force | Out-Null
    } else {
        Write-Warning "Source skill package not found at $SkillSrc"
    }
}

Write-Host ""
Write-Host "Successfully linked Deep Skills!"
Write-Host "You can now use these skills in your Agent workspace."
Write-Host "----------------------------------------"
