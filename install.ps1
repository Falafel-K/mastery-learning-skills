# Windows PowerShell installer to link or download Mastery Learning Skills packages.

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

# Determine if running in online piped mode or local mode
$LocalMode = $true
if ([string]::IsNullOrEmpty($PSScriptRoot) -or -not (Test-Path -Path (Join-Path $PSScriptRoot "skills"))) {
    $LocalMode = $false
}

Write-Host "----------------------------------------"
Write-Host "Mastery Learning Skills Windows Installer"
Write-Host "----------------------------------------"
Write-Host "Target directory: $Dest"

$Skills = @("mastery-learning-obsidian", "skill-scaffolder")

# Ensure target directory exists
if (-not (Test-Path -Path $Dest)) {
    Write-Host "Creating directory: $Dest"
    New-Item -ItemType Directory -Path $Dest -Force | Out-Null
}

if ($LocalMode) {
    $SrcDir = $PSScriptRoot
    Write-Host "Mode: Local (Developer Symlink)"
    Write-Host "Source directory: $SrcDir"
    Write-Host ""

    foreach ($Skill in $Skills) {
        $SkillSrc = Join-Path $SrcDir "skills\$Skill"
        $SkillDest = Join-Path $Dest $Skill

        if (Test-Path -Path $SkillSrc) {
            Write-Host "Linking: $Skill -> $SkillDest"
            
            # Remove existing symlink or folder at destination
            if (Test-Path -Path $SkillDest) {
                $Item = Get-Item $SkillDest
                if ($Item.Attributes -match "ReparsePoint") {
                    [System.IO.Directory]::Delete($SkillDest)
                } else {
                    Remove-Item -Path $SkillDest -Recurse -Force
                }
            }
            
            # Create symbolic link
            New-Item -ItemType SymbolicLink -Path $SkillDest -Target $SkillSrc -Force | Out-Null
        } else {
            Write-Warning "Source skill package not found at $SkillSrc"
        }
    }
} else {
    Write-Host "Mode: Online (Auto-download & Copy)"
    Write-Host ""
    
    # Create secure temp path
    $TempFolder = Join-Path $env:TEMP ([Guid]::NewGuid().ToString())
    New-Item -ItemType Directory -Path $TempFolder -Force | Out-Null
    $ZipPath = Join-Path $TempFolder "archive.zip"
    $ZipUrl = "https://github.com/Falafel-K/mastery-learning-skills/archive/refs/heads/main.zip"
    
    Write-Host "Downloading latest packages from GitHub..."
    try {
        # Using .NET class for maximum compatibility across PowerShell versions
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
        $WebClient = New-Object System.Net.WebClient
        $WebClient.DownloadFile($ZipUrl, $ZipPath)
    } catch {
        Write-Error "Failed to download packages: $_"
        Remove-Item -Path $TempFolder -Recurse -Force -ErrorAction SilentlyContinue
        exit 1
    }
    
    Write-Host "Extracting packages..."
    try {
        Expand-Archive -Path $ZipPath -DestinationPath $TempFolder -Force
    } catch {
        Write-Error "Failed to extract archive. Please ensure Expand-Archive is available."
        Remove-Item -Path $TempFolder -Recurse -Force -ErrorAction SilentlyContinue
        exit 1
    }
    
    $ExtractedFolder = Join-Path $TempFolder "mastery-learning-skills-main"
    foreach ($Skill in $Skills) {
        $SkillSrc = Join-Path $ExtractedFolder "skills\$Skill"
        $SkillDest = Join-Path $Dest $Skill
        
        if (Test-Path -Path $SkillSrc) {
            Write-Host "Copying: $Skill -> $SkillDest"
            if (Test-Path -Path $SkillDest) {
                # Check for link vs folder to delete safely
                $Item = Get-Item $SkillDest
                if ($Item.Attributes -match "ReparsePoint") {
                    [System.IO.Directory]::Delete($SkillDest)
                } else {
                    Remove-Item -Path $SkillDest -Recurse -Force
                }
            }
            Copy-Item -Path $SkillSrc -Destination $SkillDest -Recurse -Force
        } else {
            Write-Warning "Package $Skill not found in downloaded archive."
        }
    }
    
    # Clean up temp folder
    Remove-Item -Path $TempFolder -Recurse -Force
}

Write-Host ""
Write-Host "Successfully installed Mastery Learning Skills!"
Write-Host "You can now use these skills in your Agent workspace."
Write-Host "----------------------------------------"
