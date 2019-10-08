$running=@()
$stopped=@()
$noping=@()
$ping=@()
$nopath=@()
$yespath=@()
$comp = "Running" 
$cn = get-content "D:\filepath\filename.csv" 
$64ACL = "D:\filepath\64 bit\SetACL.exe"
$32ACL = "D:\filepath\32 bit\SetACL.exe"

foreach($cu in $cn) {
    if (Test-Connection $cu -Count 1 -Quiet) {
        if(-not($GetObject)){
            $ping+=$cu
    }
        else{
            $noping +=$cu
    }
}
}
foreach($cn2 in $ping){
    if (Test-Path -Path "\\$cn2\c$\Program Files\Cylance\Desktop\"){
        if(-not($GetObject)){
               $yespath+= $cn2 }
    } 
        else{
             $nopath+=$cn2
        }
}
foreach($cn1 in $yespath){
    $out1 = (Get-Service -ServiceName Cylancesvc -ComputerName $cn1 -erroraction 'silentlycontinue').status
        if ($out1 -eq $comp){
            $running+=$cn1
        }   
        else{ 
            $stopped+=$cn1
        }
}

foreach($computer in $running){
    if((get-wmiobject win32_operatingsystem -computer $computer | select-object OSArchitecture).OSArchitecture -eq "64-bit"){
        $EXEACL = $64ACL
        & $EXEACL -on "\\$computer.domain\HKEY_LOCAL_MACHINE\SOFTWARE\Cylance\Desktop" -ot reg -actn ace -ace "n:$computer.domain\Administrators;p:full" 
        & $EXEACL -on "\\$computer.domain\HKEY_LOCAL_MACHINE\SOFTWARE\Cylance\Desktop" -ot reg -actn setowner -ownr "n:domain\username"
        reg delete  "\\$computer\HKEY_LOCAL_MACHINE\SOFTWARE\Cylance\Desktop" /v LastStateRestorePoint /f
        & $EXEACL -on "\\$computer.domain\HKEY_LOCAL_MACHINE\SOFTWARE\Cylance\Desktop" -ot reg -actn ace -ace "n:$computer.domain\Administrators;p:read"
}
    else{
        $EXEACL = $32ACL
        & $EXEACL -on "\\$computer.domain\HKEY_LOCAL_MACHINE\SOFTWARE\Cylance\Desktop" -ot reg -actn ace -ace "n:$computer.domin\Administrators;p:full" 
        & $EXEACL -on "\\$computer.domain\HKEY_LOCAL_MACHINE\SOFTWARE\Cylance\Desktop" -ot reg -actn setowner -ownr "n:domain\username"
        reg delete  "\\$computer\HKEY_LOCAL_MACHINE\SOFTWARE\Cylance\Desktop" /v LastStateRestorePoint /f
        & $EXEACL -on "\\$computer.domain\HKEY_LOCAL_MACHINE\SOFTWARE\Cylance\Desktop" -ot reg -actn ace -ace "n:$computer.domainAdministrators;p:read"
}
}