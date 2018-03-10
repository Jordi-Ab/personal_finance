import pandas as pd

def crossJoin(series, columns):
  if len(series)<2:
      print ('Series to cross join must contain at least two elements')
  else:
      df1 = pd.DataFrame(series[0], columns = [columns[0]])
      df1['key'] = 1
      i=1
      while i < len(series):        
          df2 = pd.DataFrame(series[i], columns = [columns[i]])
          df2['key'] = 1
          result = pd.merge(df1, df2, on='key')
          df1 = result
          i += 1
      result.drop('key', axis=1, inplace=True)
      return result

