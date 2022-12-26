from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
app = Flask(__name__)


def outlier(df):
    columns = list(df.columns.values)
    for col in columns:
      if is_numeric_dtype(df[col]):
         
         print('Working on column: {}'.format(col))
         
         mean = df[col].mean()
         sd = df[col].std()
         
         df = df[(df[col] <= mean+(1.5*sd))]

    df.to_csv("temp.csv")
    return df

def missing_val(df):
   columns = list(df.columns.values)
   for col in columns:
      if is_numeric_dtype(df[col]):
         df[col].fillna(value= df[col].mean(), inplace=True)
      else :
         df[col].fillna(value= df[col].mode(), inplace=True)
   df.to_csv("temp.csv")

   return df


@app.route('/')
def upload_file():
   return render_template('index.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename("temp.csv"))
      df = pd.read_csv("temp.csv")

      return render_template('index.html',  tables=[df.head().to_html(classes='data', header="true")], desc= [df.describe().to_html(classes='data', header="true")] ,display = "Summary of Table",display1 = "Statistic Description of Table")

@app.route('/eda', methods = ['GET', 'POST'])
def eda():
   if request.method == 'POST':
     
      df = pd.read_csv("temp.csv")

      outl = request.form.get("outlier")
       
      if(outl == 'yes'):
        df = outlier(df)
        return render_template('index.html',  op = "Done with Outliers")

      if(outl == 'no'):
        return render_template('index.html',  op = "Skipped Outliers")

     

@app.route('/mv', methods = ['GET', 'POST'])
def mv():
   if request.method == 'POST':
     
      df = pd.read_csv("temp.csv")
      missingval = request.form.get("missingval")
      if(missingval == 'yes'):
        df = missing_val(df)
        
        return render_template('index.html',  mval = "Worked out missing values")

      if(missingval == 'no'):
        df = df
        return render_template('index.html',  mval = "Skipped Missing Values")


@app.route('/view')
def view():
   return render_template('view.html')


		
if __name__ == '__main__':
   app.run(debug = True)