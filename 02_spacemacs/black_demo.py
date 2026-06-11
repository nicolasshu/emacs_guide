import os,sys
from pathlib import Path

def greet( name ,times=3):
  result=[]
  for i in range(0,times):
      result.append( f"Hello, {name}! #{i}" )
  return result

def process_data(data,debug=False ):
      output={}
      for k,v in data.items():
            if debug==True:
                 print("processing",k,v)
            output[k ]= v*2 if isinstance(v,(int,float)) else str(v).strip()
      return output

class Report:
   def __init__(self,title,data):
        self.title=title
        self.data=data

   def summary( self ):
        total=sum([v for v in self.data.values() if type(v) in [int,float]])
        return {"title":self.title,"total":total}

if __name__=="__main__":
    raw={"a":1,"b": 2,"c":"  test  "}
    print( process_data(raw,debug = True) )
    print(greet("World", 5))
    r=Report("Demo",{"x":10,"y":20})
    print( r.summary() )
