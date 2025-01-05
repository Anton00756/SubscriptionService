from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    subscriptions = relationship('Subscription', back_populates='user')
    payment_methods = relationship('PaymentMethod', back_populates='user')
    payments = relationship('Payment', back_populates='user')


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, nullable=False)  # Тип подписки, например, "Premium", "Basic"
    price = Column(Float)
    is_active = Column(Boolean, default=True)
    duration = Column(Integer, default=30)
    auto_renew = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # Связь с таблицей пользователей
    user = relationship('User', back_populates='subscriptions')


class PaymentMethod(Base):
    __tablename__ = 'payment_methods'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # Тип способа оплаты (например, "карта", "PayPal")
    card_number = Column(String, unique=True)
    expiry_date = Column(String)
    cvv = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='payment_methods')


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer)
    amount = Column(Float, nullable=False)  # Сумма платежа
    status = Column(String, nullable=False)  # Статус платежа (pending, success, failed)
    user_id = Column(Integer, ForeignKey('users.id'))
    open_date = Column(DateTime, default=datetime.now)
    user = relationship('User', back_populates='payments')
