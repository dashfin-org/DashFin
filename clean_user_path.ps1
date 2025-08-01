<#
 clean_user_path.ps1  — tidy the *User* PATH only

 HOW TO USE (non‑elevated PowerShell)
 ------------------------------------
 1. Save this file into your repo root or any folder:
      notepad clean_user_path.ps1   # paste → save
 2. In the same window, run:
      Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
      .\clean_user_path.ps1
 3. Open a **new** terminal to pick up the changes.

 WHAT IT DOES
 ------------
 • Backs up current user PATH to  %USERPROFILE%\UserPath_backup_<ts>.txt
 • Removes exact duplicates (case‑insensitive)
 • Drops rogue entry  \usr\local\bin\python3
 • Replaces "…\PowerShell\7\pwsh.exe" with the proper dir
   "C:\Program Files\PowerShell\7\" then dedupes.
#>

$ts        = (Get-Date -Format 'yyyyMMddHHmmss')
$backup    = "$Env:USERPROFILE\UserPath_backup_$ts.txt"
$userRaw   = [Environment]::GetEnvironmentVariable('Path','User')

# --- backup ---
$userRaw | Out-File -Encoding utf8 $backup
Write-Host "✔ Backup saved to $backup"

# --- dedupe / clean ---
$seen  = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$clean = [System.Collections.Generic.List[string]]::new()

foreach ($entry in $userRaw -split ';') {
    $trim = $entry.Trim()
    if (-not $trim) { continue }

    # fix explicit pwsh.exe path → keep dir instead
    if ($trim -like '*PowerShell\\7\\pwsh.exe') {
        $trim = 'C:\Program Files\PowerShell\7\'
    }

    if ($trim -eq '\usr\local\bin\python3') { continue }  # drop rogue entry
    if ($seen.Add($trim)) { $clean.Add($trim) | Out-Null }
}

$newPath = $clean -join ';'
[Environment]::SetEnvironmentVariable('Path',$newPath,'User')
Write-Host "✔ User PATH deduplicated.  Open a new terminal to verify."
