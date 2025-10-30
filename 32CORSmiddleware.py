"""
FastAPI CORS Middleware - Lesson 32

This module demonstrates Cross-Origin Resource Sharing (CORS) implementation
in FastAPI applications. CORS is a security feature implemented by web browsers
that restricts web pages from making requests to a different domain, protocol,
or port than the one serving the web page. This middleware enables controlled
cross-origin access for web applications.

CORS Fundamentals:
    Cross-Origin Resource Sharing (CORS) is a mechanism that allows restricted
    resources on a web page to be requested from another domain outside the
    domain from which the first resource was served. It's essential for modern
    web applications that need to access APIs from different origins.

Problem Statement:
    Without CORS configuration, browsers block requests from web applications
    running on different origins (domain, port, or protocol) to your API.
    This is known as the "Same-Origin Policy" security restriction.

CORS Components:
    - Preflight Requests: OPTIONS requests sent by browsers for complex requests
    - Access-Control Headers: Headers that define allowed origins, methods, headers
    - Credentials Handling: Managing cookies and authorization headers
    - Request Validation: Checking if requests are allowed from specific origins

Security Considerations:
    - Origin Validation: Strictly control which domains can access your API
    - Credential Handling: Carefully manage when to allow credentials
    - Method Restrictions: Limit allowed HTTP methods based on security needs
    - Header Filtering: Control which headers can be sent in cross-origin requests

Production Use Cases:
    - Web applications accessing APIs from different subdomains
    - Frontend frameworks (React, Vue, Angular) calling backend APIs
    - Mobile applications with web views accessing web APIs
    - Third-party integrations and partner API access
    - Microservices architecture with cross-service communication

FastAPI CORS Implementation:
    FastAPI provides built-in CORS middleware that handles:
    - Automatic preflight request processing
    - Origin validation and header injection
    - Method and header filtering
    - Credential policy enforcement

Key Learning Objectives:
    - Understand CORS security model and browser behavior
    - Configure CORS middleware for different environments
    - Handle preflight requests and complex CORS scenarios
    - Implement secure origin validation policies
    - Debug CORS issues in web applications

Browser Compatibility:
    - Modern browsers automatically handle CORS preflight requests
    - Different browsers may have varying CORS behavior
    - Mobile browsers and web views follow CORS policies
    - Development tools help debug CORS-related issues

Testing Scenarios:
    - Same-origin requests (no CORS headers needed)
    - Cross-origin requests from allowed origins
    - Cross-origin requests from blocked origins
    - Preflight requests for complex operations
    - Credential-including requests

Author: FastAPI Learning Series
Created: 2025-10-30
Dependencies: FastAPI, Pydantic
Security Level: Medium (CORS configuration affects web security)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# FastAPI application instance with CORS capabilities
app = FastAPI(
    title="FastAPI CORS Middleware Demo",
    description="Demonstration of Cross-Origin Resource Sharing configuration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration - allowed origins for cross-origin requests
origins = ["http://localhost.tiangolo.com", 
           "https://localhost.tiangolo.com", 
           "http://localhost", 
           "http://localhost:8080"]
"""
Allowed origins configuration for CORS middleware.

This list defines which domains, protocols, and ports are permitted to make
cross-origin requests to this FastAPI application. Each entry represents
a complete origin (protocol + domain + port) that browsers will allow
to access the API from web pages.

Origin Components:
    - Protocol: http or https (must match exactly)
    - Domain: localhost, localhost.tiangolo.com, example.com, etc.
    - Port: Specific port numbers (8080, 3000, etc.) or default ports

Current Configuration:
    - http://localhost.tiangolo.com: Tiangolo's local development domain
    - https://localhost.tiangolo.com: Secure version of Tiangolo's domain
    - http://localhost: Local development without port specification
    - http://localhost:8080: Common development port for web applications

Security Implications:
    - Wildcard "*" allows ALL origins (dangerous for production)
    - Specific origins provide granular access control
    - Protocol specification prevents mixed HTTP/HTTPS attacks
    - Port specification prevents access from unexpected services

Development vs Production:
    Development Origins:
        - http://localhost:3000 (React default)
        - http://localhost:4200 (Angular default)
        - http://localhost:5173 (Vite default)
        - http://localhost:8080 (Common development port)
    
    Production Origins:
        - https://yourdomain.com (Production website)
        - https://app.yourdomain.com (Application subdomain)
        - https://admin.yourdomain.com (Admin interface)
        - https://api.yourdomain.com (API documentation)

