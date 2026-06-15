from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import click
import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

def create_app():
    app=Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py',silent=True)
    app.config.from_mapping(SECRET_KEY='Dev')
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///event_datbase.db'

    class Base(DeclarativeBase):
        pass

    db=SQLAlchemy(model_class=Base)
    db.init_app(app)

    class Event(db.Model):
        date=db.mapped_column(db.String, primary_key=True)
        event_name=db.mapped_column(db.String(200),nullable=False)
    
    @click.command('init-db')
    def init_db_command():
        with app.app_context():
            db.create_all()
            click.echo("intialized th database")
            
    app.cli.add_command(init_db_command)

    @app.route('/',methods=['GET','POST'])
    def home():
        if request.method=='POST':
            db.session.add(Event(date=datetime.datetime.now().__str__(),
                                 event_name=request.form['eventBox']))
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('home.html', eventLists=db.session.execute(db.select(Event).order_by(Event.date)).scalars())
    return app
if __name__=='__main__':
    app=create_app()
    app.run()
        

        

        
    