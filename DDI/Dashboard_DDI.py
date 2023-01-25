import json
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON


def query_generation(input_data, endpoint):
    where_clause = {
        "Gender": """?patient <http://research.tib.eu/p4-lucat/vocab/hasGender> ?gender. """,
        "Smoking Habit": """?patient <http://research.tib.eu/p4-lucat/vocab/hasSmokingHabit> ?smoking.  """,
        "Organ affected by the familiar cancer": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                                    ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                    ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer.  """,
        "Cancer Stage": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. """,
        "Histology": """OPTIONAL{?patient <http://research.tib.eu/p4-lucat/vocab/hasCUIAnnotation> ?histologycui.
                                 ?histologycui a <http://research.tib.eu/p4-lucat/vocab/Histology> .
                                 ?histologycui <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology.""",
        "ALK gene/Immunohistochemistry/Positive": """OPTIONAL{?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "ALK"))
                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "IHQ positivo")).} \n""",
        "ALK gene/Fluorescent in Situ Hybridization/ALK Gene Translocation": """OPTIONAL{?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                                ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                                ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                                ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "ALK"))
                                                                                ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "FISH traslocado")).} \n""",
        "Epidermal Growth Factor Receptor/EGFR T790M Mutation Negative": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "T790M -")). }\n""",
        "Epidermal Growth Factor Receptor/EGFR T790M Mutation Positive Non-Small Cell Lung Carcinoma": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                                                          ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                                                          ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                                                          ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                                                          ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (ucase(str(?biomarker_result))= "T790M +").} \n""",
        "Epidermal Growth Factor Receptor/EGFR Exon 19 Mutation": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Exón 19")). }\n""",
        "Epidermal Growth Factor Receptor/EGFR Exon 21 Mutation": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Exón 21")).} \n""",
        "BRAF gene/Detected (finding)": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                           ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                           ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                           ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "BRAF"))
                                           ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Se detecta")). }\n""",
        "KRAS gene/Not detected": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                     ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "KRAS"))
                                     ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "No se detecta")).} \n""",
        "PDL1 Positive": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "PDL1"))
                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Positivo")).} \n""",
        "PDL1 Negative": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                            ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "PDL1"))
                            ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Negativo")).} \n""",
        "PDL1 Unkown": """OPTIONAL{ ?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                          ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                          ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                          ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "PDL1"))
                          ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Desconocido")).} \n""",
    }


    query_select_clause = "SELECT DISTINCT ?patient ?treatmentID ?responseDesc ?drugLabel ?DrugCategory ?DDI_Literature ?DDI_DeductiveSystem ?DDI_DrugBank"
    query_where_clause = """\n WHERE { \n ?patient a <http://research.tib.eu/p4-lucat/vocab/LCPatient> .\n"""

    if "Gender" in input_data["Input"]["Variables"]:
        query_where_clause = query_where_clause + where_clause["Gender"]+ "FILTER (regex(?gender,\"" + input_data["Input"]["Variables"]["Gender"] + "\"))." + " \n"
    if "Smoking Habit" in input_data["Input"]["Variables"]:
        query_where_clause = query_where_clause + where_clause["Smoking Habit"] + "FILTER (regex(?smoking,\"" + input_data["Input"]["Variables"]["Smoking Habit"] + "\"))." + " \n"
    if "Organ affected by the familiar cancer" in input_data["Input"]["Variables"]:
        query_where_clause = query_where_clause + where_clause["Organ affected by the familiar cancer"] + "FILTER (regex(?familycancer,\"" + input_data["Input"]["Variables"]["Organ affected by the familiar cancer"] + "\" ))." + " \n"
    if "Cancer Stage" in input_data["Input"]["Variables"]:
        query_where_clause = query_where_clause + where_clause["Cancer Stage"] + "FILTER (regex(?stage,\"" + input_data["Input"]["Variables"]["Cancer Stage"] + "\"))." + " \n"
    if "Histology" in input_data["Input"]["Variables"]:
        query_where_clause = query_where_clause + where_clause["Histology"] + "FILTER (regex(?histology,\"" + input_data["Input"]["Variables"]["Histology"] + "\")).}" + " \n"
    if "ALK gene/Immunohistochemistry/Positive" in input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause["ALK gene/Immunohistochemistry/Positive"] + " \n"
    if "ALK gene/Fluorescent in Situ Hybridization/ALK Gene Translocation" in input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause["ALK gene/Fluorescent in Situ Hybridization/ALK Gene Translocation"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR T790M Mutation Negative" in input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause["Epidermal Growth Factor Receptor/EGFR T790M Mutation Negative"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR T790M Mutation Positive Non-Small Cell Lung Carcinoma" in input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause["Epidermal Growth Factor Receptor/EGFR T790M Mutation Positive Non-Small Cell Lung Carcinoma"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR Exon 19 Mutation" in input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause["Epidermal Growth Factor Receptor/EGFR Exon 19 Mutation"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR Exon 21 Mutation" in input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause["Epidermal Growth Factor Receptor/EGFR Exon 21 Mutation"] + " \n"
    if "KRAS gene/Not detected" in input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause["KRAS gene/Not detected"] + " \n"
    if "BRAF gene/Detected (finding)" in input_data["Input"]["Variables"]["Molecular Markers"]:
        query_where_clause = query_where_clause + where_clause["BRAF gene/Detected (finding)"] + " \n"
    if "PDL1 Positive" in input_data["Input"]["Variables"]["PDL1 result"]:
        query_where_clause = query_where_clause + where_clause["PDL1 Positive"] + " \n"
    if "PDL1 Negative" in input_data["Input"]["Variables"]["PDL1 result"]:
        query_where_clause = query_where_clause + where_clause["PDL1 Negative"] + " \n"
    if "PDL1 Unknown" in input_data["Input"]["Variables"]["PDL1 result"]:
        query_where_clause = query_where_clause + where_clause["PDL1 Unknown"] + " \n"

    query_where_clause = query_where_clause + """
    {?patient <http://research.tib.eu/p4-lucat/vocab/hasDrugLabel> ?drugLabel. bind( if(?drugLabel,"OnCologicalDrug","NonOncologicalDrug") as ?DrugCategory ). } 
     UNION
    {?patient <http://research.tib.eu/p4-lucat/vocab/hasNonOncologicalDrug> ?DrugBankID.
    ?DrugBankID <http://research.tib.eu/p4-lucat/vocab/drugLabel> ?drugLabel. bind( if(?drugLabel,"NonOnCologicalDrug","OncologicalDrug") as ?DrugCategory ).}    
    ?id <http://research.tib.eu/p4-lucat/vocab/hasResponsePatient> ?patient.
    ?id <http://research.tib.eu/p4-lucat/vocab/hasResponseResponse> ?response.
    ?response <http://research.tib.eu/p4-lucat/vocab/responseDescription> ?responseDesc .
    ?id <http://research.tib.eu/p4-lucat/vocab/hasResponseTreatment> ?treatmentID .
    ?treatmentID   <http://research.tib.eu/p4-lucat/vocab/hasTreatmentDrug> ?drugBankID .
    ?treatmentID   <http://research.tib.eu/p4-lucat/vocab/hasDDIs_Literature> ?DDI_Literature .
    ?treatmentID   <http://research.tib.eu/p4-lucat/vocab/hasDDIs_DeductiveSystem> ?DDI_DeductiveSystem .
    ?treatmentID   <http://research.tib.eu/p4-lucat/vocab/hasDDIs_DrugBank> ?DDI_DrugBank .\n
                                 } """
    # ?drugBankID <http://research.tib.eu/p4-lucat/vocab/drugLabel> ?drugLabel.
    sparqlQuery = query_select_clause + " " + query_where_clause
    #print(sparqlQuery)

    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(sparqlQuery)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = results["results"]["bindings"]
    # print(type(data))

    out = []

    for row in data:
        newrow = (row["patient"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
        newrow = newrow + ","+(row["responseDesc"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
        newrow = newrow + ","+(row["treatmentID"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
        newrow = newrow + ","+(row["drugLabel"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
        newrow = newrow + "," + (row["DrugCategory"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
        newrow = newrow + ","+(row["DDI_Literature"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
        newrow = newrow + ","+(row["DDI_DeductiveSystem"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
        newrow = newrow + ","+(row["DDI_DrugBank"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")

        out.append(newrow + '\n')

    d = [x.strip().split("\n") for x in out]
    df = pd.DataFrame(d)
    data = list(df[0].apply(lambda x: x.split(",")))
    return data


def writeJSON(data):
    df = pd.DataFrame(data,columns=['PatientID','Response','TreatmentID','Drugs','DrugCategory','DDI_Literature','DDI_DeductiveSystem','DDI_DrugBank'])

    def onco(x):
        if x['DrugCategory'] == 'OnCologicalDrug':
            return x['Drugs']

    def nononco(x):
        if x['DrugCategory'] == 'NonOnCologicalDrug':
            return x['Drugs']

    df['OncologicalDrugs'] = df.apply(onco, axis=1)
    df['NonOncologicalDrugs'] = df.apply(nononco, axis=1)

    def grp(x):
        return x.groupby('TreatmentID').apply(lambda x: [x.groupby('Response').apply(
            lambda x: x[['OncologicalDrugs','NonOncologicalDrugs', 'DDI_Literature', 'DDI_DeductiveSystem', 'DDI_DrugBank']]
                                        .to_dict('records')).to_dict()]).to_dict()

    res = [df.groupby('PatientID').apply(grp).to_dict()]
    return res
    #with open('data_modified.json', 'w') as f:
        #json.dump(res, f, indent=4)


def read_process(input_file):
    with open(input_file, "r") as input_file_descriptor:
        input_data = json.load(input_file_descriptor)
        data_frame = query_generation(input_data, "https://labs.tib.eu/sdm/p4lucat_kg/sparql")
        writeJSON(data_frame)
        return data_frame

def run_api(json_input,endpoint):
    data_frame = query_generation(json_input, endpoint)
    return writeJSON(data_frame)
#if __name__ == '__main__':
    #res = read_process("inputfile-DDI.json")