Dynamic Origin Configuration:
    ```python
    import os
    
    # Environment-based origin configuration
    if os.getenv("ENVIRONMENT") == "development":
        origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:8080",
            "http://127.0.0.1:3000"
        ]
    elif os.getenv("ENVIRONMENT") == "staging":
        origins = [
            "https://staging.yourdomain.com",
            "https://staging-api.yourdomain.com"
        ]
    else:  # production
        origins = [
            "https://yourdomain.com",
            "https://www.yourdomain.com",
            "https://app.yourdomain.com"
        ]
    ```

Common Origin Patterns:
    - Frontend applications: Different port from API
    - Subdomain APIs: api.example.com from www.example.com
    - CDN content: Static assets from different domains
    - Partner integrations: Specific partner domains

Debugging Origins:
    - Check browser developer tools for CORS errors
    - Verify exact origin string (including protocol and port)
    - Test with curl to bypass browser CORS enforcement
    - Use browser extensions to temporarily disable CORS
"""

# CORS middleware configuration for cross-origin request handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
CORS (Cross-Origin Resource Sharing) middleware configuration.

This middleware automatically handles CORS preflight requests and adds
appropriate headers to responses, enabling web browsers to make cross-origin
requests from allowed domains to this FastAPI application.

Configuration Parameters:

allow_origins (List[str]):
    - Specifies which origins are allowed to make cross-origin requests
    - Current: Uses the predefined origins list for controlled access
    - Alternative: ["*"] allows all origins (NOT recommended for production)
    - Security: Restricts access to explicitly approved domains only

allow_credentials (bool):
    - True: Allows cookies, authorization headers, and TLS client certificates
    - False: Blocks credential-including requests from cross-origin sources
    - Current: True - enables authenticated cross-origin requests
    - Security: Only enable if frontend needs to send authentication data

allow_methods (List[str]):
    - Specifies which HTTP methods are allowed for cross-origin requests
    - Current: ["*"] allows all methods (GET, POST, PUT, DELETE, etc.)
    - Alternative: ["GET", "POST"] for restricted method access
    - Security: Limit to required methods for better security

allow_headers (List[str]):
    - Defines which headers can be sent in cross-origin requests
    - Current: ["*"] allows all headers
    - Alternative: ["Content-Type", "Authorization"] for specific headers
    - Security: Restrict to necessary headers in production

CORS Headers Generated:
    The middleware automatically adds these headers to responses:
    - Access-Control-Allow-Origin: Specifies allowed origin
    - Access-Control-Allow-Credentials: Indicates credential support
    - Access-Control-Allow-Methods: Lists permitted HTTP methods
    - Access-Control-Allow-Headers: Defines acceptable request headers
    - Access-Control-Max-Age: Caches preflight results (optional)

Preflight Request Handling:
    For complex requests, browsers send OPTIONS preflight requests:
    1. Browser detects cross-origin request with custom headers/methods
    2. Sends OPTIONS request to API endpoint
    3. API responds with CORS headers indicating permissions
    4. Browser proceeds with actual request if allowed
    5. Browser blocks request if CORS headers deny access

Production Security Configuration:
    ```python
    # Secure production CORS setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://yourdomain.com",
            "https://www.yourdomain.com",
            "https://app.yourdomain.com"
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=[
            "Accept",
            "Accept-Language",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With"
        ],
        max_age=600  # Cache preflight for 10 minutes
    )
    ```

Development vs Production Settings:
    Development (Current):
        - Permissive origins including localhost
        - All methods and headers allowed
        - Credentials enabled for authentication testing
    
    Production Recommendations:
        - Specific production domains only
        - Limited methods based on API requirements
        - Restricted headers to minimize attack surface
        - Regular security audits of CORS configuration

Common CORS Scenarios:
    1. Simple Requests: GET, POST with standard headers
       - No preflight required
       - CORS headers added to response
    
    2. Preflight Requests: Custom headers, PUT/DELETE methods
       - OPTIONS request sent first
       - Actual request follows if allowed
    
    3. Credentialed Requests: Requests with cookies/auth headers
       - Requires allow_credentials=True
       - Origin must be specific (not wildcard)

Debugging CORS Issues:
    1. Check browser console for CORS error messages
    2. Verify origin matches exactly (protocol, domain, port)
    3. Inspect OPTIONS preflight requests in network tab
    4. Test with curl to bypass browser CORS enforcement
    5. Temporarily use ["*"] origins for debugging (remove after)

Security Best Practices:
    - Never use "*" for origins in production with credentials
    - Regularly audit and update allowed origins list
    - Use HTTPS origins in production environments
    - Monitor for unauthorized cross-origin access attempts
    - Consider implementing additional rate limiting

Browser Compatibility:
    - All modern browsers support CORS automatically
    - Mobile browsers and WebViews follow CORS policies
    - Some browsers cache preflight responses differently
    - Development tools help debug CORS-related issues
"""

