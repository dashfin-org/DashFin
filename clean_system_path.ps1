#!/usr/bin/env powershell
<#
 clean_system_path.ps1 ── deduplicate & tidy the **System** PATH

 HOW TO USE
 ----------
 1. **Save this file** as `clean_system_path.ps1` **in the directory you will run it from** (e.g. `C:\Users\Mohamed\dashfin`).
    If you just copied the code from ChatGPT, open an elevated PowerShell window in that folder and run:
    ````powershell
    notepad clean_system_path.ps1   # paste the code, then File ➜ Save
    ````
 2. Start **PowerShell as Administrator**, `cd` to the folder containing `clean_system_path.ps1`.
 3. Execute:
    ````powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
    .\clean_system_path.ps1
    ````
 4. Sign‑out or reboot for every application to pick up the new System PATH.

 WHAT IT DOES
 ------------
 • Saves a timestamped backup to `%SystemRoot%\Temp\SystemPath_backup_<ts>.txt`.
 • Removes duplicate segments (case‑insensitive).
 • Drops the rogue Linux‑style entry `\usr\local\bin\python3`.
 • Leaves first occurrences in original order.
 • Touches **only** the Machine‑wide PATH (no user PATH changes).

 Tested on Windows 10 64‑bit, PowerShell 5 & 7.
#>

if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
    Write-Error "Run this script in an **elevated** PowerShell window."
    exit 1
}

$timestamp  = (Get-Date -Format 'yyyyMMddHHmmss')
$backupFile = "$Env:SystemRoot\Temp\SystemPath_backup_$timestamp.txt"
$sysPathRaw = [Environment]::GetEnvironmentVariable('Path', 'Machine')

# 0. Backup -------------------------------------------------------------
$sysPathRaw | Out-File -Encoding utf8 $backupFile
Write-Host "✔ Backup saved to $backupFile"

# 1. Deduplicate --------------------------------------------------------
$seen  = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$clean = [System.Collections.Generic.List[string]]::new()

foreach ($entry in $sysPathRaw -split ';') {
    $trim = $entry.Trim()
    if ($trim -and -not $seen.Contains($trim)) {
        if ($trim -eq '\usr\local\bin\python3') { continue }   # drop rogue
        $seen.Add($trim)  | Out-Null
        $clean.Add($trim) | Out-Null
    }
}

# 2. Persist ------------------------------------------------------------
$newPath = $clean -join ';'
[Environment]::SetEnvironmentVariable('Path', $newPath, 'Machine')
Write-Host "✔ System PATH deduplicated. Sign out or reboot to apply."
