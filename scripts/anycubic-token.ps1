$logDir = Join-Path $env:AppData 'AnycubicSlicerNext\log'
$hit = Get-ChildItem $logDir -Filter 'debug_*.log' | Select-String -Pattern 'accessToken\s*=\s*([^,\s]+)' | ForEach-Object { $ts = [datetime]::MinValue; if ($_.Line -match '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})') { $ts = [datetime]::ParseExact($Matches[1],'yyyy-MM-dd HH:mm:ss',$null) }; [pscustomobject]@{ Time=$ts; Token=$_.Matches[0].Groups[1].Value; File=$_.Filename } } | Sort-Object Time | Select-Object -Last 1
if (-not $hit) { throw 'Kein accessToken gefunden - im Slicer einmal ab- und wieder anmelden.' }
$hit.Token | Set-Clipboard
"OK - $($hit.File) ($($hit.Time)), $($hit.Token.Length) Zeichen kopiert."