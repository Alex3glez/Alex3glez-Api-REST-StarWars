from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from datetime import datetime, timezone
from typing import List


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

favorites_peoples = db.Table(
    "favorites_peoples",
    Base.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey(
        "users.id"), nullable=False),
    db.Column("people_id", db.Integer, db.ForeignKey(
        "peoples.id"), nullable=False),
)

favorites_planets = db.Table(
    "favorites_planets",
    Base.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey(
        "users.id"), nullable=False),
    db.Column("planet_id", db.Integer, db.ForeignKey(
        "planets.id"), nullable=False),
)

favorites_films = db.Table(
    "favorites_films",
    Base.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey(
        "users.id"), nullable=False),
    db.Column("film_id", db.Integer, db.ForeignKey(
        "films.id"), nullable=False),
)

favorites_vehicles = db.Table(
    "favorites_vehicles",
    Base.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey(
        "users.id"), nullable=False),
    db.Column("vehicle_id", db.Integer, db.ForeignKey(
        "vehicles.id"), nullable=False),
)


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(60), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(12), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))

    favorite_peoples: Mapped[List["People"]] = relationship(
        back_populates="user", secondary="favorites_peoples")

    favorite_vehicles: Mapped[List["Vehicle"]] = relationship(
        back_populates="user", secondary="favorites_vehicles")

    favorite_films: Mapped[List["Film"]] = relationship(
        back_populates="user", secondary="favorites_films")

    favorite_planets: Mapped[List["Planet"]] = relationship(
        back_populates="user", secondary="favorites_planets")

    @classmethod
    def create_user(self, username, email, password, name, last_name):
        user = self(username=username, email=email,
                    password=password, name=name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        return user

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "subscription_date": self.subscription_date}


class People(db.Model):
    __tablename__ = "peoples"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    gender: Mapped[str] = mapped_column(String(30), nullable=False)
    url: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    mass: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))

    user: Mapped[List["User"]] = relationship(
        back_populates="favorite_peoples", secondary="favorites_peoples")

    @classmethod
    def create_people(self, gender, url, mass, name, height):
        people = self(gender=gender, url=url, mass=mass,
                      name=name, height=height)

        db.session.add(people)
        db.session.commit()

        return people

    def to_dict(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "url": self.url,
            "name": self.name,
            "create_date": self.create_date,
            "mass": self.mass,
            "height": self.height}


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    url: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))

    user: Mapped[List["User"]] = relationship(
        back_populates="favorite_vehicles", secondary="favorites_vehicles")


class Film(db.Model):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    director: Mapped[str] = mapped_column(String(40), nullable=False)
    release_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))

    user: Mapped[List["User"]] = relationship(
        back_populates="favorite_films", secondary="favorites_films")


class Planet(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    url: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    diameter: Mapped[int] = mapped_column(Integer, nullable=False)
    climate: Mapped[str] = mapped_column(String(30), nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))

    user: Mapped[List["User"]] = relationship(
        back_populates="favorite_planets", secondary="favorites_planets")

    @classmethod
    def create_planet(self, population, url, diameter, name, climate):
        planet = self(population=population, url=url,
                      diameter=diameter, name=name, climate=climate)

        db.session.add(planet)
        db.session.commit()

        return planet

    def to_dict(self):
        return {
            "id": self.id,
            "population": self.population,
            "url": self.url,
            "name": self.name,
            "create_date": self.create_date,
            "climate": self.climate}
