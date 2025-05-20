#Setup variables

param (
    [string]$engine,
    [string]$project,
    [string]$script
)


$args = "`"$project`" -run=pythonscript -script=`"$script`" -unattended -log"

Start-Process -FilePath $engine -ArgumentList $args -NoNewWindow -Wait