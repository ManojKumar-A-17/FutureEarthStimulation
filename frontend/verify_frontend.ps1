#!/usr/bin/env pwsh
# Frontend Verification Script

Write-Host ""
Write-Host "============================================================"
Write-Host "🎨 Frontend Verification Test" -ForegroundColor Cyan
Write-Host "============================================================"

$frontendPath = "D:\Google-Earth\idea1\FutureEarthStimulation\frontend"

# Check if we're in the right directory
if (-not (Test-Path "$frontendPath\package.json")) {
    Write-Host "❌ ERROR: frontend directory not found" -ForegroundColor Red
    exit 1
}

Set-Location $frontendPath

Write-Host "`n📋 Checking Dependencies..." -ForegroundColor Yellow

# Check if node_modules exists
if (Test-Path "node_modules") {
    Write-Host "  ✅ node_modules found" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  node_modules not found - need to install" -ForegroundColor Yellow
    Write-Host "     Run: npm install or bun install" -ForegroundColor Gray
}

# Check package.json
Write-Host "`n📦 Package Info:" -ForegroundColor Yellow
$packageJson = Get-Content "package.json" | ConvertFrom-Json
Write-Host "  Name: $($packageJson.name)" -ForegroundColor Gray
Write-Host "  Version: $($packageJson.version)" -ForegroundColor Gray
Write-Host "  React: $($packageJson.dependencies.react)" -ForegroundColor Gray

# Check critical dependencies
Write-Host "`n🔍 Critical Dependencies:" -ForegroundColor Yellow
$criticalDeps = @{
    "@tanstack/react-query" = "API state management"
    "framer-motion" = "Animations"
    "lucide-react" = "Icons"
    "sonner" = "Toast notifications"
}

foreach ($dep in $criticalDeps.Keys) {
    if ($packageJson.dependencies.$dep) {
        Write-Host "  ✅ $dep ($($criticalDeps[$dep]))" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $dep missing!" -ForegroundColor Red
    }
}

# Check environment file
Write-Host "`n🔧 Environment Configuration:" -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ✅ .env file exists" -ForegroundColor Green
    $envContent = Get-Content ".env"
    if ($envContent -match "VITE_BACKEND_URL") {
        $backendUrl = ($envContent | Select-String "VITE_BACKEND_URL").ToString()
        Write-Host "  ✅ $backendUrl" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  VITE_BACKEND_URL not set" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ❌ .env file not found" -ForegroundColor Red
}

# Check vite config
Write-Host "`n⚙️  Vite Configuration:" -ForegroundColor Yellow
if (Test-Path "vite.config.ts") {
    Write-Host "  ✅ vite.config.ts exists" -ForegroundColor Green
    $viteConfig = Get-Content "vite.config.ts" -Raw
    if ($viteConfig -match "port:\s*(\d+)") {
        $port = $matches[1]
        Write-Host "  ✅ Dev server port: $port" -ForegroundColor Green
        
        if ($port -eq "5173") {
            Write-Host "     (Matches CORS configuration)" -ForegroundColor Gray
        } else {
            Write-Host "     ⚠️  Port mismatch! Backend CORS expects 5173" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "  ❌ vite.config.ts not found" -ForegroundColor Red
}

# Check TypeScript config
Write-Host "`n📘 TypeScript Configuration:" -ForegroundColor Yellow
if (Test-Path "tsconfig.json") {
    Write-Host "  ✅ tsconfig.json exists" -ForegroundColor Green
} else {
    Write-Host "  ❌ tsconfig.json not found" -ForegroundColor Red
}

# Check source files
Write-Host "`n📁 Source Files:" -ForegroundColor Yellow
$requiredFiles = @(
    "src\main.tsx",
    "src\App.tsx",
    "src\types\simulation.ts",
    "src\api\backendClient.ts",
    "src\hooks\useSimulation.ts",
    "src\components\Controls\ControlPanel.tsx",
    "src\components\Results\ResultsPanel.tsx"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file missing!" -ForegroundColor Red
        $allFilesExist = $false
    }
}

# Final summary
Write-Host ""
Write-Host "============================================================"
Write-Host "📊 Verification Summary" -ForegroundColor Cyan
Write-Host "============================================================"

$issues = @()

if (-not (Test-Path "node_modules")) {
    $issues += "Dependencies not installed"
}

if (-not (Test-Path ".env")) {
    $issues += ".env file missing"
}

if (-not $allFilesExist) {
    $issues += "Some source files missing"
}

if ($issues.Count -eq 0) {
    Write-Host ""
    Write-Host "✅ Frontend is READY!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Ensure backend is running on port 8000"
    Write-Host "  2. Run: npm run dev (or bun run dev)"
    Write-Host "  3. Open: http://localhost:5173"
    Write-Host ""
    Write-Host "============================================================"
    exit 0
} else {
    Write-Host ""
    Write-Host "⚠️  Issues Found:" -ForegroundColor Yellow
    foreach ($issue in $issues) {
        Write-Host "  - $issue" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "📝 Fixes:" -ForegroundColor Cyan
    if ($issues -contains "Dependencies not installed") {
        Write-Host "  Run: npm install (or bun install)"
    }
    if ($issues -contains ".env file missing") {
        Write-Host "  Create .env with: VITE_BACKEND_URL=http://127.0.0.1:8000"
    }
    
    Write-Host ""
    Write-Host "============================================================"
    exit 1
}
