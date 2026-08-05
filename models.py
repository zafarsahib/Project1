from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


db = SQLAlchemy()


class User(
    UserMixin,
    db.Model
):

    __tablename__ = "users"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )


    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )


    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


    pets = db.relationship(
        "Pet",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )


    def set_password(
        self,
        password
    ):

        self.password_hash = generate_password_hash(
            password
        )


    def check_password(
        self,
        password
    ):

        return check_password_hash(
            self.password_hash,
            password
        )


    def to_dict(self):

        return {

            "id": self.id,

            "username": self.username,

            "email": self.email

        }


class Pet(db.Model):

    __tablename__ = "pets"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    name = db.Column(
        db.String(100),
        nullable=False
    )


    species = db.Column(
        db.String(50),
        nullable=False
    )


    breed = db.Column(
        db.String(100),
        nullable=False
    )


    age = db.Column(
        db.Integer,
        nullable=False
    )


    gender = db.Column(
        db.String(20),
        nullable=False
    )


    description = db.Column(
        db.String(1000),
        nullable=True
    )


    status = db.Column(
        db.String(30),
        nullable=False,
        default="Available"
    )


    image = db.Column(
        db.String(255),
        nullable=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    def to_dict(self):

        return {

            "id": self.id,

            "name": self.name,

            "species": self.species,

            "breed": self.breed,

            "age": self.age,

            "gender": self.gender,

            "description": self.description,

            "status": self.status,

            "image": self.image,

            "user_id": self.user_id

        }