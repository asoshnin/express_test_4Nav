#!/usr/bin/env python3
"""
Simple CORS proxy for the assessment API
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.parse
import json

class CORSProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
    
    def do_GET(self):
        self._handle_request('GET')
    
    def do_POST(self):
        self._handle_request('POST')
    
    def _handle_request(self, method):
        # Forward the request to the Azure Functions
        # Add /api prefix since Azure Functions uses routePrefix: "api"
        target_url = f"http://localhost:7072/api{self.path}"
        
        try:
            # Read request body if present
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Create request
            req = urllib.request.Request(target_url, data=body, method=method)
            req.add_header('Content-Type', 'application/json')
            
            # Make the request
            with urllib.request.urlopen(req) as response:
                response_data = response.read()
                
                # Send response
                self.send_response(response.status)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(response_data)
                
        except Exception as e:
            print(f"Error: {e}")
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), CORSProxyHandler)
    print("CORS Proxy running on http://localhost:8080")
    server.serve_forever()
