# Example of accessing the Brain API using cURL (Command Line)

# Replace with your actual URL and Key
API_URL="http://localhost:8000"
API_KEY="my-secret-key-123"

echo "Sending message to Brain..."

curl -X POST "$API_URL/chat" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY" \
     -d '{
           "user_id": "terminal_user",
           "message": "Hello from the command line!"
         }'

echo "\nDone."
