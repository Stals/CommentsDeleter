# Delets every char that follows a comment in that line
# argv's should look like this:
# commentsDeleter.py -cpp "saveToDir" "file 1" "file 2" "ect..."
#TODO - auto.
#TODO - all Когда сделаю поддержку нескольких вариантов комментариев для мультилйна и синглайна  - когда выбирают -all , нужно создать comments сложа все комментарии для других языков


#TODO Удаление должно происходить по тексту, а не по строкам, и нужно удалять всё что после комментария но до переноса на новую строку
# Это касается как сингл- так и мулти- лайн комментариев
# Пока есть идея только посимвольно копировать в строку, пока нет комментария, потом пропускать символы, до тех пор пока не будет \n
# А в мултилайн  -  до тех пор пока не найдётся закрывающий комментарий
# И на выходе функция выдаёт текст 

import sys
import os
#TODO подумать о переназвании languages и comments

#TODO also add file extension for each language
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
		text = text[:commentBeginIndex] + text[commentEndIndex:]
	return text

#TODO  поддержка нескольких мульти-лайн комментариев для одного языка
def deleteMultiLineComments(text, comment):
	#
	while (comment[0] in text) and (comment[1] in text) :
		commentBeginIndex = text.find(comment[0])
		commentEndIndex = text.find(comment[1], commentBeginIndex + len(comment[1]))
		# copy  everything except commented text
		text = text[:commentBeginIndex] + \
		       text[commentEndIndex + len(comment[1]):]
	return text


def getTextFromFile(filename):
	f = open(filename, 'r')
	text = f.read()
	f.close()
	return text


def saveTextToFile(dirName, filename, text):
	if not os.path.isdir(dirName):
		#if directory does not exist - create it
		os.mkdir(dirName)
	f = open(dirName + "\\" + filename, 'w')
	f.write(text)
	f.close()


def getCommentsFromUser():
	singleLineComment = input("Input single line comment:")
	multiLineCommentBegin = input("Input begin of multi-line comment:")
	multiLineCommentEnd = input("Input end if multi-line comment:")
	return [singleLineComment, (multiLineCommentBegin, multiLineCommentEnd)]


def main(): #TODO Нужно переписать, а то вообще не возможно уследить за логикой,
			#TODO нужно сдлеть отдельную функцию которая будет колечать комментс ( в том числе вызывать функцию getCommentsFromUser())
			#ТОесть в неё передаётся флаг - а она возвращает те комментарии которые соответствуют этому флагу

	"""
	files = [] # stores files that need to be cleaned
	flag = "" # stores flag passed as an argument
	if len(sys.argv) > 1:
		if (sys.argv[1][0] == '-') && (( len(sys.argv) > 2):
			#if first argument is a flag AND There are files after the flag
			flag = argv[1]
			files = argv[2:]
		else:
			flag = ""
			files = argv[1:]
	else:
		# if no arguments were passed
		print("Expected: commentsDeleter.py -language 'saveToDir' 'file 1' 'file 2' 'ect...'")

	comments = getComments(flag) #TODO Should ask user to give comments if flag == ""
	for filename in files:
		text = getTextFromFile(filename)
		newText = deleteComments(text, comments)
		dirName = "withoutComments"
		saveTextToFile(dirName, filename, newText)
	"""



	comments = [] # stores comments to delete
	files = [] # stores files that need to be cleaned
	flag = "" # stores flag passed as an argument
	if len(sys.argv) > 1:
		# Get comments and files
		if sys.argv[1][0] == '-':
			flag = sys.argv[1]
			# If the first argument is a key (-cpp,-java,ect)
			files = sys.argv[2:]
			if flag in languages.keys():
				comments = languages[sys.argv[1]]

			elif flag in flags:#TODO
				pass
			else:
				print("Wrong Key\nKnown keys:")
				for language in languages:
					print (language)
				exit(0)
		else:
			files = sys.argv[1:]
			# Let user input comments in a console
			comments = getCommentsFromUser()

########################################################################################################################
		for filename in files:
			#Get text from file , delete comments and save this text back to file
			text = getTextFromFile(filename)

			newText = "" # stores text without comments
			if flag == "-all":
				newText = text
				for languageComments in languages.values():
					newText = deleteSingleLineComments(newText, languageComments[0])
					newText = deleteMultiLineComments(newText, languageComments[1])
			elif flag == "-auto":
				pass
			else:
				# if language or no flag was selected
				newText = deleteSingleLineComments(text, comments[0])
				newText = deleteMultiLineComments(newText, comments[1])

			print( newText )
			dirName = "withoutComments"
			saveTextToFile(dirName, filename, newText)

	else:
		# if no arguments were passed
		print("Expected: commentsDeleter.py -language 'saveToDir' 'file 1' 'file 2' 'ect...'")


if __name__ == '__main__':
	main()