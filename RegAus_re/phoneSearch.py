import re

fh = open("simpsons_phone_book.txt")
for line in fh:
	if re.search(r".",line):
		print line.rstrip()
fh.close()
