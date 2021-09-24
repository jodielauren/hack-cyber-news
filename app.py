from os import sendfile
import sqlite3
from sqlite3.dbapi2 import version
from flask import Flask, render_template, request, url_for, flash, redirect, send_file, Response
from werkzeug.exceptions import abort
# import xml.etree
import xml.etree.ElementTree as ET

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/rss.xml')
def rss():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    # return send_file("testfile.xml")

    rss = createEmptyFeed()    
    channel = rss.find("channel")
    for rsspost in posts:
        item = ET.SubElement(channel, "item")
        createChildElem(item, "title", rsspost['title'])
        createChildElem(item, "content", rsspost['content'])
        createChildElem(item, "link", rsspost['url'])
        createChildElem(item, "category", rsspost['category'])


    data = ET.tostring(rss, encoding='UTF-8', method='xml', xml_declaration=True)
    r = Response(response=data, status=200, mimetype="application/xml")
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    return r

def createEmptyFeed():
    comment = ET.Comment('Hackathon 2021')
    rss = ET.Element("rss", version="2.0")
    rss.append(comment)

    channel = ET.SubElement(rss, "channel")
    createChildElem(channel, "title", "Ashley Test")
    createChildElem(channel, "link", "www.test.com")
    createChildElem(channel, "copyright", "ImmersiveLabs")
    createChildElem(channel, "lastBuildDate", "24th Sepetember 2021")
    createChildElem(channel, "ttl", "40")
    return rss

def createChildElem(parent, block, text):
    elem = ET.SubElement(parent, block)
    elem.text = text

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        url = request.form['url']
        category = request.form['category']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content, url, category) VALUES (?, ?, ?, ?)',
                         (title, content, url, category))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        url = request.form['url']
        category = request.form['category']

  
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?, url = ?, category = ?'
                         ' WHERE id = ?',
                         (title, content, url, category, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/search', methods=('POST', 'GET'))
def search():
    search_item = request.form['search']
    print(f"User has searched for {search_item}")

    conn = get_db_connection()
    posts = conn.execute(
      "SELECT * FROM posts WHERE content LIKE ? ",
      ('%'+ search_item +'%',)).fetchall()
    conn.commit()
    conn.close()

    print(posts)
    # return "hello"
    return render_template('search.html', posts=posts)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)