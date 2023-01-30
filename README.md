# P4-LUCAT_API

The P4-LUCAT knowledge graph contains the data for Lung cancer patients. The main goal of a lung cancer data ecosystem in P4-LUCAT is to perform analysis that give oncologists insights
to improve the management of patients with lung cancer during their treatment, follow-up, and last period of life through data-driven techniques.

# 1) Drug-Drug Interactions (DDI) API

We are interested in computing the correlation between a DDI in treatment and the number of patients with a specific response to the treatment.
The treatment responses are evaluated in four categories: complete therapeutic response and stable disease are positive responses to treatment,
while partial therapeutic response and disease progression are negative responses. In this particular API, the lung cancer patients are extracted from the P4-LUCAT KG
based on the selected population from the Input form. For this particular population of lung cancer patients the API will output the following:
Treatment
Response 
Oncological Drugs
Non-Oncological Drugs
Drug-Drug Interactions

# Input

# Output




# 2) Horn Rules API

Mining Horn rules on top of knowledge graphs. The Horn rule consists of an atom that has variables at the subject or object position.
The Horn rule consists of a body with multiple atoms and a head with a single atom. In this particular API, the lung cancer patients are extracted from the P4-LUCAT KG
based on the selected population from the Input form. For this particular population of lung cancer patients the API will output the Horn rules that follow the selected population
and all the computed Metrics associated with this rules.


# Input

# Output