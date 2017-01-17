# -- coding: utf-8 --
import extract
import os.path
import sqlite3 as sql
import sys
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from flask import Flask, render_template, request, send_from_directory
#from tesseract import image_to_string

__author__ = 'ibininja'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
	return render_template('upload.html')

@app.route('/upload', methods = ['POST','GET'])
def upload():
	i = 0
	time = datetime.now()
	target = os.path.join(APP_ROOT, 'images/')
	#print(target)

	def clean_image(file, filename):
		output_image = None
		openCV_images = os.path.join(APP_ROOT, 'outputs/')
		if not os.path.isdir(openCV_images):
			os.mkdir(openCV_images)
		# output_image = ''.join([openCV_images, filename])
		for x in xrange(1,2):
			if output_image is None:
				output_image = ''.join([openCV_images, filename])
				extract.ext(file, output_image)
			else:
				extract.ext(output_image, output_image)
		# im = Image.open(file)
		# im = im.filter(ImageFilter.MedianFilter())
		# enhancer = ImageEnhance.Contrast(im)
		# im = enhancer.enhance(4)
		# im = im.convert('1')
		# im.save(output_image)

		return output_image


	if not os.path.isdir(target):
		os.mkdir(target)

	for file in request.files.getlist("file"):
		#print(file)
		filename = file.filename #Name of the file
		destination = "/".join([target,filename])
		#print(destination)
		file.save(destination)

		# Refence  the output image
		im = Image.open(clean_image(destination, filename))
		i = pytesseract.image_to_string(im)

		#Inserting the record

		with sql.connect('platNum.db') as con:
			cur = con.cursor()
			cur.execute("INSERT INTO platenumber(fileName,textExtracted,timeIn,timeOut) VALUES (?,?,?,?)", (filename.decode('utf-8'),i.decode('utf-8'),time,time) )

			con.commit()
			msg = "Record successfully added"

		
	return render_template("view.html", answer = i)

@app.route("/list")
def list():
	con = sql.connect('platNum.db')
	con.row_factory = sql.Row

	cur = con.cursor()
	cur.execute("SELECT * FROM platenumber")

	rows = cur.fetchall();
	return render_template("view.html",rows = rows)


if __name__  == "__main__":
	app.run(debug = True, host='0.0.0.0')
