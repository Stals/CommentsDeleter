# Delets every char that follows a comment in that line
#TODO delete multi-line comments
#argv's should look like this:
# commentsDeleter.py -cpp "saveToDir" "file 1" "file 2" "ect..."
#TODO - auto. give a key depending on file extension
#TODO - all deletes comments for all the languages


#TODO Удаление должно происходить по тексту, а не по строкам, и нужно удалять всё что после комментария но до переноса на новую строку
# Это касается как сингл- так и мулти- лайн комментариев
# Пока есть идея только посимвольно копировать в строку, пока нет комментария, потом пропускать символы, до тех пор пока не будет \n
# А в мултилайн  -  до тех пор пока не найдётся закрывающий комментарий
# И на выходе функция выдаёт текст 

import sys
import os
languages = {"-cpp"    : [ '//', ('/*', '*/') ],
             "-java"   : [ '//', ('/*', '*/') ],
             "-delphi" : [ '//', ('{', '}') ],
             "-python" : [ '#',  ('"""', '"""') ],
             "-ruby"   : [ '#',  ('=begin', '=end') ]
}

flags = ["-auto", # gives a key depending on file extension
         "-all"]  # deletes comments for all the languages

#TODO  поддержка нескольких сингл-лайн комментариев для одного языка
def deleteSingleLineComments(text, singleComment):#TODO Rewrite coz this is veeeery bad solutuion for big files ( calles copy for the whole text for each comment )

	while singleComment in text :
		commentBeginIndex = text.find(singleComment)
		commentEndIndex = text.find('\n',commentBeginIndex)
		# copy  everything except commented text
		text = text[:commentBeginIndex]+text[commentEndIndex:]

	return text

#TODO  поддержка нескольких мульти-лайн комментариев для одного языка
def deleteMultiLineComments(text, comment):

	while (comment[0] in text) and (comment[1] in text) :
		commentBeginIndex = text.find(comment[0])
		commentEndIndex = text.find(comment[1], commentBeginIndex + len(comment[1]))
		# copy  everything except commented text
		text = text[:commentBeginIndex] + \
		       text[commentEndIndex + len(comment[1]):]


	return text

def main(): #TODO make separate functions for better understanding
	comments = [] #stores comments to delete
	files = [] #stores files that need to be cleaned
	if len(sys.argv) > 1:
		# Get comments and files
		if sys.argv[1][0] == '-':
			# If the first argument is a key (-cpp,-java,ect)
			files = sys.argv[2:]
			if sys.argv[1] in languages.keys():
				comments = languages[sys.argv[1]]
			else:
				print("Wrong Key\nKnown keys:")
				for language in languages:
					print (language)
				exit(0)
		else:
			files = sys.argv[1:]
			# Let user input comments in a console
			comments = [ input("Input single line comment:"),
					( input("Input begin of multi-line comment:"),
					  input("Input end if multi-line comment:") )]
			# Now we have "comments" to delete from "files"
		for filename in files:

			f = open(filename, 'r')
			text = f.read()
			f.close()

			newText = deleteSingleLineComments(text, comments[0])
			newText = deleteMultiLineComments(newText,comments[1])

			if not os.path.isdir("withoutComments"):
				os.mkdir("withoutComments")
			f = open("withoutComments\\" + filename, 'w')
			f.write(newText)
			f.close()

	else:
		#if no arguments were passed
		print("Expected: commentsDeleter.py -language 'saveToDir' 'file 1' 'file 2' 'ect...'")


if __name__ == '__main__':
	main()