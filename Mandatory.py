import sys
import subprocess
import os
import utilModule as util
from urllib.request import urlopen
from urllib.error import HTTPError

def main():
  try:
    # variable creation and retrieving JSON string from url
    url = 'https://api.github.com/orgs/python-elective-1-spring-2019/repos?per_page=100'
    res = urlopen(url)
    html = res.read().decode('utf-8', 'ignore')
    filename = 'testhtml.html'

      # Actually creates the html file
    subprocess.run(['touch', 'testhtml.html'])

      # List that will hold "clone_url" strings
    urlList = []

      # Writes the whole API response into single string
    with open(filename, "r+", encoding="utf8") as fileManager:
          fileManager.write(html)
      
      # Chops block of text into lines and adds lines with "clone_url" to a list
    with open(filename, "r+", encoding="utf-8") as fileManager:
      for text in fileManager:
        lines = text.split(',')
        for newLine in lines:
          if newLine.startswith('"clone_url'):
            urlList.append(newLine)
          else:
            pass
    
      # Uses the provided API and fetches links, formats them, and uses the formatted link names to create directories #
    pathNames = util.makePathNames(util.formatURLStrings(urlList))

    choices = '1. Make dirs\n2. Clone Repos\n3. Make consolidated README.md\n4. Delete repos\n5. Delete allREADMEs\n6. Push README to GitHub\nPress q to stop program\n'
  
    while True:
      # Promt the user for input to perform action
      userInput = input(choices)


      # Stops program
      if userInput == 'q':
        sys.exit()

      # Makes dirs
      if userInput == '1':
        # Actually makes the directories
        util.makeDirsForRepos(pathNames)
        
      # Makes clone links
      if userInput == '2':
      # The links needed for cloning
        clonePaths = util.makeClonePaths(urlList)

      # Goes into each directory and clones the corresponding GitHub link #
        util.cloneReposToDirs(pathNames, clonePaths)
        

      # Make my README
      if userInput == '3':
      # Creates a consolidated README with the bullet points from every readme found in the dirs
        util.writeFoundREADMEtoNewFile(util.findREADMEmarkdowns(pathNames))
        

      
      if userInput == '4':
      # DELETES THE CLONED REPOS
        util.deleteRepos(pathNames)
      
      if userInput == '5':
        util.deleteMyREADME()

      if userInput == '6':
        util.pushToGithub()
  except HTTPError as err:
    print()
    print('This error occurred due to too many requests to github from one IP. Choose a different network to resolve this issue.')
    print()

if __name__ == '__main__':
  main()