# Data model for item creation and management
class Item(BaseModel):
    """
    Pydantic model representing an item in the application.
    
    This model demonstrates how CORS middleware works with different types
    of API endpoints, including those that process JSON request bodies
    from cross-origin web applications.
    
    Attributes:
        name (str): The unique identifier and display name for the item.
                   Required field used for item identification.
        description (str, optional): Additional details about the item.
                                   Defaults to None if not provided.
    
    CORS Integration:
        - JSON serialization/deserialization works seamlessly with CORS
        - Request body parsing occurs after CORS validation
        - Response serialization includes CORS headers automatically
        - Validation errors include appropriate CORS headers
    
    Cross-Origin Usage:
        Web applications from allowed origins can send JSON data:
        ```javascript
        // Frontend JavaScript making CORS request
        const item = {
            name: "laptop",
            description: "High-performance development laptop"
        };
        
        fetch('http://localhost:8000/items/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(item)
        })
        .then(response => response.json())
        .then(data => console.log('Item created:', data));
        ```
    
    Validation and CORS:
        - Pydantic validation occurs after CORS preflight
        - Validation errors include CORS headers for cross-origin clients
        - Browser can display validation errors from cross-origin API
        - Type conversion works for cross-origin JSON data
    
    Production Considerations:
        - Add field validators for business logic
        - Implement proper error messages for cross-origin clients
        - Consider field aliases for API compatibility
        - Add comprehensive documentation for API consumers
    """
    name: str
    description: str = None

# In-memory storage for items (demonstration purposes)
items = []
"""
Simple in-memory list for storing items to demonstrate CORS functionality.

This list serves as a basic data store to show how CORS middleware
interacts with different types of operations:
- GET requests: Retrieving data across origins
- POST requests: Sending data from cross-origin web applications
- JSON handling: Serialization/deserialization with CORS headers

CORS Interaction:
    - GET operations: Return data with CORS headers for cross-origin access
    - POST operations: Accept JSON data from allowed origins
    - Response formatting: Automatic CORS header inclusion
    - Error handling: CORS-compliant error responses

Production Alternative:
    In production applications, this would be replaced with:
    - Database connections (PostgreSQL, MongoDB, etc.)
    - ORM operations with proper transaction handling
    - Caching layers for improved performance
    - Data validation and business logic layers
    
    CORS middleware works transparently with all data sources:
    ```python
    # Database example with CORS
    @app.get("/items/")
    async def get_items(db: Session = Depends(get_db)):
        items = db.query(ItemModel).all()
        # CORS headers automatically added to response
        return [ItemResponse.from_orm(item) for item in items]
    ```
"""

# Root endpoint demonstrating basic CORS functionality
@app.get("/")
async def main():
    """
    Root endpoint providing basic application status with CORS support.
    
    This simple endpoint demonstrates how CORS middleware automatically
    adds appropriate headers to all responses, enabling cross-origin
    access from web applications running on allowed domains.
    
    Returns:
        dict: Simple welcome message confirming service availability
    
    CORS Headers Added:
        The middleware automatically includes headers like:
        - Access-Control-Allow-Origin: <requesting-origin>
        - Access-Control-Allow-Credentials: true
        - Vary: Origin (for caching considerations)
    
    Cross-Origin Testing:
        ```javascript
        // Test from browser console on allowed origin
        fetch('http://localhost:8000/')
            .then(response => response.json())
            .then(data => console.log(data));
        // Should work from allowed origins, fail from others
        ```
    
    Browser Behavior:
        - Same-origin requests: No CORS headers needed
        - Cross-origin from allowed origins: Request succeeds with CORS headers
        - Cross-origin from blocked origins: Browser blocks request
        - Preflight not required: Simple GET request with standard headers
    
    Response Format:
        ```json
        {
            "message": "Hello World"
        }
        ```
    
    Use Cases:
        - Health checks from web dashboards on different domains
        - Service discovery for microservices architecture
        - API testing from development tools
        - Integration with monitoring systems from different origins
    
    Development Testing:
        ```bash
        # Test CORS headers with curl
        curl -H "Origin: http://localhost:3000" \
             -H "Access-Control-Request-Method: GET" \
             -H "Access-Control-Request-Headers: X-Requested-With" \
             -X OPTIONS http://localhost:8000/
        
        # Actual request
        curl -H "Origin: http://localhost:3000" \
             http://localhost:8000/
        ```
    
    Production Monitoring:
        - Monitor cross-origin requests for unusual patterns
        - Track which origins are making requests
        - Alert on requests from unauthorized origins
        - Log CORS preflight failures for security analysis
    """
    return {"message": "Hello World"}

