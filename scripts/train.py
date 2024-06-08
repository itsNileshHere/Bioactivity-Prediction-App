import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pickle
import subprocess

def lipinski_descriptors(canonical_smile):
    molecule = Chem.MolFromSmiles(canonical_smile)
    if molecule is None:
        return None
    mol_wt = Descriptors.MolWt(molecule)
    logp = Descriptors.MolLogP(molecule)
    h_donors = Descriptors.NumHDonors(molecule)
    h_acceptors = Descriptors.NumHAcceptors(molecule)
    return {
        "MolWt": mol_wt,
        "MolLogP": logp,
        "NumHDonors": h_donors,
        "NumHAcceptors": h_acceptors,
    }

def train_model(df4):
    df_lipinski = df4["canonical_smiles"].apply(lipinski_descriptors)
    df_lipinski = pd.DataFrame(df_lipinski.tolist())
    df_combined = pd.concat([df4, df_lipinski], axis=1)
    df_combined["IC50"] = pd.to_numeric(df_combined["IC50"])

    def pIC50(input):
        pIC50 = []
        for i in input["IC50"]:
            molar = i * (10**-9)
            pIC50.append(-np.log10(molar))
        input["pIC50"] = pIC50
        values = input.drop("IC50", axis=1)
        return values

    df_final = pIC50(df_combined)
    df3_selection = df_final[["canonical_smiles", "molecule_chembl_id"]]
    df3_selection.to_csv('../data/molecule.smi', sep='\t', index=False, header=False)

    padel_command = "java -Xms1G -Xmx1G -Djava.awt.headless=true -jar ../PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ../PaDEL-Descriptor/PubchemFingerprinter.xml -dir ../data -file ../data/descriptors_output.csv"
    subprocess.run(padel_command, shell=True)

    df3_X = pd.read_csv('../data/descriptors_output.csv')
    df3_X = df3_X.drop(columns=['Name'])
    df3_Y = df_final['pIC50']

    from sklearn.feature_selection import VarianceThreshold

    def remove_low_variance(input_data, threshold=0.1):
        selection = VarianceThreshold(threshold)
        selected_data = selection.fit_transform(input_data)
        selected_columns = input_data.columns[selection.get_support(indices=True)]
        return pd.DataFrame(selected_data, columns=selected_columns)

    df3_X = remove_low_variance(df3_X, threshold=0.1)

    # Save the list of selected descriptors
    with open('../data/descriptor_list.csv', 'w') as f:
        for col in df3_X.columns:
            f.write(f"{col}\n")

    X_train, X_test, Y_train, Y_test = train_test_split(df3_X, df3_Y, test_size=0.2)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)

    mse = mean_squared_error(Y_test.values, Y_pred)
    rsquare = r2_score(Y_test.values, Y_pred)

    print("Mean squared error (MSE):", round(mse, 2))
    print("Coefficient of Determination (R²):", round(rsquare, 2))

    pickle.dump(model, open("../model/SARS_coronavirus.pkl", "wb"))

if __name__ == "__main__":
    df4 = pd.read_csv('../data/preprocessed_data.csv')
    train_model(df4)
