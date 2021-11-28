from flask import Flask, request, render_template, redirect, url_for 
import pymysql
import os

_HOSTNAME = 'colbert-mysql.mysql.database.azure.com'
_USERNAME = 'mikec@colbert-mysql'
_PASSWORD = 'eoO(i1J]ZkqC%f@vVGU?rH)'
_DBNAME = 'movie_data'
_SECRET_KEY = 'ABC123'

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(_USERNAME, _PASSWORD, _HOSTNAME,  _DBNAME)


conn = pymysql.connect(
        host = _HOSTNAME,
        user = _USERNAME, 
        password = _PASSWORD,
        db = _DBNAME,
        ssl={'ca': '/var/www/html/BaltimoreCyberTrustRoot.crt.pem'},
        cursorclass = pymysql.cursors.DictCursor)

"""        
conn = pymysql.connect(
    _HOSTNAME, 
    _USERNAME,
    _PASSWORD,
    _DBNAME,
    cursorclass=pymysql.cursors.DictCursor)
"""


application = Flask(__name__)
application.config['SECRET_KEY'] = _SECRET_KEY #os.environ.get('SECRET_KEY')

@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@application.route('/movie/<movie_id>', methods=['GET', 'POST'])
def movie_details(movie_id):
    cur = conn.cursor()
    query = "SELECT * FROM movies WHERE movieId = %s"
    cur.execute(query, movie_id)
    movie = cur.fetchone()
    return render_template('movie-details.html', movie=movie)

@application.route('/movies', methods=['GET'])
def movies():
    cur = conn.cursor()
    query = "SELECT * FROM movies"
    cur.execute(query)
    movies = cur.fetchall()
    return render_template('movies.html', movies=movies)

@application.route('/search', methods=['GET', 'POST'])
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
    application.run(debug=True)

