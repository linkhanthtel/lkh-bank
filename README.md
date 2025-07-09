# LKH Bank API

A RESTful banking API built with FastAPI that provides basic banking operations including account management, transactions, and money transfers.

## Features

- **Account Management**: Create and retrieve bank accounts
- **Transaction Processing**: Handle deposits and withdrawals
- **Money Transfers**: Transfer funds between accounts
- **Transaction History**: View account transaction history
- **Data Persistence**: SQLite database with SQLAlchemy ORM

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Lightweight database for data storage
- **Uvicorn**: ASGI server for running the application

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd lkh-bank-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install fastapi sqlalchemy pydantic python-dotenv uvicorn
```

4. Create a `.env` file (optional):
```
# Add any environment variables here if needed
```

## Usage

### Running the Application

Start the development server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- **Interactive API docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API docs (ReDoc)**: `http://localhost:8000/redoc`

## API Endpoints

### Accounts

#### Create Account
- **POST** `/accounts/`
- **Body**:
  ```json
  {
    "account_number": "123456789",
    "owner_name": "John Doe"
  }
  ```

#### Get Account
- **GET** `/accounts/{account_id}`
- Returns account details including current balance

#### List All Accounts
- **GET** `/accounts/`
- Returns all accounts in the system

### Transactions

#### Create Transaction
- **POST** `/transactions/`
- **Body**:
  ```json
  {
    "account_id": 1,
    "amount": 100.0,
    "transaction_type": "deposit"
  }
  ```
- **Transaction Types**: `deposit` or `withdrawal`

#### Get Account Transactions
- **GET** `/accounts/{account_id}/transactions`
- Returns transaction history for a specific account

### Transfers

#### Transfer Money
- **POST** `/transfer/`
- **Body**:
  ```json
  {
    "from_account_id": 1,
    "to_account_id": 2,
    "amount": 50.0
  }
  ```

## Database Schema

### Accounts Table
- `id`: Primary key (Integer)
- `account_number`: Unique account identifier (String)
- `owner_name`: Account holder name (String)
- `balance`: Current account balance (Float, default: 0.0)

### Transactions Table
- `id`: Primary key (Integer)
- `account_id`: Foreign key to accounts table (Integer)
- `amount`: Transaction amount (Float)
- `transaction_type`: Type of transaction (String)
- `timestamp`: Transaction timestamp (DateTime)

## Error Handling

The API includes comprehensive error handling:
- **404**: Account not found
- **400**: Invalid transaction type or insufficient funds
- **422**: Validation errors for request data

## Example Usage

### Creating an Account
```bash
curl -X POST "http://localhost:8000/accounts/" \\
     -H "Content-Type: application/json" \\
     -d '{
       "account_number": "123456789",
       "owner_name": "John Doe"
     }'
```

### Making a Deposit
```bash
curl -X POST "http://localhost:8000/transactions/" \\
     -H "Content-Type: application/json" \\
     -d '{
       "account_id": 1,
       "amount": 1000.0,
       "transaction_type": "deposit"
     }'
```

### Transferring Money
```bash
curl -X POST "http://localhost:8000/transfer/" \\
     -H "Content-Type: application/json" \\
     -d '{
       "from_account_id": 1,
       "to_account_id": 2,
       "amount": 100.0
     }'
```

## Development

### Project Structure
```
lkh-bank-api/
├── main.py              # Main application file
├── bank.db              # SQLite database (created automatically)
├── .env                 # Environment variables (optional)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Features

1. Define new database models in the Models section
2. Create corresponding Pydantic schemas
3. Implement new endpoints with proper error handling
4. Update the database schema if needed

## Security Considerations

⚠️ **Important**: This is a basic implementation for demonstration purposes. For production use, consider:

- Authentication and authorization
- Input validation and sanitization
- Rate limiting
- HTTPS encryption
- Database connection pooling
- Proper error logging
- Transaction atomicity for complex operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue in the repository or contact the development team.
```

