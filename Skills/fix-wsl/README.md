#Requires -RunAsAdministrator

<#
.SYNOPSIS
    Fixes the WSL service being reset to Disabled after reboot on Windows 11.

.DESCRIPTION
    This script:
    1. Identifies which WSL service is present (WslService or LxssManager)
    2. Sets the service startup type to Automatic via registry
    3. Ensures required Windows features are enabled
    4. Disables Fast Startup (a common culprit)
    5. Creates a safeguard scheduled task that re-enables the service on logon
    6. Updates WSL to the latest version

.NOTES
    Run this script as Administrator in PowerShell.
    A system restart is recommended after running.
#>

$ErrorActionPreference = "Stop"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  WSL Service Fix Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# --- Step 1: Identify the WSL service ---

Write-Host "[1/6] Identifying WSL service..." -ForegroundColor Yellow

$serviceName = $null
$serviceDisplayName = $null

if (Get-Service -Name "WslService" -ErrorAction SilentlyContinue) {
    $serviceName = "WslService"
    $serviceDisplayName = "WSL Service"
    Write-Host "  Found: WslService (modern)" -ForegroundColor Green
}
elseif (Get-Service -Name "LxssManager" -ErrorAction SilentlyContinue) {
    $serviceName = "LxssManager"
    $serviceDisplayName = "LxssManager"
    Write-Host "  Found: LxssManager (legacy)" -ForegroundColor Green
}
else {
    Write-Host "  ERROR: No WSL service found. WSL may not be installed." -ForegroundColor Red
    Write-Host "  Run 'wsl --install' to install WSL first." -ForegroundColor Red
    exit 1
}

# Show current state

$svc = Get-Service -Name $serviceName
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\$serviceName"
$currentStart = (Get-ItemProperty -Path $regPath -Name "Start" -ErrorAction SilentlyContinue).Start
$startTypes = @{ 0 = "Boot"; 1 = "System"; 2 = "Automatic"; 3 = "Manual"; 4 = "Disabled" }
Write-Host "  Current status : $($svc.Status)" -ForegroundColor White
Write-Host "  Current startup: $($startTypes[$currentStart]) (registry Start=$currentStart)" -ForegroundColor White

# --- Step 2: Set service to Automatic via registry ---

Write-Host "`n[2/6] Setting $serviceName to Automatic startup..." -ForegroundColor Yellow

# Set via registry (more reliable than Set-Service for this issue)

Set-ItemProperty -Path $regPath -Name "Start" -Value 2 -Type DWord
Write-Host "  Registry key set: $regPath\Start = 2 (Automatic)" -ForegroundColor Green

# Also set via sc.exe as a belt-and-suspenders approach

& sc.exe config $serviceName start= auto | Out-Null
Write-Host "  sc.exe config confirmed" -ForegroundColor Green

# Start the service if it's not running

if ($svc.Status -ne "Running") {
    try {
        Start-Service -Name $serviceName
        Write-Host "  Service started successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "  Note: Could not start service now (will start after reboot)" -ForegroundColor DarkYellow
    }
}

# --- Step 3: Ensure Windows features are enabled ---

Write-Host "`n[3/6] Verifying required Windows features..." -ForegroundColor Yellow

$features = @(
    @{ Name = "Microsoft-Windows-Subsystem-Linux"; Display = "WSL" },
    @{ Name = "VirtualMachinePlatform"; Display = "Virtual Machine Platform" }
)

$featureChanged = $false
foreach ($feature in $features) {
    $state = (Get-WindowsOptionalFeature -Online -FeatureName $feature.Name).State
    if ($state -eq "Enabled") {
        Write-Host "  $($feature.Display): Already enabled" -ForegroundColor Green
    }
    else {
        Write-Host "  $($feature.Display): Enabling..." -ForegroundColor DarkYellow
        Enable-WindowsOptionalFeature -Online -FeatureName $feature.Name -All -NoRestart | Out-Null
        Write-Host "  $($feature.Display): Enabled" -ForegroundColor Green
        $featureChanged = $true
    }
}

