from flask import Flask, render_template, request, redirect
from hashids import Hashids
import sqlite3
app = Flask(__name__)

hashids = Hashids(salt="why so salty")

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		# Retrieve redirect destination
		dest = request.form.get("destination")

		# Connect to databse and create cursor
		conn = sqlite3.connect('test.db')
		db_cursor = conn.cursor()

		# Insert new link into databse, and commit change
		db_cursor.execute("INSERT INTO links (dest) VALUES (?)", (dest,))
		conn.commit()

		# Build hash id from link's DB id number
		link_id = db_cursor.lastrowid
		link_hash = hashids.encode(link_id)

		# Add hash id to link and update 
		db_cursor.execute("UPDATE links SET short=? WHERE id=?",(link_hash,link_id))
		conn.commit()
		conn.close()

		short_link = "/" + link_hash

		return render_template('index.html', short_link=short_link)
	else:
		return render_template('index.html')

@app.route('/<link_hash>')
def redir(link_hash):
	# Decode the shortlink and find the item in the db!
	link_id = hashids.decode(link_hash)[0]
	print("Incoming hash:",link_hash,"has been decoded to id:",link_id)
	conn = sqlite3.connect('test.db')
	db_cursor = conn.cursor()
	dest_link = db_cursor.execute("SELECT * FROM links WHERE id=?",(link_id,)).fetchone()[1]
	print("Short link found! Redirecting to: ", dest_link)
	return redirect(dest_link, code=308,)
	
