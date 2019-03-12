import subprocess
import os
import glob
from operator import itemgetter

# Pushes the new README to own GitHub #

def pushToGithub():
  commitMessage = "'git push'"
  os.chdir('../Mandatory_1_git')
  subprocess.run(['git', 'commit', '-am', f'{commitMessage}'], shell=True)
  subprocess.run(['git', 'push'], shell=True)



# Utility function for deleting all the cloned git repos #
# OBSERVE! THIS FUNCTION CAN ONLY RUN ONCE PER "python mandatory.py" DUE TO SOME ISSUE WITH GIT AND UNICODE SPECIAL CHARACTERS #
# TO DELETE THE REPO AGAIN THE PROGRAM WILL HAVE TO RESTART #
def deleteRepos(paths):
  try:
    os.chdir('../Mandatory_1')
    for path in paths:
      if not os.path.isdir(f'{path}/{path}'):
        print()
        print('Repos already deleted.')
        print()
        return
      else:
        os.chdir(f'{path}')
        subprocess.run(['rm', '-rf', f'{path}'], shell=True)
        os.chdir('../')

    print()
    print('Repos deleted.')
    print()

  except FileNotFoundError as err:
    print('The specified path was not found')
    pass




# IS RESPONSIBLE FOR FINDING README.MD FILES, RETRIEVING THE NEEDED CONTENT AND RETURNING A LIST OF SORTED CONTENT #
def findREADMEmarkdowns(paths):
  os.chdir('../Mandatory_1')
  readmeNameList = []
  readmeNameList.clear()
  fileName = ''
  savedLines = []
  try:
    for path in paths:
      
      readmeNameList.append(glob.glob(f'**/{path}/readme.md', recursive=True))
    
    if len(readmeNameList) == len(paths):
      for readme in readmeNameList:
        readme = str(readme)
        readme = readme[2:-2]
        
        fileName = open(readme, 'r', encoding="utf-8")
        fileNameText = fileName.readlines()
        
        i = 1
        for line in fileNameText:
          if line.startswith('## Required reading'):
            savedLines.append(line)
            #nextLine = fileNameText[fileNameText.index(line) + 1]
            
            while fileNameText[fileNameText.index(line) + i].startswith('* '):
              savedLines.append(fileNameText[fileNameText.index(line) + i])
              i += 1
    
    else:
      print('ERROR: list had different length to paths')
  except FileNotFoundError as err:
    print('Could not find readme.md files. Choosing "Clone repos" might fix this issue')
  except IndexError as err2:
    print()
    print(err2)
  return removeDuplicates(savedLines)
    
# IS FED THE "REQUIRED READING" CONTENTS OF EVERY README.MD FILE. CONVERTS AND SORTS THE LIST ARGUMENT #
def writeFoundREADMEtoNewFile(MDList):
  try:
    oldFirstElement = MDList[0]

    MDList = sorted(MDList[1:], key=itemgetter(3))
    
    readmeFileName = 'allReadMes.md'

    os.chdir('../Mandatory_1_git')
    # Checks if file exists. If true then deletes it. We want to have a new file every time because we get a complete list
    # every time we run this method, and as such append to the file
    if os.path.isfile('./allReadMes.md'):
      subprocess.run(['rm', 'allReadMes.md'], shell=True)
    subprocess.run(['touch', 'allReadMes.md'], shell=True)
    print()
    print('README created at ../Mandatory_1_git/')
    print()
    with open(readmeFileName, 'a+', encoding="utf-8") as fileManager:
      fileManager.write(oldFirstElement)
      for line in MDList:
        line = line[:-1]
        fileManager.write(line)
        fileManager.write('\n')
  except IndexError as err:
    print('The list argument seems to be broken')

def deleteMyREADME():
  print()
  readme = 'allReadMes.md'
  os.chdir('../Mandatory_1_git')
  if os.path.isfile(readme):
    
    print('README deleted.')
    subprocess.run(['rm', readme], shell=True)
  else:
    print('The file does not exist.')
  print()

# IS RESPONSIBLE FOR CLONING THE REQUIRED REPOS INTO THE CORRECT CORRESPONDING FOLDERS #
def cloneReposToDirs(paths, cloneLinks):
  i = 0
  if len(paths) == len(cloneLinks):
    os.chdir('../Mandatory_1')
    # First loop check if the repos already exist #
    for path in paths:
      if os.path.isdir(f'{path}/{path}'):
        print()
        print('Repos already exist.')
        print()
        break
      else:  
        os.chdir(f"{path}")

        # Second loop performs the git clone command on the proper paths #
        subprocess.run(['git', 'clone', cloneLinks[i]], shell=True)
        i += 1
        os.chdir('../')
  else:
    print('Lengths of the two arguments MUST be the same')
    pass
      

# THIS FUNCTION TAKES THE WHOLE UNFORMATTED LINE AND CUTS OFF THE "CLONE_URL" PART
# AS WELL AS THE BEGGING OPENING AND CLOSING DOUBLE QUOTES """", EXAMPLE:
# "clone_url":"https://github.com/python-elective-1-spring-2019/Lesson-06-Git-Markdown-and-Required-reading-Exercise.git"
# BECOMES  ---> "https://github.com/python-elective-1-spring-2019/Lesson-02-Introduction-to-Python-and-Python-Strings.git
def formatURLStrings(urls):
  i = 0
  for element in urls:
    urls[i] = element[12:-1]
    i += 1
  # FIRST ELEMENT OF THE LIST HAS NO README.MD, THEREFORE IT IS EXCLUDED FROM THE RETURN RESULT #
  return urls[1:]

# CREATES A SORTED LIST OF CLONE URLS THAT CAN BE READ BY THE SUBPROCESS MODULE, EXAMPLE:
# https://github.com/python-elective-1-spring-2019/Lesson-02-Introduction-to-Python-and-Python-Strings.git
def makeClonePaths(urls):
  excludedString = 'python-elective-1-spring-2019.github.io.git'
  clonePathList = []
  i = 0
  for element in urls:
    if excludedString in urls[i]:
      i += 1
    else:
      urls[i] = element[1:]
      clonePathList.append(urls[i])
      i += 1
  return sorted(clonePathList, key=str.lower)

# SIMPLY CREATES THE DIRECTORIES WERE THE CLONED REPOS WILL GO INTO
def makeDirsForRepos(dirList):
  try:
    for directory in dirList:
      if os.path.isdir(directory):
        print()
        print('Directories already exist.')
        print()
        break
      else:
        os.chdir('../Mandatory_1')
        subprocess.run(['mkdir', directory], shell=True)
  
  except OSError as err:
    print(err+ "woops")
    
    
# PURPOSE OF THIS FUNCTION IS TO AUTOMATICALLY MAKE A READABLE FOLDER NAME FOR THE CLONED REPO DESTINATIONS
def makePathNames(formattedUrlList):
  pathList = []
  i = 0
  for url in formattedUrlList:
    # THIS REMOVES THE DOMAIN PATHNAME AND LEAVES ONLY A READABLE FOLDER NAME, EXAMPLE:
    # Lesson-02-Introduction-to-Python-and-Python-Strings
    formattedUrlList[i] = url[50:-4]
    if formattedUrlList[i].startswith('python'):
      i += 1
    else:
      pathList.append(formattedUrlList[i])
      i += 1
  return sorted(pathList, key=str.lower)

def removeDuplicates(someList):
  uniqueList = []
    
  for elem in someList:
    if elem not in uniqueList:
      uniqueList.append(elem)
          
  return uniqueList