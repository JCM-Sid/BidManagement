## List Reference Directories and files

echo "=============================="
echo "=== Liste ref EBP ============"
Get-ChildItem -Path "C:\Users\jch_m\ATAE" -Recurse -File -ErrorAction SilentlyContinue |
Where-Object { $_.FullName -match "\.pdf$" -and (
    $_.FullName -match "COMMANDE EBP " -or
    $_.FullName -match "CDE EBP " -or
    $_.FullName -match "Commande EBP "
) } |
Select-Object -ExpandProperty DirectoryName |
Sort-Object -Unique


echo "=============================="
echo "=== Liste fichiers CONSULT ==="
Get-ChildItem -Path "C:\Users\jch_m\ATAE" -Recurse -File -ErrorAction SilentlyContinue |
Where-Object { $_.FullName -match "\.pdf$" -and (
    $_.FullName -match "CCTP" -or
    $_.FullName -match "CCAP" -or
    $_.FullName -match "AAPC" -or
    $_.FullName -match "RC" -or
    $_.FullName -match "memoire technique" -or
    $_.FullName -match "Commande "
) } |
ForEach-Object { "$($_.DirectoryName)\$($_.Name)" }


echo "=============================="
echo "=== Liste fichiers REJET ====="
Get-ChildItem -Path "C:\Users\jch_m\ATAE" -Recurse -File -ErrorAction SilentlyContinue |
Where-Object { $_.FullName -match "\.pdf$" -and  $_.FullName -match "ECHEC 20" -and (
    $_.FullName -match "notification" -or $_.FullName -match "Notification" -or
    $_.FullName -match "refus" -or $_.FullName -match "REFUS" -or
    $_.FullName -match "Regret" -or $_.FullName -match "regret" -or
    $_.FullName -match "Analyse" -or $_.FullName -match "analyse" 
) } |
ForEach-Object { "$($_.DirectoryName)\$($_.Name)" }

