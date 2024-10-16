import pytest
from datetime import datetime
from bson import ObjectId
from Model.model import BondingFund, Notification, Fund, Transaction, User, AccountMonetary, PyObjectId


# Fixture para crear un ObjectId válido
@pytest.fixture
def valid_object_id():
    return str(ObjectId())


# Pruebas para BondingFund
def test_bonding_fund_creation(valid_object_id):
    bonding_fund = BondingFund(
        fundId=valid_object_id,
        investedAmount=1000,
        bondingDate=datetime.now(),
        userId=valid_object_id,
        notificationPreferences="email",
        notificationId=valid_object_id,
        uniqueNumber="UNIQUE123"
    )
    assert bonding_fund.investedAmount == 1000
    assert bonding_fund.notificationPreferences == "email"


# Pruebas para Notification
def test_notification_creation(valid_object_id):
    notification = Notification(
        transactionId=valid_object_id,
        medium="email",
        sendDate=datetime.now()
    )
    assert notification.medium == "email"
    assert isinstance(notification.sendDate, datetime)


# Pruebas para Fund
def test_fund_creation():
    fund = Fund(
        name="Test Fund",
        minimumAmount=500,
        category="Investment"
    )
    assert fund.name == "Test Fund"
    assert fund.minimumAmount == 500
    assert fund.category == "Investment"


# Pruebas para Transaction
def test_transaction_creation(valid_object_id):
    transaction = Transaction(
        bondingFundId=valid_object_id,
        fundId=valid_object_id,
        type="apertura",
        amount=100,
        date=datetime.now(),
        status="completado",
        uniqueNumber="TRANS123"
    )
    assert transaction.type == "apertura"
    assert transaction.amount == 100
    assert transaction.status == "completado"


# Pruebas para User
def test_user_creation():
    user = User(
        email="user@example.com",
        hashedPassword="hashed_password",
        fullName="John Doe",
        phoneNumber="1234567890",
        isActive=True,
        isSuperuser=False,
        createdAt=datetime.now()
    )
    assert user.email == "user@example.com"
    assert user.isActive is True


# Pruebas para AccountMonetary
def test_account_monetary_creation(valid_object_id):
    account = AccountMonetary(
        userId=valid_object_id,
        amount=1500,
        createdAt=datetime.now()
    )
    assert account.amount == 1500
    assert isinstance(account.createdAt, datetime)


# Prueba de validación de PyObjectId
def test_py_object_id_validation():
    with pytest.raises(ValueError):
        PyObjectId.validate("invalid_object_id")  # Debe lanzar un ValueError
