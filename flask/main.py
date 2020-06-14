from flask import Flask,render_template
app = Flask(__name__)

posts = [
    { 
        'author':'Leo Leung',
        'title':'Blog Post 1',
        'content':'life is good',
        'date_posted': 'April 28,2018',
    },
    { 
        'author':'Leo Leung',
        'title':'Blog Post 2',
        'content':'life is bad',
        'date_posted': 'May 1,2020',
    },
]

@app.route('/')
@app.route('/home')
def hello():
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title="About")

if __name__ == '__main__':
    app.run(debug=True)
