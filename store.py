from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql
import datetime

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


@post('/category')
def create_category():
	try:
		with connection.cursor() as cursor:
			name = request.POST.get('name')
			sql = "INSERT INTO CATEGORIES(name) VALUES('" + name + "');"
			cursor.execute(sql)
			id = cursor.lastrowid
			connection.commit()
			return json.dumps({
				'STATUS': 'SUCCESS',
				'CAT_ID': id,
				'CODE': 201
			})
	# except InternalError:
	# 	return json.dumps({
	# 	'STATUS': 'ERROR',
	# 	'MSG': 'Internal Error',
	# 	'CODE': 500
	# 	})
	except Exception as e:
		return json.dumps({
			'STATUS': 'ERROR',
			'MSG': repr(e)
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


@delete('/category/<id>')
def del_category(id):
	try:
		with connection.cursor() as cursor:
			sql = "DELETE FROM CATEGORIES WHERE id='" + id + "';"
			cursor.execute(sql)
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

@get('/product/<id>')
def get_product_by_id(id):
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM PRODUCTS WHERE id='" + id + "';"
			cursor.execute(sql)
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
			sql = "SELECT * FROM CATEGORIES AS c LEFT JOIN PRODUCTS AS p ON c.id = p.category WHERE c.id='" + id + "';"
			cursor.execute(sql)
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
