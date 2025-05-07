import datetime
import random
import requests
import numpy as np
import math
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap

""" from flask_gravatar import Gravatar """
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BIGINT, NVARCHAR, String, TIMESTAMP, create_engine
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


engine=create_engine("sqlite://", echo=True)
login_manager = LoginManager()

class Base(DeclarativeBase):
    pass



db =SQLAlchemy(model_class=Base)




app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///students2.db"
login_manager.init_app(app)

app.secret_key="bnbn"


db.init_app(app)
class Student(db.Model, UserMixin):
    __tablename__="student_account"

    id:Mapped[int]=mapped_column(primary_key=True)
    mail:Mapped[str]=mapped_column(String(200), unique=True)
    name:Mapped[str]=mapped_column(String(100), unique=True)
    telephone:Mapped[str]=mapped_column(String(20), unique=True)
    gender:Mapped[str]=mapped_column(String(20))
    date:Mapped[str]
    university:Mapped[str]=mapped_column(String(200))
    password:Mapped[str]=mapped_column(String(1000))

class Comment(db.Model):

    __tablename__="comments"
    id:Mapped[int]=mapped_column(primary_key=True)
    text:Mapped[str]=mapped_column(String)
    user:Mapped[str]=mapped_column(String)
    target:Mapped[str]=mapped_column(String)
    public:Mapped[bool]
    liked:Mapped[bool]

class University(db.Model):

    __tablename__="universities"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String)
    url:Mapped[str]=mapped_column(String)
    progress:Mapped[int]=mapped_column(Integer)
    last_day:Mapped[int]=mapped_column(Integer)
    
class Notification(db.Model):

    __tablename__="notifications"
    id:Mapped[int]=mapped_column(primary_key=True)
    user:Mapped[str]=mapped_column(String)
    sender:Mapped[str]=mapped_column(String)
    message:Mapped[str]=mapped_column(String)

    




with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(Student).where(Student.id==user_id)).scalar()

@app.route("/")
def home():

    unis=db.session.execute(db.select(University)).scalars()
    for uni_toChange in unis:

        if datetime.date.weekday(datetime.date.today())==0:
            if uni_toChange.last_day==datetime.date.weekday(datetime.date.today()):
                pass
            else:
                uni_toChange.progress=random.randint(5,10)
                uni_toChange.last_day=datetime.date.weekday(datetime.date.today())
                db.session.commit()
        elif datetime.date.weekday(datetime.date.today())>0 and datetime.date.weekday(datetime.date.today())<=4:
            if uni_toChange.last_day==datetime.date.weekday(datetime.date.today()):
                pass
            else:
                uni_toChange.progress=random.randint(uni_toChange.progress,100)
                uni_toChange.last_day=datetime.date.weekday(datetime.date.today())
                db.session.commit()
        elif datetime.date.weekday(datetime.date.today())>4:
            if uni_toChange.last_day==datetime.date.weekday(datetime.date.today()):
                pass
            else:
                uni_toChange.progress=random.randint(0,5)
                uni_toChange.last_day=datetime.date.weekday(datetime.date.today())
                db.session.commit()

    if datetime.date.weekday(datetime.date.today())==4:
        unis=db.session.execute(db.select(University)).scalars()
        for uni_toChange in unis:
            if uni_toChange.progress>=80:
                users_published=db.session.execute(db.select(Student).where(Student.university==uni_toChange.name)).scalars()
                comments=db.session.execute(db.select(Comment)).scalars()
                for comment in comments:
                    for user in users_published:
                        if comment.user== user.name:
                            comment.public=True
                
                db.session.commit()





    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error=None
    if request.method=="POST":
        user=db.session.execute(db.select(Student).where(Student.mail==request.form["email"])).scalar()
        if (user):
            if request.form["password"]!=user.password:
                error="The password is not correct"
            elif request.form["password"]==user.password:
                currentId=str(user.id)
                login_user(user)
                flash('You were succesfully logged in')
                return redirect(url_for('home'))
        else:
            error="Invalid credentials, try again"

    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error=None
    if request.method=="POST":
        student_list=db.session.execute(db.select(Student))
        students_list=student_list.scalars()
        number=request.form["telephone"]
        unis=requests.get("https://raw.githubusercontent.com/Hipo/university-domains-list/refs/heads/master/world_universities_and_domains.json")
        sum=0
        for uni in unis.json():
            if(uni["country"]=="Spain"):
                if(uni["name"])==request.form["university"]:
                    sum+=1


        for element in students_list:
            if(element.name)==request.form["username"]:
                error="The username is already taken"
            elif(element.mail)==request.form["email"] or (not "@" in request.form["email"]):
                error="The mail is already taken or not valid"
            elif(element.telephone)==request.form["telephone"] or (not number.isdigit()):
                error="The telephone is not valid or already taken"
            elif(len(request.form["password"])<8):
                error="Password is too short"
            elif (request.form["password"]!=request.form["pin-2"]):
                error="Password does not match"
            elif (sum==0):
                error="Please insert a valid university name"
        if(error==None):
            student=Student(
                mail=request.form["email"],
                name=request.form["username"],
                telephone=request.form["telephone"],
                gender=request.form["gender"],
                date=request.form["date"],
                university=request.form["university"],
                password=request.form["password"]
                )
            db.session.add(student)
            db.session.commit()
            user=db.session.execute(db.select(Student).where(Student.mail==request.form["email"])).scalar()
            if (user):
                login_user(user)
            return redirect(url_for("home"))

    return render_template("register.html", error=error)

