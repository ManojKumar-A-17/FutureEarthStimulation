# Start backend server and keep it running
$pythonPath = "d:\Google-Earth\idea1\FutureEarthStimulation\backend\.venv\Scripts\python.exe"
$scriptPath = "d:\Google-Earth\idea1\FutureEarthStimulation\backend\run.py"
$workDir = "d:\Google-Earth\idea1\FutureEarthStimulation\backend"

Set-Location $workDir
& $pythonPath $scriptPath
