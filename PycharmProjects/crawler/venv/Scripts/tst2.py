import pandas as pd

aaa = pd.read_csv("C:/Users/yui/Documents/aaa/tester.csv")

print(aaa)
aaa.to_json("C:/Users/yui/Documents/aaa/tester.json", orient='records')