from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LKH Bank API")

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./bank.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    owner_name = Column(String)
    balance = Column(Float, default=0.0)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    amount = Column(Float)
    transaction_type = Column(String)  # "deposit" or "withdrawal"
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class TransactionResponse(BaseModel):
    id: int
    account_id: int
    amount: float
    transaction_type: str
    timestamp: datetime

class TransferCreate(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float

class AccountCreate(BaseModel):
    account_number: str
    owner_name: str

class AccountResponse(BaseModel):
    id: int
    account_number: str
    owner_name: str
    balance: float

class TransactionCreate(BaseModel):
    account_id: int
    amount: float
    transaction_type: str

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

# Endpoints
@app.post("/accounts/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = Account(
        account_number=account.account_number,
        owner_name=account.owner_name
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@app.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@app.post("/transactions/")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == transaction.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if transaction.transaction_type not in ["deposit", "withdrawal"]:
        raise HTTPException(status_code=400, detail="Invalid transaction type")
    
    if transaction.transaction_type == "withdrawal" and account.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Update account balance
    if transaction.transaction_type == "deposit":
        account.balance += transaction.amount
    else:
        account.balance -= transaction.amount
    
    # Create transaction record
    db_transaction = Transaction(
        account_id=transaction.account_id,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type
    )
    
    db.add(db_transaction)
    db.commit()
    return {"message": "Transaction successful", "new_balance": account.balance}

@app.get("/accounts/", response_model=List[AccountResponse])
def list_accounts(db: Session = Depends(get_db)):
    accounts = db.query(Account).all()
    return accounts

@app.get("/accounts/{account_id}/transactions", response_model=List[TransactionResponse])
def get_account_transactions(account_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.account_id == account_id).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    return transactions

@app.post("/transfer/")
def transfer_money(transfer: TransferCreate, db: Session = Depends(get_db)):
    from_account = db.query(Account).filter(Account.id == transfer.from_account_id).first()
    to_account = db.query(Account).filter(Account.id == transfer.to_account_id).first()
    
    if not from_account or not to_account:
        raise HTTPException(status_code=404, detail="One or both accounts not found")
    
    if from_account.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Process transfer
    from_account.balance -= transfer.amount
    to_account.balance += transfer.amount
    
    # Record transactions
    withdrawal = Transaction(
        account_id=transfer.from_account_id,
        amount=transfer.amount,
        transaction_type="transfer_out"
    )
    deposit = Transaction(
        account_id=transfer.to_account_id,
        amount=transfer.amount,
        transaction_type="transfer_in"
    )
    
    db.add_all([withdrawal, deposit])
    db.commit()
    
    return {
        "message": "Transfer successful",
        "from_account_balance": from_account.balance,
        "to_account_balance": to_account.balance
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)