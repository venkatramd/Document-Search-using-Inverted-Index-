import re
import string
import os
import glob
from selenium import webdriver

#cwd = os.getcwd()  # Get the current working directory (cwd)
#files = os.listdir(cwd)  # Get all the files in that directory
#print("Files in '%s': %s" % (cwd, files))

#getting all files from folder to a array
cwd = os.getcwd()# Get the current working directory (cwd)
cwd=cwd+"/dataset/" #adding exact location
files = []
#print(cwd)
for i in os.listdir(cwd):
    if i.endswith('.txt'):
        files.append(i)
#print(files)

totalfiles=len(files)
retrivedfiles=[]

actualfile = []
wordsinfile = []
noofoccurenceofwords = []
afterremovingduplecates = []
wordoccurenceandpos = []
sortwithmaxwordoccurence = []
#reading from file and store it into a array
for i in range(0,len(files)):
    print("DOCUMENT "+str(i+1)+"\n\n\n\n\n")
    print("\n\n\n\nREADING DATA FROM FILE\n")

    with open(cwd+files[i], 'r') as myfile:
        data=myfile.read().replace('\n', " ")

        data.replace(':',"")
        data.replace('-'," ")
    print(data)
    actualfile.insert(i,data)


    arra1 = re.sub('['+string.punctuation+']', '', data).split()
    arra1 = [element.lower() for element in arra1];
    #print(arra1)


    #converting to lowercase
    #map(str.lower, arra1)

    print("\n\n\nTOTAL NO OF WORDS EXTRACTED IN THE FILE  :"+str(len(arra1)))
    wordsinfile.insert(i,len(arra1))

    #arra1=["aaa","bbb","ccc","ddd","aaa","aaa","aaa"]
    lwp = []
    b = []
    unique = []
    k=0
    for i in range(0,len(arra1)):

        presense=False
        for check in range(0,len(unique)):
            presense=False
            if(arra1[i]==unique[check]):
                presense=True
                break
            if(presense==True):break

        if(presense==False):
            unique.append(arra1[i])
            count=0
            b.append(arra1[i])
            lwp.append(arra1[i])
            pos = []

            pos=[]
            for j in range(i,len(arra1)):

                if(arra1[i]==arra1[j]):
                    count=count+1
                    pos.append(j+1)
            b.append(count)
            #print("position list")
            #print(pos)
            lwp.append(count)
            lwp.append(pos)
    #print()
    print("\n\n\n\nNO OF OCCURENCE OF WORDS\n\n ")
    print(b)
    noofoccurenceofwords.insert(i,b)

    print("\n\n\n\nAFTER REMOVAL OF DUPLECATE WORDS\n\n ")
    print(unique)
    afterremovingduplecates.insert(i,unique)

    print("\n\n\n\nINVERTED INDEX WITH OCCURENCE AND POSITIONS\n\n ")
    print(lwp)
    wordoccurenceandpos.insert(i,lwp)

    #continue with highest number of occurence of words
    occur = []
    occurword = []
    for i in range(1,len(b),2):
        occur.append(b[i])

    for i in range(0,len(b),2):
        occurword.append(b[i])

    #print(occur)
    #print(occurword)

    seq=occur.copy()
    seqword=occurword.copy()

    for i in range(1, len(seq)):
            j = i
            while j > 0 and seq[j - 1] > seq[j]:
                seq[j - 1], seq[j] = seq[j], seq[j - 1]
                seqword[j - 1], seqword[j] = seqword[j], seqword[j - 1]
                j -= 1
    seq.reverse()
    seqword.reverse()
    #print(seq)
    #print(seqword)

    #after merge
    aftersort = []
    for i in range(0,int((len(b))/2)):
        aftersort.append(seqword[i])
        aftersort.append(seq[i])

    print("\n\n\n\nSORTING WITH RESPECT TO NUMBER OF OCCURENCE\n\n ")
    print(aftersort)
    print("\n\n\n\n")
    sortwithmaxwordoccurence.insert(i,aftersort)


#important ARRAYS FOR SEARCHING
#actualfile wordsinfile noofoccurenceofwords afterremovingduplecates wordoccurenceandpos sortwithmaxwordoccurence



browser = webdriver.Chrome()
browser.get("file:///home/venkatram/PycharmProjects/invertedIndex/projecthtml/index.html")
#browser.maximize_window()
querybox=browser.find_element_by_id('querybox')
check=browser.find_element_by_id('check')
resultbox=browser.find_element_by_id('resultbox')

query=''
def getquery():
    print("\n\nquery is :"+query)
    check.clear()
    check.send_keys('false')
    querylist = query.split()
    # print("QUERRY LIST"+str(querylist))
    qurres = []
    qurresfinal= []
    for s in range(0, len(querylist)):
        insertonce = False
        qurres=[]
        for j in range(0, len(files)):
            for i in range(0, len(wordoccurenceandpos[j]), 3):
                if wordoccurenceandpos[j][i] == querylist[s]:
                    if (insertonce == False):
                        insertonce = True
                        qurres.append(wordoccurenceandpos[j][i])
                    qurres.append(" " + files[j]+"")
                    retrivedfiles.append(" " + files[j]+"")
                    qurres.append(wordoccurenceandpos[j][i + 1])
                    qurres.append(wordoccurenceandpos[j][i + 2])
        qurresfinal.insert(s,qurres)
    print(qurres)
    print(qurresfinal)




    sendtoresultbox=','.join(str(e) for e in qurresfinal)
    resultbox.clear()
    resultbox.send_keys(sendtoresultbox)

#SEND QUERY INFORMATION FROM HERE



while True:
    if(check.get_attribute('value')=='true'):
        query=querybox.get_attribute('value')
        getquery()





#query = "College shivamogga"

#read querry from file


