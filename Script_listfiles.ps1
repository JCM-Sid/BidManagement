echo "=== Liste ref EBP ==="
Get-ChildItem -Path "C:\Users\ATAEM08\ATAE" -Recurse -File -ErrorAction SilentlyContinue |
Where-Object { $_.FullName -match "COMMANDE EBP "} | ForEach-Object { "$($_.DirectoryName)\$($_.Name)" }

echo "=== Liste fichiers CCTP ==="
Get-ChildItem -Path "C:\Users\ATAEM08\ATAE" -Recurse -File -ErrorAction SilentlyContinue |
Where-Object { $_.FullName -match "SPS" -and $_.FullName -match "CCTP" } | ForEach-Object { "$($_.DirectoryName)\$($_.Name)" }