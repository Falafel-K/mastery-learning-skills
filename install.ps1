# Windows PowerShell installer to link or download Mastery Learning Skills packages.

param (
    [string]$Dest,
    [switch]$Uninstall,
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: .\install.ps1 [-Dest <TargetDirectory>] [-Uninstall]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Dest <dir>    Set the target destination directory (default: auto-detected)"
    Write-Host "  -Uninstall     Uninstall/remove Mastery Learning Skills from target/detected directories"
    Write-Host "  -Help          Show this help message"
    return
}

$Skills = @("mastery-learning-obsidian", "skill-scaffolder", "study", "review", "dashboard", "sync", "audit", "handoff", "help")

# Auto-detect target paths if -Dest is not specified
$TargetPaths = @()
if ([string]::IsNullOrEmpty($Dest)) {
    $FoundAny = $false
    
    # 1. Gemini / Antigravity (Google Agents)
    $GeminiDir = Join-Path $Home ".gemini\config"
    if (Test-Path -Path $GeminiDir) {
        $TargetPaths += Join-Path $GeminiDir "skills"
        $FoundAny = $true
    }
    
    # 2. Claude Code
    $ClaudeDir = Join-Path $Home ".claude"
    if (Test-Path -Path $ClaudeDir) {
        $TargetPaths += Join-Path $ClaudeDir "skills"
        $FoundAny = $true
    }
    
    # 3. Legacy / Codex / General agents (include old path for cleanup/compatibility)
    $AgentsDir = Join-Path $Home ".agents"
    if (Test-Path -Path $AgentsDir) {
        $TargetPaths += Join-Path $AgentsDir "skills"
        $FoundAny = $true
    }
    
    # Fallback if none exist
    if (-not $FoundAny) {
        $TargetPaths += Join-Path $Home ".gemini\config\skills"
        $TargetPaths += Join-Path $Home ".agents\skills"
    }
} else {
    $TargetPaths += $Dest
}

# Determine if running in online piped mode or local mode
$LocalMode = $true
if ([string]::IsNullOrEmpty($PSScriptRoot) -or -not (Test-Path -Path (Join-Path $PSScriptRoot "skills"))) {
    $LocalMode = $false
}

if ($Uninstall) {
    Write-Host "----------------------------------------"
    Write-Host "Mastery Learning Skills Windows Uninstaller"
    Write-Host "----------------------------------------"
    
    foreach ($Target in $TargetPaths) {
        Write-Host "Checking target directory: $Target"
        if (Test-Path -Path $Target) {
            foreach ($Skill in $Skills) {
                $SkillDest = Join-Path $Target $Skill
                if (Test-Path -Path $SkillDest) {
                    Write-Host "Removing: $SkillDest"
                    $Item = Get-Item $SkillDest
                    if ($Item.Attributes -match "ReparsePoint") {
                        [System.IO.Directory]::Delete($SkillDest)
                    } else {
                        Remove-Item -Path $SkillDest -Recurse -Force
                    }
                }
            }
            # Clean up empty parent directory if it contains no other files/folders
            $Remaining = Get-ChildItem -Path $Target -ErrorAction SilentlyContinue
            if ($null -eq $Remaining -or @($Remaining).Count -eq 0) {
                Write-Host "Removing empty parent directory: $Target"
                Remove-Item -Path $Target -Force
            }
        }
    }
    
    Write-Host ""
    Write-Host "Successfully uninstalled Mastery Learning Skills!"
    Write-Host "All configured links and folders have been cleared."
    Write-Host "----------------------------------------"
    return
}

Write-Host "----------------------------------------"
Write-Host "Mastery Learning Skills Windows Installer"
Write-Host "----------------------------------------"
Write-Host "Target directories: $($TargetPaths -join ', ')"
Write-Host ""

if ($LocalMode) {
    $SrcDir = $PSScriptRoot
    Write-Host "Mode: Local (Developer Symlink)"
    Write-Host "Source directory: $SrcDir"
    Write-Host ""

    foreach ($Target in $TargetPaths) {
        # Ensure target directory exists
        if (-not (Test-Path -Path $Target)) {
            Write-Host "Creating directory: $Target"
            New-Item -ItemType Directory -Path $Target -Force | Out-Null
        }

        foreach ($Skill in $Skills) {
            $SkillSrc = Join-Path $SrcDir "skills\$Skill"
            $SkillDest = Join-Path $Target $Skill

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
                
                # Create junction (no admin elevation required on Windows)
                New-Item -ItemType Junction -Path $SkillDest -Target $SkillSrc -Force | Out-Null
            } else {
                Write-Warning "Source skill package not found at $SkillSrc"
            }
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
        return
    }
    
    Write-Host "Extracting packages..."
    try {
        Expand-Archive -Path $ZipPath -DestinationPath $TempFolder -Force
    } catch {
        Write-Error "Failed to extract archive. Please ensure Expand-Archive is available."
        Remove-Item -Path $TempFolder -Recurse -Force -ErrorAction SilentlyContinue
        return
    }
    
    $ExtractedFolder = Join-Path $TempFolder "mastery-learning-skills-main"
    
    foreach ($Target in $TargetPaths) {
        # Ensure target directory exists
        if (-not (Test-Path -Path $Target)) {
            Write-Host "Creating directory: $Target"
            New-Item -ItemType Directory -Path $Target -Force | Out-Null
        }

        foreach ($Skill in $Skills) {
            $SkillSrc = Join-Path $ExtractedFolder "skills\$Skill"
            $SkillDest = Join-Path $Target $Skill
            
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
    }
    
    # Clean up temp folder
    Remove-Item -Path $TempFolder -Recurse -Force
}

Write-Host ""
Write-Host "Successfully installed Mastery Learning Skills!"
Write-Host "Four Pillars Architecture active:"
Write-Host "  - Vocabulary aligned via CONTEXT.md in project root."
Write-Host "  - User/Model invocation triggers mapped (see docs/invocation.md)."
Write-Host "  - Soft degradation storage rules defined (see docs/adr/0001-mastery-storage-soft-degradation.md)."
Write-Host "You can now use these skills in your Agent workspace."
Write-Host "----------------------------------------"
