from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html', request=request)
	else:
		return "Goteem!"


@app.route('/test')
def create():
	return "Eyy a link!\n"