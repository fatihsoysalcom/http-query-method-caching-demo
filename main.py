import http.server
import socketserver
import threading
import time
import json
import http.client

# Global in-memory cache for demonstration purposes.
# In a real application, this would be a more robust caching solution (e.g., Redis, Memcached).
CACHE = {}
PORT = 8000

class QueryRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    Custom HTTP request handler to demonstrate the conceptual HTTP QUERY method
    and its caching challenges.
    """

    # The article refers to RFC 10008 as a placeholder for a new method.
    # Standard http.server doesn't support 'QUERY' natively, so we implement do_QUERY.
    def do_QUERY(self):
        """
        Handles HTTP QUERY requests.
        This method simulates processing a complex query from the request body
        and demonstrates a basic caching mechanism.
        """
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length:
            request_body_bytes = self.rfile.read(content_length)
            try:
                query_params = json.loads(request_body_bytes.decode('utf-8'))
                # Use sorted JSON string as cache key to ensure consistent keys for identical queries
                query_key = json.dumps(query_params, sort_keys=True)
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON in request body")
                return
        else:
            query_params = {}
            query_key = "{}" # Empty query

        self.send_response(200)
        self.send_header("Content-Type", "application/json")

        # Simulate caching logic based on the request body (the query itself)
        if query_key in CACHE:
            # Cache Hit: Return cached data immediately
            response_data = CACHE[query_key]
            self.send_header("X-Cache", "HIT") # Indicate cache status in a custom header
            print(f"Server: Cache HIT for query: {query_key}")
        else:
            # Cache Miss: Simulate database lookup or complex computation
            print(f"Server: Cache MISS for query: {query_key}. Simulating work...")
            time.sleep(1) # Simulate delay for processing a new query
            
            # Generate a dynamic response based on query parameters.
            # In a real scenario, this would involve querying a database
            # or performing complex calculations.
            result = {
                "query_received": query_params,
                "data": [
                    {"id": 1, "name": f"Item A for {query_params.get('type', 'default')}"},
                    {"id": 2, "name": f"Item B for {query_params.get('type', 'default')}"}
                ],
                "timestamp": time.time()
            }
            if "filter" in query_params:
                result["data"] = [d for d in result["data"] if query_params["filter"] in d["name"]]

            response_data = result
            CACHE[query_key] = response_data # Store the new result in cache
            self.send_header("X-Cache", "MISS") # Indicate cache status
            print(f"Server: Stored in cache: {query_key}")

        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

def run_server():
    """Starts a simple HTTP server in a separate thread."""
    with socketserver.TCPServer(('', PORT), QueryRequestHandler) as httpd:
        print(f"Server: Serving on port {PORT}")
        # httpd.serve_forever() blocks, so we run it in a thread
        httpd.serve_forever()

def run_client():
    """Sends sample HTTP QUERY requests to the server."""
    print("\nClient: Sending QUERY requests...")
    conn = http.client.HTTPConnection("localhost", PORT)

    # --- Test Case 1: First request for a specific query ---
    query1 = {"type": "products", "filter": "Item A"}
    query1_body = json.dumps(query1)
    print(f"\nClient: Sending QUERY 1 (first time): {query1_body}")
    conn.request("QUERY", "/data", body=query1_body, headers={"Content-Type": "application/json"})
    response = conn.getresponse()
    print(f"Client: Response Status: {response.status}, X-Cache: {response.getheader('X-Cache')}")
    print(f"Client: Response Body: {response.read().decode('utf-8')[:100]}...") # Print first 100 chars
    response.close()
    time.sleep(0.5) # Small delay for readability

    # --- Test Case 2: Same query as Test Case 1 (should be a cache hit) ---
    print(f"\nClient: Sending QUERY 1 (second time, expecting cache HIT): {query1_body}")
    conn.request("QUERY", "/data", body=query1_body, headers={"Content-Type": "application/json"})
    response = conn.getresponse()
    print(f"Client: Response Status: {response.status}, X-Cache: {response.getheader('X-Cache')}")
    print(f"Client: Response Body: {response.read().decode('utf-8')[:100]}...")
    response.close()
    time.sleep(0.5)

    # --- Test Case 3: A different query (should be a cache miss) ---
    query2 = {"type": "users", "limit": 10}
    query2_body = json.dumps(query2)
    print(f"\nClient: Sending QUERY 2 (first time): {query2_body}")
    conn.request("QUERY", "/data", body=query2_body, headers={"Content-Type": "application/json"})
    response = conn.getresponse()
    print(f"Client: Response Status: {response.status}, X-Cache: {response.getheader('X-Cache')}")
    print(f"Client: Response Body: {response.read().decode('utf-8')[:100]}...")
    response.close()
    time.sleep(0.5)

    conn.close()
    print("\nClient: All QUERY requests sent.")

if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Give the server a moment to start up
    time.sleep(1.5) 

    # Run the client operations
    run_client()

    # In a real application, you'd have a way to gracefully shut down the server.
    # For this self-contained example, the server thread will exit when the main program exits
    # because it's a daemon thread.
    print("\nMain: Example finished. Server thread will terminate.")
