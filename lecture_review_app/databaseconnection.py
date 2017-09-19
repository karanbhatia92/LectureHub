import datetime
import random
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    user = Column(String, primary_key=True)
    user_type = Column(Integer)
    password = Column(String)

class Courses(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String)

class Lectures(Base):
    __tablename__ = 'lectures'
    course_id = Column(Integer, ForeignKey(Courses.course_id))
    lecture_id = Column(String, primary_key=True)
    lecture_name = Column(String)
    sentiment_total = Column(Float)
    rating_total = Column(Float)
    count = Column(Integer)

class Notes(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    notes = Column(String)
    user = Column(String, ForeignKey(Users.user))
    lecture_id = Column(String, ForeignKey(Lectures.lecture_id))

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lecture_id = Column(String, ForeignKey(Lectures.lecture_id))
    comment = Column(String)
    rating = Column(Integer)
    sentiment = Column(Float)
    user = Column(String, ForeignKey(Users.user))

def initialize():
    engine = create_engine(
        'postgresql://brh@mypgserver-brh:BigRedHacks2017@mypgserver-brh.postgres.database.azure.com:5432/postgres',
        echo=False)

    Base.metadata.create_all(engine)
    return engine

def add_lecture(engine, course_name, lecture_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    course = session.query(Courses).filter(Courses.course_name == course_name)
    # generating lecture id
    for c in course:
        # now = datetime.datetime.now()
        lecture_id = str(c.course_id)+str(random.sample(range(1, 100),1)[0])
        # lecture_id = str(c.course_id)+str(now.day)+str(now.month)+str(now.year)
        new_lecture = Lectures(course_id=c.course_id, lecture_id=lecture_id,
                               lecture_name=lecture_name, rating_total=0.0,
                               sentiment_total=0.0, count=0)
        session.add(new_lecture)
        session.commit()
        # print lecture_id
        return lecture_id

def login(engine, user, pwd):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(Users).filter(Users.user == user)
    # print user

    if user is None:
        return None
    else:
        for u in user:
            if u.password == pwd:
                return u.user_type
            else:
                return None

def valid_lecture_id(engine, lecture_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    id = session.query(Lectures).filter(Lectures.lecture_id == lecture_id).one_or_none()
    if id is None:
        return False
    else:
        return True

def submit_comment(engine, lecture_id, comment, rating,sentiment, user):
    Session = sessionmaker(bind=engine)
    session = Session()

    #enter in comments table
    new_comment = Comments(lecture_id=lecture_id, comment=comment,
                           rating=rating, sentiment=sentiment, user=user)
    session.add(new_comment)

    #enter in lectures table
    new_lecture = session.query(Lectures)\
        .filter(Lectures.lecture_id == lecture_id).one_or_none()

    current_rating = new_lecture.rating_total
    current_sentiment = new_lecture.sentiment_total
    current_count = new_lecture.count

    new_lecture.rating_total = rating+current_rating
    new_lecture.sentiment_total = sentiment+current_sentiment
    new_lecture.count = current_count+1
    session.commit()

def add_notes(engine, user, lecture_id, notes):
    Session = sessionmaker(bind=engine)
    session = Session()
    note = session.query(Notes).filter(Notes.user == user, Notes.lecture_id == lecture_id).one_or_none()
    if note is None:
        n = Notes(notes=notes, user=user, lecture_id=lecture_id)
        session.add(n)
    else:
        note.notes = notes
    session.commit()

def get_notes(engine, user, lecture_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    notes = session.query(Notes).filter(Notes.lecture_id == lecture_id, Notes.user == user)
    # print notes.notes
    for n in notes:
        return n.notes
    return ""

def retrieve_sentiment_students(engine, lecture_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(Comments.sentiment, func.count(Comments.user)).\
    filter(Comments.lecture_id == lecture_id).group_by(Comments.sentiment)
    ans = [["Sentiment", "No. of Students"]]
    for r in result:
        ans.append([float(r[0]), float(r[1])])
    return ans

def retrieve_rating_students(engine, lecture_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(Comments.rating, func.count(Comments.user))\
        .filter(Comments.lecture_id == lecture_id).group_by(Comments.rating)
    ans = [["Rating", "No. of Students"]]
    for r in result:
        ans.append([float(r[0]), float(r[1])])
    return ans

def retrieve_lecture_sentiment(engine, course_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    ans = [["Lecture","Avg. Sentiment"]]
    sentiments = session.query(Lectures).filter(Lectures.course_id == course_id)
    for s in sentiments:
        if s.count == 0:
            avg = 0
        else:
            avg = s.sentiment_total/s.count
        ans.append([s.lecture_name, avg])

    return ans

def retrieve_lecture_rating(engine, course_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    ans = [["Lecture", "Avg. Rating"]]
    sentiments = session.query(Lectures).filter(Lectures.course_id == course_id)
    for s in sentiments:
        if s.count == 0:
            avg = 0
        else:
            avg = s.rating_total/s.count
        ans.append([s.lecture_name, avg])

    return ans

def retrieve_catergories(engine,lecture_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    ans = {'one': [], 'two': [], 'three': [], 'four': [], 'five': []}
    result = session.query(Comments).filter(Comments.lecture_id == lecture_id)
    for r in result:
        if r.sentiment <= 0.2:
            ans['one'].append(r.comment)
        else:
            if r.sentiment <= 0.4:
                ans['two'].append(r.comment)
            else:
                if r.sentiment <= 0.6:
                    ans['three'].append(r.comment)
                else:
                    if r.sentiment <= 0.8:
                        ans['four'].append(r.comment)
                    else:
                        if r.sentiment <= 1:
                            ans['five'].append(r.comment)

    return ans

def get_lectures(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    ans = []
    lectures = session.query(Lectures)
    for l in lectures:
        dict = {'lecture_name': l.lecture_name, 'lecture_id': l.lecture_id}
        ans.append(dict)
    return ans
