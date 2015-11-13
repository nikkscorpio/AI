import sys
import fileinput
import itertools

# Global Flag to check if converttoCNF should run with distributivity
mainflag = False

##Check if sentence is a variable
def isLiteral(sentence):
  if len(sentence) == 1 and sentence.isupper():
    return True
  else:
    return False

##Check if sentence is a negation
def isNegative(sentence):
  if len(sentence)>1 and eval(sentence)[0]=='not':
    return True
  else:
    return False

##Check if the main connective is OR
def hasOROperator(sentence):
  if len(sentence) == 1 and sentence.isupper():
    return False
  else:
    flag = False
    operator = eval(sentence)[0]
    if(operator == 'or'):
      flag = True
    return flag
   
# remove duplicates
def eliminateDup(inputlist):
  for item in inputlist:
    items = [j for j, x in enumerate(inputlist) if x == item]
    if len(items)>1:
      del items[0]
      for Z in items:
    ##Pop the element
        inputlist.pop(Z)
      
  for item in inputlist:  
    if isinstance(item, list):
      for j in item:
        items = [k for k, x in enumerate(item) if x == j]
        if len(items)>1:
          ## Delete the items
          del items[0]
          for Z in items:
            item.pop(Z)

## Flatten Disjunctions and Conjunctions
  
def flattenConnectives(inputlist):
  operand = inputlist[0]
  mainsentence = []
  mainsentence.append(operand)
  for item in range(1,len(inputlist)):
    inneritem = inputlist[item]
    if(len(inneritem)>1 ):
      innersubitem = eval(str(inneritem))
      if(innersubitem[0]==operand):
        inneroperand = innersubitem[0]
        innersubitem.remove(innersubitem[0])
        for each in innersubitem:
          mainsentence.append(each)
        
      else:
        mainsentence.append(innersubitem)
    else:
      mainsentence.append(inneritem)
  return mainsentence
        
## Main function to convert sentence to CNF form
## Following steps are followed:
## 1. Eliminate biconditionals and implications
## 2.  Move NOT inwards
## 3. Distribute AND over OR (Run this only if the above )

def converttoCNF(sentence):

  global mainflag
  if len(sentence) == 1:
    return sentence
  else:
    inputstrlist = eval(sentence)
    operandlist = [inputstrlist[0]]


 #CASE FOR IMPLIES
  #################
  
  if inputstrlist[0] == 'implies':
    new1operand = ["not",inputstrlist[1]]
    newlist = ["or",new1operand,inputstrlist[2]]
    sentence =  str(newlist)
    return converttoCNF(sentence)

  #CASE FOR IFF
  #################
  
  if inputstrlist[0] == 'iff':
    list1 = ["implies",inputstrlist[1],inputstrlist[2]]
    list2 = ["implies",inputstrlist[2],inputstrlist[1]]
    newlist = ["and",list1,list2]
    sentence = str(newlist)
    return converttoCNF(sentence)
  
  # CASE FOR NOT
  ################
  
  if inputstrlist[0] == 'not':
    i=1
    newlist = []
    #Check if first operand is a variable
    if len((inputstrlist[1]))== 1 and str(inputstrlist[1]).isupper():
      return ((inputstrlist))
    elif len(inputstrlist[1])>1:

      new1operand = eval(str(inputstrlist[1]))
      if new1operand[0] == 'and':
        newlist = ["or"]
        i=1
       
        while i<len(new1operand):
          newoperandlist = ["not",new1operand[i]]
          newlist.append(newoperandlist)
          i = i+1
      elif new1operand[0] == 'or':
        newlist = ["and"]
        i=1
        while i<len(new1operand):
          newoperandlist = ["not",new1operand[i]]
          newlist.append(newoperandlist)
          i = i+1
      elif new1operand[0] == 'not':
        return converttoCNF(str(new1operand[1]))
      else:
        newlist =['not']
        newlist.append(converttoCNF(str(new1operand)))
 
    sentence = str(newlist)
    return converttoCNF(sentence)

  # CASE FOR AND OR DISTRIBUTIVITY
  #################################
  
  if len(inputstrlist) > 1 and mainflag:
    operandlist = [inputstrlist[0]]
    ##SIMPLIFY SENTENCES
    for k in range(1,len(inputstrlist)):
       if(isLiteral(str(inputstrlist[k]))):
         operandlist.append(inputstrlist[k])     
       else:
         
         operandlist.append(converttoCNF(str(inputstrlist[k])))

    #CHECK IF THE MAIN OPERATOR IS "AND", IF SO RETURN THE SENTENCE
    if(operandlist[0]=='and'):
        return operandlist
    else:
      ORliterals = ['or']
      ANDliterals = ['and']
      for m in range(1,len(operandlist)):
        if(isLiteral(str(operandlist[m])) or hasOROperator(str(operandlist[m])) or isNegative(str(operandlist[m]))):
          if hasOROperator(str(operandlist[m])):
            ORopers = eval(str(operandlist[m]))
            for p in range(1,len(eval(str(operandlist[m])))):
              ORliterals.append(ORopers[p])
          else:
              ORliterals.append(operandlist[m])
        else:
              ANDliterals.append(operandlist[m])
      ANDliteralsstr = str(ANDliterals)
      ANDliteralsstr = ANDliteralsstr.replace("'and',","")
      # Perform AND-OR operations if there are more than 1 AND Clauses
      result = []
      if len(ANDliterals) > 2:
        ANDliteralsstr = str(ANDliterals)
        ANDliteralsstr = ANDliteralsstr.replace("'and',","")
        ANDliteralsstreval = eval(ANDliteralsstr)

        result2 = list(itertools.product(*ANDliteralsstreval))
        result3 = []
        for item in result2:
          newitem = list(set(item))
          newitem.insert(0,"or")
          result3.append(newitem)
        result = result3
                

      
      if(len(ANDliterals)>2):
        newsentence = ['and']
        for n in range(0,len(result)):
          tempORliterals = []
          if len(ORliterals)>1:
            for item in ORliterals:
              tempORliterals.append(item)
            tempORliterals.append(result[n])
            newsentence.append(tempORliterals)
            print tempORliterals
          else:
            newsentence.append(result[n])
        return newsentence

        if len(ORliterals)<2 and len(ANDliterals) >2:
          newsentence = ['and']
          for n in range(0,len(result)):
            newsentence.append(result[n])
          return newsentence
      elif len(ANDliterals) == 2 and len(ORliterals)>1:
        newsentence =['and']
        for z in range(1,len(eval(str(ANDliterals[1])))):
          tempANDliteral = eval(str(ANDliterals[1]))
          tempORliteral = []
          for z1 in ORliterals:
            tempORlit = z1
            tempORliteral.append(tempORlit)
 
          tempORliteral.append(tempANDliteral[z])
          newsentence.append(tempORliteral)
        return newsentence
      else:
        return ORliterals
  return sentence         
    
filename = sys.argv[2]

#Reading the file
with open(filename) as f:
    input = f.read().splitlines()
length = input[0]
outputfile = open('sentences_CNF.txt', 'w')
for i in range(1,int(length)+1):
  inputstr = input[i]
  mainflag = False
  output = str(converttoCNF(inputstr))
  mainflag = True
  output = str(converttoCNF(output))
  outputeval = eval(output)
## Eliminate Duplicates from output
  eliminateDup(outputeval)
## FLATTEN CONJUNCTIONS AND DISJUNCTIONS
  outputeval = flattenConnectives(outputeval)
  inputstring = str(outputeval)
  output_sentences = inputstring+"\n"
  outputfile.write(output_sentences)
  
