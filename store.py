from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

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
			sql = "INSERT INTO CATEGORIES(name) VALUES();"
			cursor.execute(sql)
			connection.commit()
			id = cursor.lastrowid
			return json.dumps({
				'STATUS': 'SUCCESS',
				'CAT_ID': id,
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
			'CODE': {
				200: 'Success',
			}
		})
	except Exception as e:
		return json.dumps({
			'STATUS': 'ERROR',
			'MSG': repr(e),
			'CODE': 500
		})

# @get('/category/<id>/products')
# def get_products_by_id(id):
# 	return ({
# 	'STATUS': {
# 		'SUCCESS': 'categories fetched',
# 		'ERROR': 'internal error'
# 		},
# 		'MSG': 'internal error',
# 		'PRODUCTS': [],
# 		'CODE': {
# 			200: 'Success',
# 			404: 'category not found',
# 			500: 'internal error'
# 		}
# 	})


@get('/products')
def get_products():
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM PRODUCTS;"
			cursor.execute(sql)
			result = cursor.fetchall()
		return json.dumps({
			'STATUS': 'SUCCESS',
			'CATEGORIES': result,
			'CODE': {
				200: 'Success',
			}
		})
	except Exception as e:
		return json.dumps({
			'STATUS': 'ERROR',
			'MSG': repr(e),
			'CODE': 500
		})

run(host='0.0.0.0', port=argv[1])
