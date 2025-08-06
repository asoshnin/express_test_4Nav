# Complete Assessment Script
$sessionId = "ff9b220c-d3ab-474f-bcf2-713e553a094f"
$baseUrl = "http://localhost:7071/api/assessment/$sessionId"

# Answer questions 4-40 (we've already answered 1-3)
for ($i = 4; $i -le 40; $i++) {
    $body = "{\"questionNumber\": $i, \"chosenStatementId\": \"A\"}"
    
    Write-Host "Answering question $i..."
    
    $response = curl -X POST "$baseUrl/answer" -H "Content-Type: application/json" -d $body
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Question $i answered successfully"
    } else {
        Write-Host "Error answering question $i"
        break
    }
    
    # Small delay to avoid overwhelming the server
    Start-Sleep -Milliseconds 100
}

Write-Host "Assessment completed!" 