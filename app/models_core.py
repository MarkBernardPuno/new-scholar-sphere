from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base


class College(Base):
    __tablename__ = "colleges"

    college_id = Column(Integer, primary_key=True, index=True)
    college_name = Column(String(255), nullable=False)
    college_campus = Column(String(255), nullable=False)


class Department(Base):
    __tablename__ = "departments"

    dept_id = Column(Integer, primary_key=True, index=True)
    dept_name = Column(String(255), nullable=False)


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(100), nullable=False, unique=True)

    users = relationship("User", back_populates="role")


class Campus(Base):
    __tablename__ = "campuses"

    campus_id = Column(Integer, primary_key=True, index=True)
    campus_name = Column(String(255), nullable=False)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    role = relationship("Role", back_populates="users")
    agendas = relationship("Agenda", back_populates="creator")
    papers = relationship("Paper", back_populates="researcher")