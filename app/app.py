from flask import Flask, request, render_template, send_file, redirect, url_for
import pandas as pd
import subprocess
import os
import pickle
import base64

app = Flask(__name__)

def desc_calc():
    bashCommand = (
        "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ../PaDEL-Descriptor/PaDEL-Descriptor.jar "
        "-removesalt -standardizenitro -fingerprints -descriptortypes ../PaDEL-Descriptor/PubchemFingerprinter.xml "
        "-dir data -file data/descriptors_output.csv"
    )
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    os.remove('data/molecule.smi')

def build_model(input_data):
    with open('../model/SARS_coronavirus.pkl', 'rb') as f:
        model = pickle.load(f)
    prediction = model.predict(input_data)
    return prediction

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join('data', 'molecule.smi')
            file.save(filepath)
            
            load_data = pd.read_table(filepath, sep=' ', header=None)
            load_data.to_csv('data/molecule.smi', sep='\t', header=False, index=False)
            desc_calc()
            
            desc = pd.read_csv('data/descriptors_output.csv')
            with open('../data/descriptor_list.csv', 'r') as f:
                Xlist = f.read().splitlines()
            desc_subset = desc[Xlist]
            
            prediction = build_model(desc_subset)
            
            prediction_output = pd.Series(prediction, name='pIC50')
            molecule_name = pd.Series(load_data[1], name='molecule_name')
            result_df = pd.concat([molecule_name, prediction_output], axis=1)
            
            result_html = filedownload(result_df)
            
            return render_template('index.html', tables=[result_df.to_html(classes='data', header="true")], result_html=result_html)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