# Items retrieval endpoint with CORS support
@app.get("/items/")
async def get_items():
    """
    Retrieve all items with automatic CORS header inclusion.
    
    This endpoint demonstrates how CORS middleware handles data retrieval
    requests from cross-origin web applications. The response automatically
    includes appropriate CORS headers based on the requesting origin.
    
    Returns:
        list: All items currently stored in the application
    
    CORS Behavior:
        - Simple GET request requires no preflight
        - CORS headers added automatically to response
        - JSON serialization works transparently with CORS
        - Browser allows cross-origin access from permitted origins
    
    Response Format:
        ```json
        [
            {
                "name": "laptop",
                "description": "Development machine"
            },
            {
                "name": "mouse",
                "description": null
            }
        ]
        ```
    
    Cross-Origin Usage Example:
        ```javascript
        // Frontend code from allowed origin
        async function fetchItems() {
            try {
                const response = await fetch('http://localhost:8000/items/');
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const items = await response.json();
                console.log('Retrieved items:', items);
                return items;
                
            } catch (error) {
                if (error.name === 'TypeError' && error.message.includes('CORS')) {
                    console.error('CORS error: Origin not allowed');
                } else {
                    console.error('Fetch error:', error);
                }
            }
        }
        ```
    
    React Component Example:
        ```jsx
        import React, { useState, useEffect } from 'react';
        
        function ItemList() {
            const [items, setItems] = useState([]);
            const [loading, setLoading] = useState(true);
            
            useEffect(() => {
                fetch('http://localhost:8000/items/')
                    .then(response => response.json())
                    .then(data => {
                        setItems(data);
                        setLoading(false);
                    })
                    .catch(error => {
                        console.error('Error fetching items:', error);
                        setLoading(false);
                    });
            }, []);
            
            if (loading) return <div>Loading...</div>;
            
            return (
                <ul>
                    {items.map((item, index) => (
                        <li key={index}>
                            <strong>{item.name}</strong>
                            {item.description && `: ${item.description}`}
                        </li>
                    ))}
                </ul>
            );
        }
        ```
    
    Vue.js Example:
        ```vue
        <template>
            <div>
                <h2>Items</h2>
                <ul v-if="items.length">
                    <li v-for="item in items" :key="item.name">
                        {{ item.name }}
                        <span v-if="item.description">: {{ item.description }}</span>
                    </li>
                </ul>
                <p v-else>No items found</p>
            </div>
        </template>
        
        <script>
        export default {
            data() {
                return {
                    items: []
                };
            },
            async mounted() {
                try {
                    const response = await fetch('http://localhost:8000/items/');
                    this.items = await response.json();
                } catch (error) {
                    console.error('Failed to fetch items:', error);
                }
            }
        };
        </script>
        ```
    
    Performance Considerations:
        - CORS headers add minimal overhead to responses
        - Browser caching works normally with CORS responses
        - Consider pagination for large item lists
        - Monitor cross-origin request patterns for optimization
    
    Security Notes:
        - Data exposure: Consider what data is safe for cross-origin access
        - Rate limiting: Implement limits for cross-origin requests
        - Authentication: May require additional handling for credentialed requests
        - Monitoring: Track cross-origin access patterns
    
    Testing CORS:
        ```bash
        # Test from allowed origin
        curl -H "Origin: http://localhost:3000" \
             http://localhost:8000/items/
        
        # Test from blocked origin (should work with curl but not browser)
        curl -H "Origin: http://malicious.com" \
             http://localhost:8000/items/
        ```
    
    Production Enhancements:
        - Add query parameters for filtering and pagination
        - Implement caching headers for better performance
        - Add compression for large responses
        - Include proper error handling for database failures
    """
    return items