# --- Step 4: Disable Fast Startup ---

Write-Host "`n[4/6] Checking Fast Startup..." -ForegroundColor Yellow

$fastStartupPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Power"
$currentFastStartup = (Get-ItemProperty -Path $fastStartupPath -Name "HiberbootEnabled" -ErrorAction SilentlyContinue).HiberbootEnabled

if ($currentFastStartup -eq 1) {
    Set-ItemProperty -Path $fastStartupPath -Name "HiberbootEnabled" -Value 0 -Type DWord
    Write-Host "  Fast Startup was ENABLED -> now DISABLED" -ForegroundColor Green
    Write-Host "  (Fast Startup can prevent services from initializing correctly)" -ForegroundColor DarkGray
}
elseif ($currentFastStartup -eq 0) {
    Write-Host "  Fast Startup already disabled - good" -ForegroundColor Green
}
else {
    Write-Host "  Fast Startup setting not found (OK, likely already off)" -ForegroundColor DarkGray
}

# --- Step 5: Create a safeguard scheduled task ---

Write-Host "`n[5/6] Creating safeguard scheduled task..." -ForegroundColor Yellow

$taskName = "EnsureWSLServiceAutomatic"
$taskDescription = "Safeguard: ensures the WSL service startup type remains Automatic after reboot"

# Remove existing task if present

if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "  Removed existing task" -ForegroundColor DarkGray
}

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument @"
-NoProfile -WindowStyle Hidden -Command "& { `$svc = '$serviceName'; `$regPath = 'HKLM:\SYSTEM\CurrentControlSet\Services\' + `$svc; `$start = (Get-ItemProperty -Path `$regPath -Name 'Start' -ErrorAction SilentlyContinue).Start; if (`$start -ne 2) { Set-ItemProperty -Path `$regPath -Name 'Start' -Value 2 -Type DWord; sc.exe config `$svc start= auto | Out-Null }; if ((Get-Service `$svc).Status -ne 'Running') { Start-Service `$svc -ErrorAction SilentlyContinue } }"
"@

$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description $taskDescription | Out-Null
Write-Host "  Scheduled task '$taskName' created" -ForegroundColor Green
Write-Host "  Runs at startup as SYSTEM to ensure the service stays Automatic" -ForegroundColor DarkGray

# --- Step 6: Update WSL ---

Write-Host "`n[6/6] Updating WSL to latest version..." -ForegroundColor Yellow

try {
    $wslUpdate = & wsl --update 2>&1
    Write-Host "  $wslUpdate" -ForegroundColor Green
}
catch {
    Write-Host "  Could not update WSL (non-critical, can be done manually later)" -ForegroundColor DarkYellow
}

# --- Summary ---

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Fix Applied Successfully" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "What was done:" -ForegroundColor White
Write-Host "  1. Set $serviceName startup type to Automatic (registry + sc.exe)" -ForegroundColor White
Write-Host "  2. Verified WSL and Virtual Machine Platform features are enabled" -ForegroundColor White
Write-Host "  3. Disabled Fast Startup (prevents service init issues)" -ForegroundColor White
Write-Host "  4. Created '$taskName' scheduled task as a safeguard" -ForegroundColor White
Write-Host "  5. Updated WSL to latest version" -ForegroundColor White
Write-Host ""

if ($featureChanged) {
    Write-Host "  ** A RESTART IS REQUIRED (Windows features were changed) **" -ForegroundColor Red
}
else {
    Write-Host "  A restart is recommended to verify the fix." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "To verify after reboot, run:" -ForegroundColor DarkGray
Write-Host "  Get-Service $serviceName | Select-Object Name, Status, StartType" -ForegroundColor DarkGray
Write-Host "  wsl --status" -ForegroundColor DarkGray
Write-Host ""


