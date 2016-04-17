def getQueries(data):
  queries = []
  j = 0
  for i in data:
    j = j + 1
    if i == "******": break
    queries.append(i)
  return queries, j

def seperateNodeInfo(data):
  nodes = []
  current = []
  for i in data:
    if i == "***" or i == "******":
      nodes.append(current)
      current = []
      continue
    current.append(i)

  nodes.append(current)
  return nodes

def arrayToIOString(array):
  str = ""
  lasti = len(array)-1
  for i in array[:lasti]:
    str = str + i + "\n"
  str = str + array[lasti]
  return str

def roundFloat(f):
  o = f
  if o < 0: f = f*-1
  rounded = int(f*100)
  new = int(f*1000)
  remainder = new %10
  if remainder >= 5: rounded = rounded + 1
  
  f = (o < 0 and -1 or 1)*float(rounded)/100
  return f

def roundInt(i):
  o = i
  if o < 0: i = i*-1
  j = int(i)
  diff = i - j
  if diff*10 >= 5: r= j+1
  else: r= j
  return (o < 0 and -1 or 1)*r

def arrayToString(array):
  str = ""
  lasti = len(array)-1
  if lasti <0: return ""
  for i in xrange(lasti):
    str = str + array[i] + " "
  str = str + array[lasti]
  
  return str