from flask import Flask, request, render_template, redirect, url_for 
import pymysql
import os

conn = pymysql.connect(
        host = os.environ.get('DBHOSTNAME'),
        user = os.environ.get('DBUSERNAME'),
        password = os.environ.get('DBPASSWORD'),
        db = os.environ.get('DBNAME'), 
        ssl={'ca': './BaltimoreCyberTrustRoot.crt.pem'},
        cursorclass = pymysql.cursors.DictCursor)  

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/movie/<movie_id>', methods=['GET', 'POST'])
def movie_details(movie_id):
    cur = conn.cursor()
    query = "SELECT * FROM movies WHERE movieId = %s"
    cur.execute(query, movie_id)
    movie = cur.fetchone()
    return render_template('movie-details.html', movie=movie)

@app.route('/movies', methods=['GET'])
def movies():
    cur = conn.cursor()
    query = "SELECT * FROM movies"
    cur.execute(query)
    movies = cur.fetchall()
    return render_template('movies.html', movies=movies)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        cur = conn.cursor()
        query = "SELECT * FROM movies WHERE title LIKE %(search)s OR releaseYear LIKE %(search)s"
        param_dict = { "search": '%' + search_value + '%' }
        cur.execute(query, param_dict)
        if cur.rowcount > 0:
            results = cur.fetchall()
            return render_template('movies.html', movies=results)
        else:
            return render_template('movies.html', no_match="No matches found for your search.")
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

