# Name:  Manuel Steele      * Net ID:  msteele1
# Program:  proj2_graph1_draft.py

########################################################
#PSEUDOCODE
# This code does the following steps
# 1. Opens input file and reads lines.
# 2. Applies regular expressions to filter out comment lines.
# 3. Splits lines by the pipe '|' symbol into a list.
# 4. Numerical analysis is applied to the list.
#   a.Counts each class into parameters transitCnt, contentCnt, and
#     enterpriseCnt.
#   b. Counts the total and then the percentage of each class.
#       i. Creates the labels for each class
#       ii. Stores the percentage values in a list - List_Graph1.
# 5. Uses the list from step 5 to create a pie chart.
import re
import matplotlib.pyplot as plt

def main():
    # Open the input file
    myFile = open('20150801.as2types.txt', 'r')
    
    # Before the loop of reading lines begins - initialize the
    # parameters for count and percent
    # Count of Enterprise
    entCount = 0;
    # Couint of Transit/Access
    transCount = 0;
    # Count of Content
    contCount = 0;
    #Total Count
    totalCount = 0;
    # Percent of Entrprise
    entPct = 0;
    # Percent of Transit/Access
    transPct = 0;
    # Percent of Content
    contPct = 0;

    for myLine in myFile:
        # strip newline characters
        myLine = myLine.rstrip('\n')

        # Search for the lines that match the pattern of ex. '20|CAIDA_class|Transit/Access'
        myPattern = re.search(r'^\d{1,8}\|[a-zA-Z]{1,15}_class\|[a-zA-Z]{1,15}\/?[a-zA-Z]{0,10}',
            myLine, re.M|re.I)
        # If a line matches the expected pattern of pipe-delimited data, then
        # split the lines into a list.
        if myPattern:
            myList = myLine.split("|")
            # Extract the class value from the 3rd element in the list
            myClass = myList[2]
                  
            # Check if myClass matches enterprise
            entPattern = re.search(r'^[eE]nterprise|^[eE]nterpise', myClass, re.M|re.I)
            # Check if myclass matches transit/access
            transPattern = re.search(r'^[tT]ransit/Access', myClass, re.M|re.I)
            # Check if myclass matches content
            contPattern = re.search(r'^[cC]ontent', myClass, re.M|re.I)

            if entPattern:
                #increment count of Enterprise
                entCount = entCount + 1;
            if transPattern:
                #increment count of Transit/Access
                transCount = transCount + 1;
            if contPattern:
                #increment count of Content
                contCount = contCount + 1;
        # Increment total regardless of match
        totalCount = totalCount + 1

    # Calculate percentage for enterprise
    entPct = entCount/totalCount;
    # Calculate percentage for transit/access
    transPct = transCount/totalCount;
    # Calculate percentage for content
    contPct = contCount/totalCount;
    
    # Create the pie plot
    pieLabels = ('Enterprise', 'Transit/Access', 'Content')
    # percentages
    pcntList = [entPct, transPct, contPct]

    # Plot
    plt.axis("equal")
    plt.pie(
            pcntList,
            labels = pieLabels,
            autopct = "%1.3f%%"
        )
    plt.title("Project 2 - Graph 1")
    plt.show()

    # Close file
    myFile.close()


main()
