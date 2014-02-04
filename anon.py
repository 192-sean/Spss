
#---------------1st Function------------------------
#Strips every label value so that there is no extra white space on either ends
#Also deletes any variable labels starting with variable name starting with "SCO" and on 
import spss, re

def removeScoLabels(filename):
  spss.Submit(filename)
  spss.StartDataStep()
  datasetObj = spss.Dataset()
  varListObj = datasetObj.varlist
  count = len(varListObj)
  change = False

  for i in datasetObj.varlist:
      if i.label:
         temp = str(i.label)
         temp = str.strip(temp)
         i.label = unicode(temp)
      else:
         s = 1-1
  for i in range(count):
      if re.search('\ASC0', datasetObj.varlist[i].name):
          change = True
      if change:
           datasetObj.varlist[i].label = ''
  spss.EndDataStep()


#-----------------2nd Function---------------------------
#Removes all digits in the Please rate variable labels
#so that the order of the question doesn't matter.
#Also removes the words "items" or "issues" because
#some questions had them and some didn't.
#Last it correctly prefixes the variable names.

import spss, re

def renameDoopLabels(filename):
  spss.Submit(filename)
  spss.StartDataStep()
  datasetObj = spss.Dataset()
  varListObj = datasetObj.varlist
  prefix = ''
  pren = 'EE'
  for i in datasetObj.varlist:
    print i.name
    if i.label:
       
       if re.search('\APlease rate the', i.label):
         i.label = ''.join(k for k in i.label if not k.isdigit())
       if re.search('\APlease rate the following items', i.label):
         i.label = re.sub("items ", "", i.label, count=1)
       if re.search('\APlease rate the following issues', i.label):
         i.label = re.sub("issues ", "", i.label, count=1)

       if re.search('\AExample ', i.label):
         prefix = 'ex '
         pren = 'EE'
         i.name = 'EE' + i.name

       if re.search('\AQuality of',i.label):
         prefix = 'qh '
         pren = 'EE'
         i.name = 'EE' + i.name
       if re.search('\ASoap Box', i.label):
         prefix = 'sb '
         pren = 'EE'
         i.name = 'EE' + i.name
       if re.search('\AInternational Aid', i.label):
         prefix = 'ai '
         pren = 'EE'
         i.name = 'EE' + i.name
       if re.search('\AFlood-Control', i.label):
         prefix = 'fc '
         pren = 'EE'
         i.name = 'EE' + i.name
       if re.search('\AFlood Control', i.label):
         prefix = 'fc '
         pren = 'EE'
         i.name = 'EE' + i.name
       if re.search('\ANurse Schedule', i.label):
         prefix = 'ns '
         pren = 'EE'
         i.name = 'EE' + i.name
       if re.search('\AWater Quality', i.label):
         prefix = 'wq '
         pren = 'EE'
         i.name = 'EE' + i.name
       if re.search('\AGrant Proposal', i.label):
         prefix = 'gp '
         pren = 'EE'
         i.name = 'EE' + i.name
       if re.search('\APedestrian Bridge', i.label):
         prefix = 'pb '
         pren = 'EE'
         i.name = 'EE' + i.name
       
       if re.search('\AFamine', i.label):
         prefix = 'fam '
         pren = 'DD'
         i.name = 'DD' + i.name
       if re.search('\AReporter', i.label):
         prefix = 'rep '
         pren = 'DD'
         i.name = 'DD' + i.name
       if re.search('\ASchool Board', i.label):
         prefix = 'sch '
         pren = 'DD'
         i.name = 'DD' + i.name
       if re.search('\ACancer', i.label):
         prefix = 'can '
         pren = 'DD'
         i.name = 'DD' + i.name
       if re.search('\ADemonstration', i.label):
         prefix = 'dem '
         pren = 'DD'
         i.name = 'DD' + i.name
 
       if re.search('\AConsider', i.label):
            i.label = prefix + i.label
       if re.search('\APlease rate', i.label):
            i.label = prefix + i.label
       if re.search('\ARate the', i.label):
            i.label = prefix + i.label
            
       if re.search('\AQ', i.name):
            i.name = pren + i.name
       if re.search('\A[a-d]_', i.name):
            i.name = pren + i.name
       if re.search('\A[a-b].', i.name):
            i.name = pren + i.name
       
    else:
      print 'caught'
    
  spss.EndDataStep()

#-----------------------3rd Function-----------------------------
#Creates a dictionary of variable names and labels.
#Run through each file pairs the label and name according to
#the dictionary adding to it if needed.

import spss, re
dict = {}

def rename(filename, dictionary):
  prefix = 'GG'
  spss.Submit(filename)
  spss.StartDataStep()
  datasetObj = spss.Dataset()
  varListObj = datasetObj.varlist
  for i in datasetObj.varlist:
    if i.label:
     if i.label in dict:
        print i.label + ' ' + dict[i.label]
        i.name = dict[i.label]
     else:
        if re.search('\AEE', i.name):
           prefix = 'EE'
        elif re.search('\ADD', i.name):
           prefix = 'DD'
        elif re.search('\ATeam', i.name):
           prefix = 'TT'
        else:
           prefix = 'GG'
        dict[i.label] = prefix + str(len(dict) + 1)
        i.name = dict[i.label]
    else:
        print 'caught'
  spss.EndDataStep()

#--------------------4th function------------------------
#Runs through each file in folder and adds a 
#new variable called source_file so that when
#merged the original file will be known.
#This function automatically saves after completion

import os, spss
dir = 'C:\Users\Sean\Downloads\Spss' # Specify folder containing .sav files.
fils = sorted([fil for fil in os.listdir(dir) if fil.endswith('.sav')])
vallabs = ' '.join([str(num + 1) + '"%s"'%fil for num,fil in enumerate(fils)])
for num,fil in enumerate(fils):
    num += 1
    spss.Submit('''
get fil '%(dir)s/%(fil)s'.
compute source_file=%(num)d.
val lab source_file %(vallabs)s.
sav out '%(dir)s/%(fil)s'.
'''%locals())
spss.Submit('new fil.')

#------------------5th function----------------
#Merges each file in the folder
import os, spss
rdir = 'C:\Users\Sean\Downloads\Spss' #Please specify folder containing .sav files.
fils = sorted([fil for fil in os.listdir(rdir) if fil.endswith('.sav')])
spss.Submit('get file "%s/%s".'%(rdir,fils.pop(0)))
for rep in range(len(fils)/49 + 1):
    spss.Submit('add files file=*/%s.'%'/'.join(['file="%s"'%os.path.join(rdir,fil) for fil in fils[49*rep:49*rep + min(49,len(fils)-49*rep)]]))
spss.Submit('exe.')

#----------Test function-----------------------------
#searches for matching label and prints with string length
import spss, re

def stringLen(filename):
  spss.Submit(filename)
  spss.StartDataStep()
  datasetObj = spss.Dataset()
  varListObj = datasetObj.varlist
  for i in datasetObj.varlist:
   if i.label:
    if re.search('\Aqh', i.label):
        print i.label + '   ' + str(len(i.label))
   else:
        s = 1 + 1
  spss.EndDataStep()
