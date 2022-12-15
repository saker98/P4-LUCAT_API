import pandas as pd
import json
import re

rule = []
data = []
variables = []
met = []

def createTable(variables, rule, filtered_data):
    for col in filtered_data.columns:
        if col == 'Head Coverage':
            values = filtered_data[col].values.tolist()
            met.append((col, values))
        if col == 'PCA Confidence':
            values = filtered_data[col].values.tolist()
            met.append((col, values))

    result = pd.DataFrame(
        {'Variable': pd.Series(variables), 'Values': pd.Series(rule), 'Metrics': pd.Series(met)})

    return result

def match(df,rule):
    data = df[df.Rule.map(set(rule).issubset)]
    data.reset_index(drop=True, inplace=True)
    return data



def extract(df):
    for index, row in df.iterrows():
        foundRule = re.findall(r"<(.*?)>", row['Rule'])
        data1 = [foundRule, row['Head Coverage'], row['Std Confidence'], row['PCA Confidence'],row['Positive Examples'], row['Body size'], row['PCA Body size']]
        data.append(data1)
    new_df = pd.DataFrame(data, columns=['Rule', 'Head Coverage','Std Confidence','PCA Confidence','Positive Examples','Body size','PCA Body size'])
    return new_df


def read_json(input_file):
    with open(input_file, "r") as input_file_descriptor:
        input_data = json.load(input_file_descriptor)
        for val in input_data['Variables']:
            variables.append(val)
        for val in input_data['Values']:
            rule.append(val)
    return variables,rule


if __name__ == '__main__':
    variables,rule  = read_json("input-file-Rules.json")
    df = pd.read_csv("all_data_dashboard-trial.csv")
    data = extract(df)
    r = list(filter(None, rule))
    filtered_data = match(data,r)
    result = createTable(variables, rule, filtered_data)
    print(result)
    # result.to_csv("Metrics.csv", index=False)
    # plot(filtered_data, plot_val)