# Item creation endpoint demonstrating CORS with POST requests
@app.post("/items/")
async def create_item(item: Item):
    """
    Create a new item with CORS support for cross-origin POST requests.
    
    This endpoint demonstrates how CORS middleware handles complex requests
    that may require preflight OPTIONS requests. POST requests with JSON
    content-type typically trigger preflight validation by browsers.
    
    Args:
        item (Item): Pydantic model containing item data from request body
    
    Returns:
        Item: The created item object confirming successful creation
    
    CORS Preflight Behavior:
        For POST requests with JSON content, browsers typically send:
        1. OPTIONS preflight request to check permissions
        2. Actual POST request if preflight succeeds
        3. CORS headers included in both preflight and actual responses
    
    Request Flow:
        ```
        Browser → OPTIONS /items/ (preflight)
                ← 200 OK with CORS headers
        Browser → POST /items/ (actual request)
                ← 200 OK with item data + CORS headers
        ```
    
    Cross-Origin POST Example:
        ```javascript
        // Frontend code creating items from allowed origin
        async function createItem(itemData) {
            try {
                const response = await fetch('http://localhost:8000/items/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        // Browser automatically adds Origin header
                    },
                    body: JSON.stringify(itemData)
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const createdItem = await response.json();
                console.log('Item created:', createdItem);
                return createdItem;
                
            } catch (error) {
                console.error('Error creating item:', error);
                throw error;
            }
        }
        
        // Usage
        createItem({
            name: "keyboard",
            description: "Mechanical keyboard for programming"
        });
        ```
    
    React Form Example:
        ```jsx
        import React, { useState } from 'react';
        
        function ItemForm({ onItemCreated }) {
            const [name, setName] = useState('');
            const [description, setDescription] = useState('');
            const [loading, setLoading] = useState(false);
            
            const handleSubmit = async (e) => {
                e.preventDefault();
                setLoading(true);
                
                try {
                    const response = await fetch('http://localhost:8000/items/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            name,
                            description: description || null
                        })
                    });
                    
                    if (response.ok) {
                        const newItem = await response.json();
                        onItemCreated(newItem);
                        setName('');
                        setDescription('');
                    } else {
                        console.error('Failed to create item');
                    }
                } catch (error) {
                    console.error('Error:', error);
                } finally {
                    setLoading(false);
                }
            };
            
            return (
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Item name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />
                    <input
                        type="text"
                        placeholder="Description (optional)"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? 'Creating...' : 'Create Item'}
                    </button>
                </form>
            );
        }
        ```
    
    Fetch API with Error Handling:
        ```javascript
        async function createItemWithErrorHandling(itemData) {
            try {
                const response = await fetch('http://localhost:8000/items/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(itemData),
                    credentials: 'include'  // If authentication needed
                });
                
                // Handle different response status codes
                if (response.status === 422) {
                    const errorData = await response.json();
                    throw new Error(`Validation error: ${JSON.stringify(errorData)}`);
                }
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                return await response.json();
                
            } catch (error) {
                if (error.name === 'TypeError' && error.message.includes('fetch')) {
                    console.error('Network error or CORS issue:', error);
                } else {
                    console.error('API error:', error);
                }
                throw error;
            }
        }
        ```
    
    CORS Preflight Details:
        ```http
        # Browser sends preflight request
        OPTIONS /items/ HTTP/1.1
        Origin: http://localhost:3000
        Access-Control-Request-Method: POST
        Access-Control-Request-Headers: content-type
        
        # Server responds with permissions
        HTTP/1.1 200 OK
        Access-Control-Allow-Origin: http://localhost:3000
        Access-Control-Allow-Methods: POST
        Access-Control-Allow-Headers: content-type
        Access-Control-Allow-Credentials: true
        ```
    
    Authentication with CORS:
        ```javascript
        // Sending authenticated requests with CORS
        async function createAuthenticatedItem(itemData, token) {
            const response = await fetch('http://localhost:8000/items/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                credentials: 'include',  // Include cookies
                body: JSON.stringify(itemData)
            });
            
            return response.json();
        }
        ```
    
    Testing CORS POST:
        ```bash
        # Test preflight request
        curl -X OPTIONS "http://localhost:8000/items/" \
             -H "Origin: http://localhost:3000" \
             -H "Access-Control-Request-Method: POST" \
             -H "Access-Control-Request-Headers: content-type"
        
        # Test actual POST request
        curl -X POST "http://localhost:8000/items/" \
             -H "Origin: http://localhost:3000" \
             -H "Content-Type: application/json" \
             -d '{"name": "test-item", "description": "Test description"}'
        ```
    
    Validation and CORS:
        - Pydantic validation errors include CORS headers
        - 422 status responses work with cross-origin requests
        - Error messages are accessible from allowed origins
        - Browser can display validation feedback from API
    
    Production Considerations:
        - Monitor preflight request frequency for performance
        - Consider caching preflight responses with max_age
        - Implement proper authentication for item creation
        - Add rate limiting for cross-origin POST requests
        - Log creation events for audit trails
    
    Security Best Practices:
        - Validate origin even with CORS middleware
        - Implement proper authentication and authorization
        - Monitor for suspicious cross-origin creation patterns
        - Consider additional validation for cross-origin requests
        - Rate limit by origin to prevent abuse
    """
    items.append(item)
    return item