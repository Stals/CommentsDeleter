# Delets every char that follows a comment in that line
# argv's should look like this:
# commentsDeleter.py -cpp "file 1" "file 2" "ect..."
# NOTE: Currently only language flags are working, also you cant choose directory to save files to

#TODO - auto.
#TODO - all Когда сделаю поддержку нескольких вариантов комментариев для мультилйна и синглайна  - когда выбирают -all , нужно создать comments сложа все комментарии для других языков
#TODO подумать о переназвании comments


import sys
import os

class Language:
	def __init__(self,name,flag,singleLineComment,multiLineComment,fileExtensions):
		self.name = name
		self.flag = flag
		self.singleLineComment = singleLineComment
		self.multiLineComment = multiLineComment
		self.fileExtensions = fileExtensions


languages = []
languages.append( Language( 'C++',    '-cpp',    ['//',], [('/*', '*/'),],       ('.cpp', '.h', '.hpp') ) )
languages.append( Language( 'JAVA',   '-java',   ['//',], [('/*', '*/'),],       ('') ) )
languages.append( Language( 'Delphi', '-delphi', ['//',], [('{', '}'),],         ('') ) )
languages.append( Language( 'Python', '-python', ['#',],  [('"""', '"""'),],     ('.py') ) )
languages.append( Language( 'Ruby',   '-ruby',   ['#',],  [('=begin', '=end'),], ('.rb') ) )


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
	while (comment[0] in text) and (comment[1] in text) :
		commentBeginIndex = text.find(comment[0])
		commentEndIndex = text.find(comment[1], commentBeginIndex + len(comment[1])) # TODO mb len(comment[0]) needed?
		# copy  everything except commented text
		text = text[:commentBeginIndex] + \
		       text[commentEndIndex + len(comment[1]):]
	return text


def deleteComments(text, comments):
	newText = text
	for comment in comments[0]:
		#for all single Line Comments
		newText = deleteSingleLineComments(newText, comment)
	for comment in comments[1]:
		#for all multi-line comments
		newText = deleteMultiLineComments(newText, comment)
	return newText


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
	print("No flag was specified")
	singleLineComment = input("Input single line comment:")
	multiLineCommentBegin = input("Input begin of multi-line comment:")
	multiLineCommentEnd = input("Input end if multi-line comment:")
	return [[singleLineComment,], [(multiLineCommentBegin, multiLineCommentEnd),]]


def getComments(flag):
	if flag == "":
		return getCommentsFromUser()
	else:
		for language in languages:
			if flag == language.flag:
				return [language.singleLineComment, language.multiLineComment]

		#if flag is not known
		print("Wrong flag\nKnown flags:")
		for language in languages:
			print ("{0} for {1}".format(language.flag, language.name))
		exit(0)


def main():
	files = [] # stores files that need to be cleaned
	flag = "" # stores flag passed as an argument
	if len(sys.argv) > 1:
		if (sys.argv[1][0] == '-') and (( len(sys.argv) > 2)):
			#if first argument is a flag AND There are files after the flag
			flag = sys.argv[1]
			files = sys.argv[2:]
		else:
			#flag was not specified
			flag = ""
			files = sys.argv[1:]
	else:
		# if no arguments were passed
		print("Expected: commentsDeleter.py -language 'file 1' 'file 2' 'ect...'")
		exit(0)

	comments = getComments(flag)
	for filename in files:
		text = getTextFromFile(filename)
		newText = deleteComments(text, comments)
		dirName = "withoutComments"
		saveTextToFile(dirName, filename, newText)

if __name__ == '__main__':
	main()