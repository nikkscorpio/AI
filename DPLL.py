import sys
import fileinput
import itertools

clauses = []
model = []
model_value = []
symbols = []
pure_symbols = []
unit_symbols = []
split_clause1=[]
split_clause2=[]
isSatisfiable = False
def extract_clauses(inputstr):
  global clauses,model,symbols,pure_symbols,unit_symbols,split_clause1,split_clause2,model_value
  clauses = []
  model = []
  model_value = []
  symbols = []
  pure_symbols = []
  unit_symbols = []
  split_clause1=[]
  split_clause2=[]
  
  if(len(inputList)>0 and inputList[0]=='and'):
    for item in range(1,len(inputList)):
      clauses.append(inputList[item])
  else:
    clauses.append(inputList)
  # remove all OR symbols from clauses
  replace_OR_clause = str(clauses)
  replace_OR_clause= replace_OR_clause.replace("'or',","")
  clauses = eval(replace_OR_clause)

  ##  [['R', ['not', 'B'], 'W']]
  return clauses

## Find if the clauses contain an empty clause
def has_empty_clause(clauses):
  hasEmpty = False
  for item in clauses:
    if len(item)<1:
      hasEmpty =  True
  return hasEmpty

## Find if there is an empty sentence
def is_empty_sentence(clauses):
  if not clauses:
    return True
  else:
    return False

def find_symbols(clauses):
  global symbols
  for item in clauses:
    if len(item) == 1 and str(item).isupper():
      symbols.append(item)
    else:
      itemChild = eval(str(item))
      if str(itemChild[0]) == 'not':
        symbols.append(itemChild)
      else:
        for i in itemChild:
          symbols.append(i)
  return symbols

def find_pure_symbols(clauses):
  global symbols, pure_symbols
  find_symbols(clauses)
  for item in symbols:
    if len(item)==1:
      itemstr = item
      negativeitem = ['not',str(itemstr)]
      if symbols.count(negativeitem) <= 0:
        pure_symbols.append(item)
    elif len(item)>1:
      itemstr = item[1]
      if symbols.count(itemstr) <= 0:
        pure_symbols.append(item)
  return pure_symbols

def eliminate_pure_symbols(clauses):
  global symbols,pure_symbols

  itemarr = []
  for item in pure_symbols:
    if item in clauses:
      clauses.remove(item)
    for subclauses in clauses:
      if(item in subclauses):
        for k in range(0,subclauses.count(item)):
          ## Remove all clauses containing PURE_SYMBOL from CLAUSES list
          clauses.remove(subclauses)
    ## Remove pure_symbol from SYMBOLS list
    if item in symbols:
      for k in range(0,symbols.count(item)):
        symbols.remove((item))

      
    ## Remove pure_symbol from PURE_SYMBOLS list
    itemarr.append(item)
  for items in itemarr:
    ## Append the PURE SYMBOL in the MODEL
    model.append(items)
    pure_symbols.remove(items)
    
    
def find_unit_symbols(clauses):
  global symbols,pure_symbols,unit_symbols
  for item in clauses:
    if(len(item)==1 or eval(str(item))[0]=='not'):

      unit_symbols.append(item)
      
  
def eliminate_unit_symbol(clauses):
  global symbols,pure_symbols,unit_symbols
  itemarr = []

  for item in unit_symbols:

    if(len(item)==1 and str(item).isupper()):
      negative_item = ['not',item]
    else:
      negative_item = eval(str(item))[1]

    if(item in clauses):
      clauses.remove(item)
    if(negative_item in clauses):
      clauses.remove(negative_item)
      clauses.append([])

    for subclauses in clauses:       
      if(str(item) in subclauses):
        clauses.remove(subclauses)

      if(negative_item in subclauses):

        clauses.remove(subclauses)
        subclauses.remove(negative_item)
        clauses.append(subclauses)

     ## Remove unit_symbol from SYMBOLS list
    if item in symbols:
      for k in range(0,symbols.count(item)):
        symbols.remove((item))

    ## Remove pure_symbol from PURE_SYMBOLS list
    itemarr.append(item)
  for items in itemarr:
    ## Append the PURE SYMBOL in the MODEL
    model.append(items)
    unit_symbols.remove(items)
      
def remove_duplicates(values):
    global model
    outputres = []
    for value in model:
        if value not in outputres:
            outputres.append(value)
    return outputres
  
def remove_duplicate_model():
  global model
  for item in model:

    if len(item)==1:
      negative_item = ['not',item]
    else:
      negative_item = eval(str(item))[1]

    if negative_item in model:

      model.remove(negative_item)
  return remove_duplicates(model)
 
  
  

def dpll(clauses):

  global symbols,pure_symbols,unit_symbols
  global isSatisfiable
  if is_empty_sentence(clauses):

    isSatisfiable =  True

  elif has_empty_clause(clauses):

    isSatisfiable =  False
  ## Find and Eliminate all PURE SYMBOLS
  else:
    find_pure_symbols(clauses)

    if(len(pure_symbols)>0):
      eliminate_pure_symbols(clauses)

      dpll(clauses)
    ## Find and Eliminate all UNIT SYMBOLS
    find_unit_symbols(clauses)
    if(len(unit_symbols)>1):
      eliminate_unit_symbol(clauses)

      dpll(clauses)
    split_clause1=[]
    split_clause2=[]
    split_clause1=clauses
    split_clause2=clauses
    if len(clauses)>0:
      if(len(symbols)>0):
        if(len(symbols[0])==1):
          negative_symbol = ['not',symbols[0]]
        else:
          negative_symbol = eval(str(symbols[0]))[1]

        split_clause1.append(symbols[0])
        split_clause2.append(negative_symbol)
        split1 = dpll(split_clause1)
        split2 = dpll(split_clause2)
        if(split1 or split2):
          isSatisfiable =  True
        elif(not split1 and not split2):
          isSatisfiable =  False

  return isSatisfiable
    


filename = sys.argv[2]

#Reading the file
with open(filename) as f:
    input = f.read().splitlines()
length = input[0]
outputfile = open('CNF_satisfiability.txt', 'w')
for i in range(1,int(length)+1):
  inputstr = input[i]
  print input[i]
  inputList = eval(inputstr)
  extract_clauses(inputstr)
  if(dpll(clauses)):
    model_value.append("true")
    model = remove_duplicate_model()
    for item in model:
      if(len(item)==1):
        strvalue = item+"=true"
        model_value.append(strvalue)
      else:
        itemstr = eval(str(item))[1]
        strvalue = itemstr+"=false"
        model_value.append(strvalue)
      
  else:
    model_value.append("false")
  outputfile.write(str(model_value)+"\n")






