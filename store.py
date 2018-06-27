from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql
import datetime
import time

connection = pymysql.connect(host='localhost',
						  user='root',
						  password='root',
						  db='store_adv',
						  charset='utf8',
						  cursorclass=pymysql.cursors.DictCursor)

@get("/admin")
def admin_portal():
	return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@get('/get_store_name')
def get_store_name():
	try:
		with connection.cursor() as cursor:
			sql = "SELECT name FROM STORE_NAME"
			cursor.execute(sql)
			result = cursor.fetchone()
		return json.dumps({
			'STATUS': 'SUCCESS',
			'STORE_NAME': result,
			'CODE': 200
		})
	except Exception as e:
		return json.dumps({
			'STATUS': 'ERROR',
			'MSG': repr(e),
			'CODE': 500
		})

@post('/update_store_name')
def update_store_name():
	try:
		store_name = request.POST.get('storeName')
		email = request.POST.get('email')
		with connection.cursor() as cursor:
			sql = "UPDATE STORE_NAME set name=%s, email=%s;"
			cursor.execute(sql, (store_name, email))
			connection.commit()
			return json.dumps({
				'STATUS': 'SUCCESS',
				'CODE': 201
			})
	except Exception as e:
		return json.dumps({
			'STATUS': 'ERROR',
			'MSG': repr(e),
			'CODE': 500
		})


@post('/category')
def create_category():
	try:
		name = request.POST.get('name')
		with connection.cursor() as cursor:
			sql = "INSERT INTO CATEGORIES(name) VALUES(%s);"
			cursor.execute(sql, (name))
			connection.commit()
			return json.dumps({
				'STATUS': 'SUCCESS',
				'CAT_ID': cursor.lastrowid,
				'CODE': 201
			})
	except Exception as e:
		return json.dumps({
			'STATUS': 'ERROR',
			'MSG': repr(e),
			'CODE': 500
		})


@delete('/category/<id>')
def del_category(id):
	try:
		with connection.cursor() as cursor:
			sql = "DELETE FROM CATEGORIES WHERE id=%s;"
			cursor.execute(sql, (id))
			connection.commit()
			return json.dumps({
				'STATUS': 'SUCCESS',
				'CODE': 201
			})
	except Exception as e:
		return json.dumps({
			'STATUS': 'ERROR',
			'MSG': repr(e),
			'CODE': 500
		})


@get('/categories')
def get_categories():
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM CATEGORIES;"
			cursor.execute(sql)
			result = cursor.fetchall()
		return json.dumps({
			'STATUS': 'SUCCESS',
			'CATEGORIES': result,
			'CODE':200
		})
	except Exception as e:
		return json.dumps({
			'STATUS': 'ERROR',
			'MSG': repr(e),
			'CODE': 500
		})


@post('/product')
def add_product():
	category = request.POST.get('category')
	price = request.POST.get('price')
	title = request.POST.get('title')
	desc = request.POST.get('desc')
	img_url = request.POST.get('img_url')
	favorite = request.POST.get('favorite')
	id = request.POST.get('id')
	if favorite is None:
		favorite = 0
	else:
		favorite = 1
	try:
		with connection.cursor() as cursor:
			if id:
				sql = "UPDATE PRODUCTS SET category=%s, price=%s, title=%s, description=%s, img_url=%s, favorite=%s WHERE id=%s"
				cursor.execute(sql, (category, price, title, desc, img_url, favorite, id))
			else:
				sql = "INSERT INTO PRODUCTS(category, price, title, description, img_url, favorite, date_created) VALUES(%s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(sql, (category, price, title, desc, img_url, favorite, time.strftime('%Y-%m-%d')))
			connection.commit()
			return json.dumps({
				'STATUS': 'SUCCESS',
				'PRODUCT_ID': cursor.lastrowid,
				'CODE': 201
			})
	except Exception as e:
		return json.dumps({
		'STATUS': 'ERROR',
		'MSG': repr(e),
		'CODE': 500
		})


@get('/product/<id>')
def get_product_by_id(id):
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM PRODUCTS WHERE id=%s;"
			cursor.execute(sql, (id))
			result = cursor.fetchone()
			return json.dumps({
				'STATUS': 'SUCCESS',
				'PRODUCTS': result,
				'CODE': {
				200: 'Success',
			}
		}, default=str)
	except Exception as e:
		return json.dumps({
		'STATUS': 'ERROR',
		'MSG': repr(e),
		'CODE': 500
		})


@delete('/product/<id>')
def delete_product(id):
	try:
		with connection.cursor() as cursor:
			sql = "DELETE FROM PRODUCTS WHERE id=%s;"
			cursor.execute(sql, (id))
			connection.commit()
			return json.dumps({
				'STATUS': 'SUCCESS',
				'CODE': 201
			})
	except Exception as e:
		return json.dumps({
			'STATUS': 'ERROR',
			'MSG': repr(e),
			'CODE': 500
		})


@get('/products')
def get_products():
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM PRODUCTS;"
			cursor.execute(sql)
			result = cursor.fetchall()
		return json.dumps({
			'STATUS': 'SUCCESS',
			'PRODUCTS': result,
			'CODE': {
				200: 'Success',
			}
		}, default=str)
	except Exception as e:
		return json.dumps({
			'STATUS': 'ERROR',
			'MSG': repr(e),
			'CODE': 500
		})


@get('/category/<id>/products')
def get_products_by_id(id):
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM CATEGORIES AS c LEFT JOIN PRODUCTS AS p ON c.id = p.category WHERE c.id=%s ORDER BY p.favorite desc, date_created;"
			cursor.execute(sql, (id))
			result = cursor.fetchall()
			return json.dumps({
				'STATUS': 'SUCCESS',
				'PRODUCTS': result,
				'CODE': 200
			}, default=str)
	except Exception as e:
		return json.dumps({
			'STATUS': 'ERROR',
			'MSG': repr(e),
			'CODE': 500
		})


run(host='0.0.0.0', port=argv[1])
