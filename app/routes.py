from app import app
from flask import render_template

from flask_login import login_required

@app.route('/oldhome')
def home():
    my_list = ['Shoha',"Josh", 'Dylan','Nicole']
    my_second_list = sorted(my_list)
    return render_template('index.html', my_title = "This is the HOME page", name='Shoha', my_list = my_second_list)

@app.route('/about')
@login_required
def iCanNameThisAnything():
    return render_template('about.html', my_title = "aBoUt")

@app.route('/testing')
def test():
    return {'hi':'there'}

@app.route('/new/api')
def test2():
    return {'students':[
        {
            "first_name": 'William',
            "last_name": 'B'
        },
        {
            "first_name": 'Asher',
            "last_name": 'C'
        },
        {
            "first_name": 'Shouwang',
            "last_name": 'H'
        },
        {
            "first_name": 'Matias',
            "last_name": 'N'
        },
        {
            "first_name": 'Samantha',
            "last_name": 'M'
        },
        {
            "first_name": 'John',
            "last_name": 'B'
        },
        {
            "first_name": 'Iwona',
            "last_name": 'M'
        },
        {
            "first_name": 'Allan',
            "last_name": 'E'
        },
        {
            "first_name": 'Alex',
            "last_name": 'E'
        }
    ]}