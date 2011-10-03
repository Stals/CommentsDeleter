# Delets every char that follows a comment in that line
#TODO delete multi-line comments
import sys
languages = {"-cpp"    : [ '//', ('/*', '*/') ],
             "-java"   : [ '//', ('/*', '*/') ],
             "-delphi" : [ '//', ('{', '}') ],
             "-python" : [ '#',  ('"""', '"""') ],
             "-ruby"   : [ '#',  ('=begin', '=end') ]
             }

def deleteSingleLineComments(lines,singleComment):#TODO do not delete line separators
    newLines = []
    for line in lines:
        if singleComment in line:
            newLine = ""
            commentIndex = line.find(singleComment)
            newLine = line[:commentIndex] + "\n" #TODO add /n only if /n is at the end of the line
            newLines.append(newLine)
        else:
            newLines.append(line)

    print (newLines)
    return newLines

def main():
    comments = []
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
            lines = f.readlines()
            f.close()

            newLines = deleteSingleLineComments(lines, comments[0])
            #newLines = deleteMultiLineComments(newLines,comments[1:])

            f = open("2.txt", 'w')
            f.writelines(newLines)
            f.close()

if __name__ == '__main__':
  main()