@app.route("/collaborators")
def collaborators():

    
    uni_data=requests.get("https://raw.githubusercontent.com/Hipo/university-domains-list/refs/heads/master/world_universities_and_domains.json")

  
    """for uni in uni_data.json():
                if(uni["country"]=="Spain"):
                    uni_item=University(
                        name=uni["name"],
                        url=uni["web_pages"][0],
                        progress=0,
                        last_day=0
                    )
                    db.session.add(uni_item)
                    db.session.commit()"""  
    return render_template("collaborators.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/user", methods=["GET", "POST"])
def user():

    """ if request.method=="POST":
        logout_user()
        return redirect(url_for("home"))  """
    error=None
    comment_list=db.session.execute(db.select(Comment).where(Comment.target==current_user.name))
    comments=comment_list.scalars()
    
    users_list=db.session.execute(db.select(Student))
    users=users_list.scalars()
    if request.method=="POST":
        for user in users:
            if user.name!=request.form["target"]:
                error="Type a valid target-user name"
            else:
                error=None
                break
        if error==None:
            comment=Comment(
                user=current_user.name,
                target=request.form["target"],
                text=request.form["message"],
                public=False,
                liked=False
            )
            db.session.add(comment)
            db.session.commit()

    """  if datetime.date.weekday(datetime.date.today())==0:
        uni=db.session.execute(db.select(University).where(University.name==current_user.university))
        uni_toChange=uni.scalar()
        if uni_toChange.last_day==datetime.date.weekday(datetime.date.today()):
            pass
        else:
            uni_toChange.progress=random.randint(0,10)
            uni_toChange.last_day=datetime.date.weekday(datetime.date.today())
            db.session.commit()
    elif datetime.date.weekday(datetime.date.today())>0 and datetime.date.weekday(datetime.date.today())<=4:
        uni=db.session.execute(db.select(University).where(University.name==current_user.university))
        uni_toChange=uni.scalar()
        if uni_toChange.last_day==datetime.date.weekday(datetime.date.today()):
            pass
        else:
            uni_toChange.progress=random.randint(uni_toChange.progress,100)
            uni_toChange.last_day=datetime.date.weekday(datetime.date.today())
            db.session.commit()
    elif datetime.date.weekday(datetime.date.today())>4:
        uni=db.session.execute(db.select(University).where(University.name==current_user.university))
        uni_toChange=uni.scalar()
        if uni_toChange.last_day==datetime.date.weekday(datetime.date.today()):
            pass
        else:
            uni_toChange.progress=0
            uni_toChange.last_day=datetime.date.weekday(datetime.date.today())
            db.session.commit()

    if datetime.date.weekday(datetime.date.today())==4:
        uni=db.session.execute(db.select(University).where(University.name==current_user.university))
        uni_toChange=uni.scalar()
        if uni_toChange.progress>=80:
            users_published=db.session.execute(db.select(Student).where(Student.university==current_user.university)).scalars()
            comments=db.session.execute(db.select(Comment)).scalars()
            for comment in comments:
                for user in users_published:
                    if comment.user== user.name:
                        comment.public=True
            
            db.session.commit() """


    uni=db.session.execute(db.select(University).where(University.name==current_user.university))
    uni_toChange=uni.scalar()

    info_toPass={
        "weekday":datetime.date.today(),
        "progress":uni_toChange.progress
    }

    notifs_list=db.session.execute(db.select(Notification).where(Notification.user==current_user.name))
    notifs=notifs_list.scalars()
    
    return render_template("user.html", users=users, comments=comments, error=error, date=info_toPass, notifs=notifs)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/publish")
def publish():
    comments=db.session.execute(db.select(Comment)).scalars()
    for comment in comments:
        comment.public=True
    
    db.session.commit()
    return redirect(url_for("user"))

@app.route("/like/<com_id>", methods=["GET", "POST"])
def like(com_id):
    comment_toLike=db.session.execute(db.select(Comment).where(Comment.id==com_id)).scalar()
    comment_toLike.liked=True

    user_liked=db.session.execute(db.select(Student).where(Student.name==comment_toLike.user)).scalar()
    user_sender=db.session.execute(db.select(Student).where(Student.name==comment_toLike.target)).scalar()
    
    notification=Notification(
        user=user_liked.name,
        sender=user_sender.name,
        message=comment_toLike.text
    )

    db.session.add(notification)

    db.session.commit()


    return redirect(url_for("user"))

@app.route("/delete-notif/<notif_id>", methods=["GET", "POST"])
def delete_notif(notif_id):
    notif_toDelete=db.session.execute(db.delete(Notification).where(Notification.id==notif_id))
    db.session.commit()
    return redirect(url_for("user"))


if __name__=="__main__":
    app.run(debug=True, port=5002)




