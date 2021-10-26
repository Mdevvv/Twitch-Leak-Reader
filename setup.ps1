function Find-Folders {
    [Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") | Out-Null
    [System.Windows.Forms.Application]::EnableVisualStyles()
    $browse = New-Object System.Windows.Forms.FolderBrowserDialog
    $browse.SelectedPath = "C:\"
    $browse.ShowNewFolderButton = $false
    $browse.Description = "Select twitch-payouts directory"

    $loop = $true
    while($loop)
    {
        if ($browse.ShowDialog() -eq "OK")
        {
        $loop = $false
		
		#Insert your script here
		
        } else
        {
            $res = [System.Windows.Forms.MessageBox]::Show("You clicked Cancel. Would you like to try again or exit?", "Select a location", [System.Windows.Forms.MessageBoxButtons]::RetryCancel)
            if($res -eq "Cancel")
            {
                #Ends script
                return
            }
        }
    }
    $browse.SelectedPath
    $browse.Dispose()
}


# Determine script location for PowerShell
$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path
cd $ScriptDir

$FileCount = 0

$months2019 = "2019", 9, 12
$months2020 = "2020", 1, 12
$months2021 = "2021", 1, 9

$Years = $months2019, $months2020, $months2021

$Path = Find-Folders
$Path = "$Path\all_revenues"

if(Test-Path -Path $Path){
}
else {
  [System.Windows.Forms.MessageBox]::Show("Your path is not valid press enter and restart the program","setup.exe")
  exit
}

if(Test-Path -Path ".\decompressed_files") {
}
else {
  mkdir ".\decompressed_files"
}

$current = "$Path\2019\08\28\all_revenues.csv.gz"
if(Test-Path -Path $current) {
  if(Test-Path -Path ".\decompressed_files\revenues$FileCount.csv") {
    Write-Out "$current already decompress"
  } else {
    .\7-Zip\7z.exe x "$current"
    Rename-Item -Path "all_revenues.csv" -NewName "revenues$FileCount.csv"
    Move-Item -Path "revenues$FileCount.csv" -Destination ".\decompressed_files"
  }

} else {
  [System.Windows.Forms.MessageBox]::Show("$current doesn't exist","setup.exe") 
}


$FileCount = $FileCount + 1

foreach($i in $Years) {

  for ($j = $i[1]; $j -lt $i[2]+1; $j++) {
    $k = $j.ToString()
    if($k.Length -eq 1) {
      $k = "0$k"
    }
    $y = $i[0].ToString()
    $current = "$Path\$y\$k\07\all_revenues.csv.gz"

    if(Test-Path -Path $current) {
      if(Test-Path -Path ".\decompressed_files\revenues$FileCount.csv") {
        Write-Out "$current already decompress"
        
      } else {
        .\7-Zip\7z.exe x "$current"
        Rename-Item -Path "all_revenues.csv" -NewName "revenues$FileCount.csv"
        Move-Item -Path "revenues$FileCount.csv" -Destination ".\decompressed_files"
      }

    } else {
      [System.Windows.Forms.MessageBox]::Show("$current doesn't exist","setup.exe")
    }


    $FileCount = $FileCount + 1

    $Perc = ($FileCount/26)*100
    Write-Progress -Activity "recovery of nessecary files" -PercentComplete $Perc

  }

}

$current = "$Path\2021\10\05\all_revenues.csv.gz"

if(Test-Path -Path $current) {
  if(Test-Path -Path ".\decompressed_files\revenues$FileCount.csv") {
    Write-Out "$current already decompress"
  } else {
    .\7-Zip\7z.exe x "$current"
    Rename-Item -Path "all_revenues.csv" -NewName "revenues$FileCount.csv"
    Move-Item -Path "revenues$FileCount.csv" -Destination ".\decompressed_files"
  }
} else {
  [System.Windows.Forms.MessageBox]::Show("$current doesn't exist", "setup.exe")
}
$Perc = ($FileCount/26)*100
Write-Progress -Activity "Finish" -PercentComplete $Perc
[System.Windows.Forms.MessageBox]::Show("Finish","setup.exe")
