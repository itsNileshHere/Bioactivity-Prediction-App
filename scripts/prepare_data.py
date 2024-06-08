import pandas as pd
from chembl_webresource_client.new_client import new_client

def calculate_bioactivity_threshold(standard_values):
    bioactivity_threshold = []
    for value in standard_values:
        if float(value) >= 10000:
            bioactivity_threshold.append("inactive")
        elif float(value) <= 1000:
            bioactivity_threshold.append("active")
        else:
            bioactivity_threshold.append("intermediate")
    return bioactivity_threshold

def preprocess_data():
    target = new_client.target
    target_query = target.search("coronavirus")
    targets = pd.DataFrame(target_query)
    selected_target = targets.target_chembl_id[6]
    activity = new_client.activity
    perform = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")
    df = pd.DataFrame(perform)
    df2 = df[df.standard_value.notna()]
    df2 = df2[df.canonical_smiles.notna()]
    df2 = df2.drop_duplicates(["canonical_smiles"])
    df2 = df2.reset_index(drop=True)
    selection = ["molecule_chembl_id", "canonical_smiles", "standard_value"]
    df3 = df2[selection]
    df3 = df3.rename(columns={"standard_value": "IC50"})
    bioactivity_class = calculate_bioactivity_threshold(df3["IC50"])
    bioactivity_class = pd.Series(bioactivity_class, name="class")
    df4 = pd.concat([df3, bioactivity_class], axis=1)
    df4.to_csv('../data/preprocessed_data.csv', index=False)
    return df4

if __name__ == "__main__":
    preprocess_data()
