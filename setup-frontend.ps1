# AI Navigator Profiler - Frontend Setup Script
# This script sets up the React frontend for local development

Write-Host "🚀 Setting up AI Navigator Profiler Frontend..." -ForegroundColor Green

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 16 or higher." -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check if npm is available
try {
    $npmVersion = npm --version
    Write-Host "✅ npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found. Please install npm." -ForegroundColor Red
    exit 1
}

# Navigate to frontend directory
if (Test-Path "frontend") {
    Set-Location "frontend"
    Write-Host "📁 Navigated to frontend directory" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend directory not found. Please run this script from the project root." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check if backend is running
Write-Host "🔍 Checking if backend is running..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:7071/api/health" -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend is running on http://localhost:7071" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Backend responded with status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Backend not running on http://localhost:7071" -ForegroundColor Yellow
    Write-Host "Please start the backend first:" -ForegroundColor Cyan
    Write-Host "  cd .." -ForegroundColor White
    Write-Host "  func start" -ForegroundColor White
}

# Start development server
Write-Host "🚀 Starting development server..." -ForegroundColor Green
Write-Host "The frontend will be available at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

npm run dev 