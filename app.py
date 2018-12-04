from flask import Flask, jsonify, abort, render_template, make_response, request
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from books import books
from credentials import USERNAME, PASSWORD

app = Flask(__name__)

@app.route("/")
def home():
    # Flask will look for templates in the templates folder.
    return render_template('home_extend.html')

@app.route("/about")
def about():
    return render_template('about_extend.html')

@app.route("/contact")
def contact():
		return render_template('contact.html')

@app.route("/portfolio")
def portfolio():
		return render_template('portfolio.html')


@app.route('/api/books', methods=['GET'])
@auth.login_required
def get_books():
		return jsonify({'books': books})

@app.route('/api/books/<int:id>', methods=['GET'])
@auth.login_required
def get_book(id):
		book = [book for book in books if book['id'] == id]
		if len(book) == 0:
			return make_response(jsonify({'error': 'Book not found'}), 404)
		return jsonify({'books': book[0]})

@app.route('/api/books', methods=['POST'])
def add_book():
		if not request.json or not 'title' in request.json or not 'author' in request.json:
			abort(400)
		book = {
			'id' : books[-1]['id'] + 1,
			'title': request.json['title'],
			'author': request.json['author']
		}
		books.append(book)
		return jsonify({'book': book}), 201

@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
		book = [book for book in books if book['id'] == id]
		if len(book) == 0:
			abort(404)
		if not request.json:
			abort(400)
		if 'title' in request.json and type(request.json['title']) is not str:
			abort(400)
		if 'author' in request.json and type(request.json['author']) is not str:
			abort(400)
		book[0]['title'] = request.json.get('title', book[0]['title'])
		book[0]['author'] = request.json.get('author', book[0]['author'])
		return jsonify({'book': book[0]})

@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
	book = [book for book in books if book['id'] == id]
	if len(book) == 0:
		abort(404)
	books.remove(book[0])
	return jsonify({'message': 'Deleted ' + str(book[0]['title'] + ' by ' + str(book[0]['author']))})

@app.errorhandler(404)
def page_not_found(err):
		return render_template('404.html'), 404

@auth.get_password
def get_password(username):
		if username == USERNAME:
			return PASSWORD
		return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 403)

if __name__ == '__main__':
	app.run(debug=True)