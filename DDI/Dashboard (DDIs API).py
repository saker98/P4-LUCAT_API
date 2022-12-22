import json
import operator
import itertools
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON


def query_generation(input_data, endpoint):
    where_clause = {
        "Male": """?patient <http://research.tib.eu/p4-lucat/vocab/hasGender> ?gender. FILTER (regex(?gender, "Male")). \n""",
        "Female": """?patient <http://research.tib.eu/p4-lucat/vocab/hasGender> ?gender. FILTER (regex(?gender, "Female")). \n""",
        "CurrentSmoker": """?patient <http://research.tib.eu/p4-lucat/vocab/hasSmokingHabit> ?smoking. FILTER (regex(?smoking, "CurrentSmoker")). \n""",
        "FormerSmoker": """?patient <http://research.tib.eu/p4-lucat/vocab/hasSmokingHabit> ?smoking. FILTER (regex(?smoking, "FormerSmoker")). \n""",
        "NonSmoker": """?patient <http://research.tib.eu/p4-lucat/vocab/hasSmokingHabit> ?smoking. FILTER (regex(?smoking, "NonSmoker")). \n""",
        "UnKnown": """?patient <http://research.tib.eu/p4-lucat/vocab/hasSmokingHabit> ?smoking. FILTER (regex(?smoking, "UnKnown")). \n""",
        "UNK": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                               ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                               ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "UNK")). \n""",
        "Head_and_Neck": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                   ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                   ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Head_and_Neck")). \n""",
        "Colorectal": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Colorectal")). \n""",
        "Esophagus_Gastric": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Esophagus_Gastric")). \n""",
        "Liver": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Liver")). \n""",
        "Leukemia": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Leukemia")). \n""",
        "Lymphoma": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Lymphoma")). \n""",
        "Breast": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                       ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Breast")). \n""",
        "Melanoma": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Melanoma")). \n""",
        "Others": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Others")). \n""",
        "Skin_no_melanoma": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Skin_no_melanoma")). \n""",
        "Prostate": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Prostate")). \n""",
        "Lung": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Lung")). \n""",
        "Pancreas": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Pancreas")). \n""",
        "Renal": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                           ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Renal")). \n""",
        "Central_Nervous_System": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Central_Nervous_System")). \n""",
        "Sarcoma": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Sarcoma")). \n""",
        "Germ_tumor": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Germ_tumor")). \n""",
        "Bladder_Urinary_Tract": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Bladder_Urinary_Tract")). \n""",
        "Gallbladder": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Gallbladder")). \n""",
        "Uterus_Cervix": """?family a <http://research.tib.eu/p4-lucat/vocab/Patient_Cancer_Family>.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                               ?family <http://research.tib.eu/p4-lucat/vocab/hasFamiliarCancer> ?familycancer. FILTER (regex(?familycancer, "Uterus_Cervix")). \n""",
        "Limitado": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "Limitado")).\n""",
        "Extendido": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "Extendido")).\n""",
        "IA": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IA")).\n""",
        "IA1": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IA1")).\n""",
        "IA2": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IA2")).\n""",
        "IB": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IB")).\n""",
        "IIA": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IIA")).\n""",
        "IIB": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IIB")).\n""",
        "IIIA": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IIIA")).\n""",
        "IIIB": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IIIB")).\n""",
        "IIIC": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IIIC")).\n""",
        "IV": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IV")).\n""",
        "IVA": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IVA")).\n""",
        "IVB": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "/IVB")).\n""",
        "Otros": """?patient <http://research.tib.eu/p4-lucat/vocab/hasStage> ?stage. FILTER (regex(?stage, "Otros")).\n""",
        "Adenocarcinoma": """?diag a <http://research.tib.eu/p4-lucat/vocab/Diagnosis> .
                                         ?diag <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology. 
                                         FILTER (regex(?histology, "adenocarcinoma")). \n""",
        "Small cell carcinoma of lung": """?diag a <http://research.tib.eu/p4-lucat/vocab/Diagnosis> .
                                             ?diag <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology. 
                                             FILTER (regex(?histology, "small_cell_carcinoma_of_lung")). \n""",
        "Carcinoma, Large Cell": """?diag a <http://research.tib.eu/p4-lucat/vocab/Diagnosis> .
                                             ?diag <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology. 
                                             FILTER (regex(?histology, "carcinoma,_large_cell")). \n""",
        "Squamous cell carcinoma": """?diag a <http://research.tib.eu/p4-lucat/vocab/Diagnosis> .
                                             ?diag <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology. 
                                             FILTER (regex(?histology, "squamous_cell_carcinoma")). \n""",
        "Not Otherwise Specified": """?diag a <http://research.tib.eu/p4-lucat/vocab/Diagnosis> .
                                             ?diag <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology. 
                                             FILTER (regex(?histology, "not_otherwise_specified")). \n""",
        "Undifferentiated": """?diag a <http://research.tib.eu/p4-lucat/vocab/Diagnosis> .
                                             ?diag <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology. 
                                             FILTER (regex(?histology, "undifferentiated")). \n""",
        "large cell neuroendocrine carcinoma of lung": """?diag a <http://research.tib.eu/p4-lucat/vocab/Diagnosis> .
                                             ?diag <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology. 
                                             FILTER (regex(?histology, "large_cell_neuroendocrine_carcinoma_of_lung")). \n""",
        "Adenosquamous carcinoma": """?diag a <http://research.tib.eu/p4-lucat/vocab/Diagnosis> .
                                             ?diag <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology. 
                                             FILTER (regex(?histology, "adenosquamous_carcinoma")). \n""",
        "Carcinoid Tumor": """?diag a <http://research.tib.eu/p4-lucat/vocab/Diagnosis> .
                                             ?diag <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology. 
                                             FILTER (regex(?histology, "carcinoid_tumor")). \n""",
        "Squamous cell carcinoma, spindle cell": """?diag a <http://research.tib.eu/p4-lucat/vocab/Diagnosis> .
                                                 ?diag <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology. 
                                                 FILTER (regex(?histology, "squamous_cell_carcinoma,_spindle_cell")). \n""",
        "Others": """?diag a <http://research.tib.eu/p4-lucat/vocab/Diagnosis> .
                                 ?diag <http://research.tib.eu/p4-lucat/vocab/histologyLabel_ENG> ?histology. 
                                 FILTER (regex(?histology, "null_value")). \n""",
        "ALK gene/Immunohistochemistry/Positive": """?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "ALK"))
                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "IHQ positivo")). \n""",
        "ALK gene/Fluorescent in Situ Hybridization/ALK Gene Translocation": """?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "ALK"))
                                                                ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "FISH traslocado")). \n""",
        "Epidermal Growth Factor Receptor/EGFR T790M Mutation Negative": """?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "T790M -")). \n""",
        "Epidermal Growth Factor Receptor/EGFR T790M Mutation Positive Non-Small Cell Lung Carcinoma": """?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (ucase(str(?biomarker_result))= "T790M +"). \n""",
        "Epidermal Growth Factor Receptor/EGFR Exon 19 Mutation": """?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Exón 19")). \n""",
        "Epidermal Growth Factor Receptor/EGFR Exon 21 Mutation": """?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "EGFR"))
                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Exón 21")). \n""",
        "BRAF gene/Detected (finding)": """?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                                ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                                ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                                ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "BRAF"))
                                                                                ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Se detecta")). \n""",
        "KRAS gene/Not detected": """?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                                ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                                ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                                ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "KRAS"))
                                                                                ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "No se detecta")). \n""",
        "PDL1 Positive": """?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "PDL1"))
                                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Positivo")). \n""",
        "PDL1 Negative": """?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "PDL1"))
                                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Negativo")). \n""",
        "PDL1 Unkown": """?marker a  <http://research.tib.eu/p4-lucat/vocab/Diagnosis_Markers>.
                                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasID_LCPatient> ?patient.
                                                                                        ?marker <http://research.tib.eu/p4-lucat/vocab/hasIDMarker> ?markerid.
                                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkers> ?biomarker. FILTER (regex(?biomarker, "PDL1"))
                                                                                        ?markerid <http://research.tib.eu/p4-lucat/vocab/hasMolecularMarkersResult> ?biomarker_result. FILTER (regex(?biomarker_result, "Desconocido")). \n""",

    }

    query_select_clause = "SELECT DISTINCT ?patientID ?treatmentID ?responseDesc ?drugLabel ?DDI_Literature ?DDI_DeductiveSystem ?DDI_DrugBank"
    query_where_clause = """WHERE { ?patient a <http://research.tib.eu/p4-lucat/vocab/LCPatient> .\n"""

    if "Male" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Male"] + " \n"
        # query_select_clause = query_select_clause + "?patient"
    if "Female" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Female"] + " \n"
    if "CurrentSmoker" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["CurrentSmoker"] + " \n"
    if "FormerSmoker" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["FormerSmoker"] + " \n"
    if "NonSmoker" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["NonSmoker"] + " \n"
    if "UnKnown" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["UnKnown"] + " \n"
    if "UNK" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["UNK"] + " \n"
    if "Head_and_Neck" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Head_and_Neck"] + " \n"
    if "Colorectal" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Colorectal"] + " \n"
    if "Esophagus_Gastric" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Esophagus_Gastric"] + " \n"
    if "Liver" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Liver"] + " \n"
    if "Leukemia" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Leukemia"] + " \n"
    if "Lymphoma" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Lymphoma"] + " \n"
    if "Breast" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Breast"] + " \n"
    if "Melanoma" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Melanoma"] + " \n"
    if "Others" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Others"] + " \n"
    if "Skin_no_melanoma" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Skin_no_melanoma"] + " \n"
    if "Prostate" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Prostate"] + " \n"
    if "Lung" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Lung"] + " \n"
    if "Pancreas" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Pancreas"] + " \n"
    if "Renal" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Renal"] + " \n"
    if "Central_Nervous_System" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Central_Nervous_System"] + " \n"
    if "Sarcoma" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Sarcoma"] + " \n"
    if "Germ_tumor" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Germ_tumor"] + " \n"
    if "Bladder_Urinary_Tract" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Bladder_Urinary_Tract"] + " \n"
    if "Gallbladder" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Gallbladder"] + " \n"
    if "Uterus_Cervix" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Uterus_Cervix"] + " \n"
    if "Limitado" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Limitado"] + " \n"
    if "Extendido" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Extendido"] + " \n"
    if "IA" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IA"] + " \n"
    if "IA1" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IA1"] + " \n"
    if "IA2" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IA2"] + " \n"
    if "IB" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IB"] + " \n"
    if "IIA" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IIA"] + " \n"
    if "IIB" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IIB"] + " \n"
    if "IIIA" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IIIA"] + " \n"
    if "IIIB" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IIIB"] + " \n"
    if "IIIC" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IIIC"] + " \n"
    if "IV" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IV"] + " \n"
    if "IVA" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IVA"] + " \n"
    if "IVB" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["IVB"] + " \n"
    if "Otros" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Otros"] + " \n"
    if "Adenocarcinoma" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Adenocarcinoma"] + " \n"
    if "Small cell carcinoma of lung" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Small cell carcinoma of lung"] + " \n"
    if "Carcinoma, Large cell" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Carcinoma, Large cell"] + " \n"
    if "Squamous cell carcinoma" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Squamous cell carcinoma"] + " \n"
    if "Not Otherwise Specified" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Not Otherwise Specified"] + " \n"
    if "Undifferentiated" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Undifferentiated"] + " \n"
    if "large cell neuroendocrine carcinoma of lung" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["large cell neuroendocrine carcinoma of lung"] + " \n"
    if "Adenosquamous carcinoma" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Adenosquamous carcinoma"] + " \n"
    if "Carcinoid Tumor" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Carcinoid Tumor"] + " \n"
    if "Squamous cell carcinoma, spindle cell" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Squamous cell carcinoma, spindle cell"] + " \n"
    if "Others" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["Others"] + " \n"
    if "ALK gene/Immunohistochemistry/Positive" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["ALK gene/Immunohistochemistry/Positive"] + " \n"
    if "ALK gene/Fluorescent in Situ Hybridization/ALK Gene Translocation" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause[
            "ALK gene/Fluorescent in Situ Hybridization/ALK Gene Translocation"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR T790M Mutation Negative" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause[
            "Epidermal Growth Factor Receptor/EGFR T790M Mutation Negative"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR T790M Mutation Positive Non-Small Cell Lung Carcinoma" in input_data[
        "Values"]:
        query_where_clause = query_where_clause + where_clause[
            "Epidermal Growth Factor Receptor/EGFR T790M Mutation Positive Non-Small Cell Lung Carcinoma"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR Exon 19 Mutation" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause[
            "Epidermal Growth Factor Receptor/EGFR Exon 19 Mutation"] + " \n"
    if "Epidermal Growth Factor Receptor/EGFR Exon 21 Mutation" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause[
            "Epidermal Growth Factor Receptor/EGFR Exon 21 Mutation"] + " \n"
    if "KRAS gene/Not detected" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["KRAS gene/Not detected"] + " \n"
    if "BRAF gene/Detected (finding)" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["BRAF gene/Detected (finding)"] + " \n"
    if "PDL1 Positive" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["PDL1 Positive"] + " \n"
    if "PDL1 Negative" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["PDL1 Negative"] + " \n"
    if "PDL1 Unknown" in input_data["Values"]:
        query_where_clause = query_where_clause + where_clause["PDL1 Unknown"] + " \n"

    query_where_clause = query_where_clause + """?id <http://research.tib.eu/p4-lucat/vocab/hasResponsePatient> ?patient. 
                                 BIND(REPLACE(STR(?patient),"http://research.tib.eu/p4-lucat/entity/","") AS ?patientID) .
                                 ?id <http://research.tib.eu/p4-lucat/vocab/hasResponseResponse> ?response. 
                                 ?response <http://research.tib.eu/p4-lucat/vocab/responseDescription> ?responseDescNew . 
                                 BIND(REPLACE(STR(?responseDescNew),"http://research.tib.eu/p4-lucat/entity/","") AS ?responseDesc) .
                                 ?id <http://research.tib.eu/p4-lucat/vocab/hasResponseTreatment> ?treatmentIDNew . 
                                 BIND(REPLACE(STR(?treatmentIDNew),"http://research.tib.eu/p4-lucat/entity/","") AS ?treatmentID) .
                                 ?treatmentIDNew   <http://research.tib.eu/p4-lucat/vocab/hasTreatmentDrug> ?drugBankID .
                                 ?drugBankID <http://research.tib.eu/p4-lucat/vocab/drugLabel> ?drugLabel. 
                                 BIND(REPLACE(STR(?drugLabelNew),"http://research.tib.eu/p4-lucat/entity/","") AS ?drugLabel) .
                                 ?treatmentIDNew <http://research.tib.eu/p4-lucat/vocab/hasDDIs_Literature> ?DDI_LiteratureNew.
                                 BIND(REPLACE(STR(?DDI_LiteratureNew),"http://research.tib.eu/p4-lucat/entity/","") AS ?DDI_Literature) .
                                 ?treatmentIDNew <http://research.tib.eu/p4-lucat/vocab/hasDDIs_DeductiveSystem> ?DDI_DeductiveSystemNew.
                                 BIND(REPLACE(STR(?DDI_DeductiveSystemNew),"http://research.tib.eu/p4-lucat/entity/","") AS ?DDI_DeductiveSystem) .
                                 ?treatmentIDNew <http://research.tib.eu/p4-lucat/vocab/hasDDIs_DrugBank> ?DDI_DrugBankNew.
                                 BIND(REPLACE(STR(?DDI_DrugBankNew),"http://research.tib.eu/p4-lucat/entity/","") AS ?DDI_DrugBank) .
                                  
                                 } """
    sparqlQuery = query_select_clause + " " + query_where_clause
    # print(sparqlQuery)


    # query_where_clause = """?id <http://research.tib.eu/p4-lucat/vocab/hasResponsePatient> ?patient.
    #                              ?id <http://research.tib.eu/p4-lucat/vocab/hasResponseResponse> ?response.
    #                              ?response <http://research.tib.eu/p4-lucat/vocab/responseDescription> ?responseDesc .
    #                              ?id <http://research.tib.eu/p4-lucat/vocab/hasResponseTreatment> ?treatmentID .
    #                              ?treatmentID   <http://research.tib.eu/p4-lucat/vocab/hasDDIs_Literature> ?DDI_Literature .
    #                              ?treatmentID   <http://research.tib.eu/p4-lucat/vocab/hasDDIs_DeductiveSystem> ?DDI_DeductiveSystem .
    #                              ?treatmentID   <http://research.tib.eu/p4-lucat/vocab/hasDDIs_DrugBank> ?DDI_DrugBank .
    #                              ?treatmentID   <http://research.tib.eu/p4-lucat/vocab/hasTreatmentDrug> ?drugBankID .
    #                              ?drugBankID <http://research.tib.eu/p4-lucat/vocab/drugLabel> ?drugLabel. \n """

    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(sparqlQuery)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = results["results"]["bindings"]
    # print(type(data))
    # print(data)

    # out = []
    #
    # for row in data:
    #     # newrow = (row["patient"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
    #     newrow = (row["responseDesc"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
    #     newrow = newrow + ","+(row["treatmentID"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
    #     newrow = newrow + ","+(row["drugLabel"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
    #     # newrow = newrow + ","+(row["DDI_Literature"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
    #     # newrow = newrow + ","+(row["DDI_DeductiveSystem"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
    #     # newrow = newrow + ","+(row["DDI_DrugBank"]["value"]).replace("http://research.tib.eu/p4-lucat/entity/", "")
    #
    #     out.append(newrow + '\n')
    #
    # d = [x.strip().split("\n") for x in out]
    # df = pd.DataFrame(d)
    # data = list(df[0].apply(lambda x: x.split(",")))
    # # print(data)
    return data



def writeJSON(data):
    jsonString = json.dumps(data, indent=4)
    jsonFile = open("DDI_output.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()



def read_process(input_file):
    with open(input_file, "r") as input_file_descriptor:
        input_data = json.load(input_file_descriptor)
        data_frame = query_generation(input_data, "https://labs.tib.eu/sdm/p4lucat_kg/sparql")
        writeJSON(data_frame)
        return data_frame


if __name__ == '__main__':
    res = read_process("inputfile-DDI.json")
