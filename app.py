#imports
from flask import Flask , render_template, redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


#myapp
app=Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALECHEMY_TRACK_MODIFICATION"]=False
db=SQLAlchemy(app)

#Data class ~ row of data
class MyTask(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(100),nullable=False)
    complete=db.Column(db.Integer,default=0)
    created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"
with app.app_context():
        db.create_all()



#home page
@app.route("/",methods=["POST","GET"])
def index():
    #add a task
    if request.method=="POST":
        current_task=request.form['content']
        new_task=MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR : {e}")
            return f"ERROR : {e}"
    
    #see all current tasks
    else:
        tasks=MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html",tasks=tasks)
    
#https://www.home.com/pageone/2/task
#delete an item 
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task=MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()    
        return redirect("/")
    except Exception as e:
        return f"ERROR :{e}" 

#edit an item
@app.route("/edit/<int:id>",methods =["GET","POST"])
def edit(id:int):
    task=MyTask.query.get_or_404(id)
    if request.method=="POST":
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR :{e}"
    else:
        return render_template('edit.html',task=task)



#taaki flask is updating itself 
if __name__ == "__main__":
    app.run(debug=True)
