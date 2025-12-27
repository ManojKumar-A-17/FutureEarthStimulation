# Frontend Verification Script
Write-Host "============================================================"
Write-Host "Frontend Verification Test" -ForegroundColor Cyan
Write-Host "============================================================"

$frontendPath = "D:\Google-Earth\idea1\FutureEarthStimulation\frontend"

if (-not (Test-Path "$frontendPath\package.json")) {
    Write-Host "ERROR: frontend directory not found" -ForegroundColor Red
    exit 1
}

Set-Location $frontendPath

Write-Host "`nChecking Dependencies..." -ForegroundColor Yellow

if (Test-Path "node_modules") {
    Write-Host "  [OK] node_modules found" -ForegroundColor Green
} else {
    Write-Host "  [WARNING] node_modules not found" -ForegroundColor Yellow
    Write-Host "  Run: npm install or bun install" -ForegroundColor Gray
}

Write-Host "`nEnvironment Configuration:" -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  [OK] .env file exists" -ForegroundColor Green
    $envContent = Get-Content ".env"
    if ($envContent -match "VITE_BACKEND_URL") {
        $backendUrl = ($envContent | Select-String "VITE_BACKEND_URL").ToString()
        Write-Host "  [OK] $backendUrl" -ForegroundColor Green
    } else {
        Write-Host "  [WARNING] VITE_BACKEND_URL not set" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [ERROR] .env file not found" -ForegroundColor Red
}

Write-Host "`nVite Configuration:" -ForegroundColor Yellow
if (Test-Path "vite.config.ts") {
    Write-Host "  [OK] vite.config.ts exists" -ForegroundColor Green
    $viteConfig = Get-Content "vite.config.ts" -Raw
    if ($viteConfig -match "port:\s*(\d+)") {
        $port = $matches[1]
        Write-Host "  [OK] Dev server port: $port" -ForegroundColor Green
    }
} else {
    Write-Host "  [ERROR] vite.config.ts not found" -ForegroundColor Red
}

Write-Host "`nKey Source Files:" -ForegroundColor Yellow
$files = @(
    "src\main.tsx",
    "src\types\simulation.ts",
    "src\api\backendClient.ts",
    "src\hooks\useSimulation.ts"
)

$allGood = $true
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] $file missing!" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host "`n============================================================"
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "============================================================"

if ((Test-Path "node_modules") -and (Test-Path ".env") -and $allGood) {
    Write-Host "`n[SUCCESS] Frontend is READY!" -ForegroundColor Green
    Write-Host "`nNext steps:"
    Write-Host "  1. Start backend: cd ..\backend; python run.py"
    Write-Host "  2. Start frontend: npm run dev"
    Write-Host "  3. Open: http://localhost:5173"
} else {
    Write-Host "`n[WARNING] Some issues found" -ForegroundColor Yellow
    if (-not (Test-Path "node_modules")) {
        Write-Host "  - Run: npm install"
    }
    if (-not (Test-Path ".env")) {
        Write-Host "  - Create .env file"
    }
}

Write-Host "============================================================`n"
