$sessionId = "ff9b220c-d3ab-474f-bcf2-713e553a094f"
$baseUrl = "http://localhost:7071/api/assessment/$sessionId"

# Answer questions 4-40 quickly
for ($i = 4; $i -le 40; $i++) {
    $json = "{\"questionNumber\": $i, \"chosenStatementId\": \"A\"}"
    Write-Host "Answering question $i..."
    
    $response = curl -X POST "$baseUrl/answer" -H "Content-Type: application/json" -d $json
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Question $i completed"
    } else {
        Write-Host "Error on question $i"
        break
    }
}

Write-Host "Assessment completed!" 