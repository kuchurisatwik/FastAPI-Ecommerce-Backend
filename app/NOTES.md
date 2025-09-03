### 

### **Database Schema:**



**Users (id, email, password, role, created-at).**



**Products (id, name, description, price, stock, category, created-at).**



**Orders (id, user-id, status, total-price, created-at).**



**Order-Items (id, order-id, product-id, quantity, price).**



**Payments (id, order-id, status, amount, created-at).**









### **Endpoints In Desc-Order:**



**User-GET, POST, DELETE**



**Products-GET, POST(ADMIN), PUT(ADMIN), DELETE(ADMIN)**



**Orders-GET,POST,DELETE**



**Order-Items-GET,POST, PUT(for user to increase or decrease the quantity size), DELETE**



**Payments-GET, POST**





