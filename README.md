## REST API Service for transactions 

### Technologies Used:  <img src="https://vk.com/emoji/e/f09f92bb.png" height="30px"/>
- FastAPI
- AlchemySQL
- PostgreSQL
- Docker

### How to run the service: 
**To run the service, `cd` in the `app` directory and just run `docker-compose up --build`**

### Methods of API:  
- **`POST /add_client/`**  
**Adds new client in the Database**  
**Example of using the method**: `{
"name": "Dima",
"balance": 100
}`  
**Example of the result:** `{
"status": 200,
"message": "Client was created successfully, id of the client=43"
}`
- **`GET /get_client_balance/`**  
  **Gets client's balance from the Clients table by `client_id`**  
  **Example of the result:** `{
  "status": 200,
  "message": "Client with client_id=42 was found in clients table",
  "client_id": 42,
  "balance": 10
  }`  
- **`POST /perform_transaction/`**  
  **Method for executing transaction from client1 to client2**  
  **Example of using the method**: `{
  "first_client_id": 42,
  "second_client_id": 41,
  "amount": 90
  }`  
  **Examples of the result:**  
- `{
  "status": 400,
  "message": "Negative balance for client with client_id=42"
  }`
- `{
  "status": 200,
  "message": "Transaction with client_id=42 and client_id=41 was performed successfully"
  }`



