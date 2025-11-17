from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

favorites = db.Table(
    "favorites_peoples",
    Base.metadata,
    db.Column("users", db.ForeignKey("users.id")),
    db.Column("peoples", db.ForeignKey("peoples.id")),
)

favorites = db.Table(
    "favorites_planets",
    Base.metadata,
    db.Column("users", db.ForeignKey("users.id")),
    db.Column("peoples", db.ForeignKey("planets.id")),
)

favorites = db.Table(
    "favorites_films",
    Base.metadata,
    db.Column("users", db.ForeignKey("users.id")),
    db.Column("peoples", db.ForeignKey("films.id")),
)

favorites = db.Table(
    "favorites_vehicles",
    Base.metadata,
    db.Column("users", db.ForeignKey("users.id")),
    db.Column("peoples", db.ForeignKey("vehicles.id")),
)



class User(db.Model):
    __tablename__= "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(12), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(nullable=False)
    
    favorite_peoples: Mapped[List["People"]] = relationship(back_populates="user", secondary="favorites_peoples")

    favorite_vehicles: Mapped[List["Vehicle"]] = relationship(back_populates="user", secondary="favorites_vehicles")

    favorite_films: Mapped[List["Film"]] = relationship(back_populates="user", secondary="favorites_films")

    favorite_planet: Mapped[List["Planet"]] = relationship(back_populates="user", secondary="favorites_planets")



class People(db.Model):
    __tablename__= "peoples"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    gender: Mapped[str] = mapped_column(String(30), nullable=False)
    url: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    mass: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    create_date: Mapped[datetime] = mapped_column(nullable=False)
    

    user_id:Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    user: Mapped[List["User"]]= relationship(back_populates="favorite_peoples", secondary="favorites_peoples" )

class Vehicle(db.Model):
    __tablename__= "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    url: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    create_date: Mapped[datetime] = mapped_column(nullable=False)
    #falta la clave foranea de user

    user_id:Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    user: Mapped[List["User"]]= relationship(back_populates="favorite_vehicles", secondary="favorites_vehicles")

    
class Film(db.Model):
    __tablename__= "films"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    director: Mapped[str] = mapped_column(String(40), nullable=False)
    release_date: Mapped[datetime] = mapped_column(nullable=False)
    

    user_id:Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    user: Mapped[List["User"]]= relationship(back_populates="favorite_films", secondary="favorites_films")

class Planet(db.Model):
    __tablename__= "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    url: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    diameter: Mapped[int] = mapped_column(Integer, nullable=False)
    climate: Mapped[str] = mapped_column(String(30), nullable=False)
    create_date: Mapped[datetime] = mapped_column(nullable=False)
    

    user_id:Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    user: Mapped[List["User"]]= relationship(back_populates="favorite_planet", secondary="favorite_planets")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
