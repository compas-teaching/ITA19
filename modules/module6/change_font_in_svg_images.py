import os

path = os.path.dirname(__file__)
images_folder = os.path.join(path, "images")

for file in os.listdir(images_folder):
	print(file)
	name, ext = os.path.splitext(file)
	if ext == '.svg':
		fullfilename = os.path.join(images_folder, file)
		with open(fullfilename, 'r') as f:
			data = f.read()

		txt_old = []
		txt_new = []

		txt_old.append("font-family:'Roboto-Regular';")
		txt_new.append("font-family:'Roboto';")

		txt_old.append("<style type=\"text/css\">\n\t.")
		txt_new.append("<style type=\"text/css\">\n\t@import url('https://fonts.googleapis.com/css?family=Roboto');\n\t.")

		for old, new in zip(txt_old, txt_new):
			if data.find(old) != -1:
				data = data.replace(old, new)

		with open(fullfilename, 'w') as f:
			f.write(data)