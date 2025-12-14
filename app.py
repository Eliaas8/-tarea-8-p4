from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail
from config import Config
from celery_app import make_celery
from tasks import send_email_task

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
celery = make_celery(app)

books = []

@app.route('/')
def index():
    return render_template('books.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book = {
            'id': len(books) + 1,
            'title': request.form['title'],
            'author': request.form['author']
        }
        books.append(book)

        send_email_task.delay('Libro agregado', book['title'])
        flash('Libro agregado. Correo enviado de forma asíncrona.', 'success')
        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)

    if not book:
        flash('Libro no encontrado', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        books.remove(book)
        send_email_task.delay('Libro eliminado', book['title'])
        flash('Libro eliminado. Correo enviado de forma asíncrona.', 'success')
        return redirect(url_for('index'))

    return render_template('delete_book.html', book=book)

if __name__ == '__main__':
    app.run()
