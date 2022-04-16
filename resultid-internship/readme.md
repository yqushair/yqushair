## Resultid Internship

This folder contains code that I developed for my internship with Resultid.

Resultid is an AI-powered business intelligence company whose platform allows for automated market assessments of new technologies. The platform synthesizes data from patents, grants, market data, and company information, enabling investors and market researchers to make better-informed evaluations of early-stage innovations.

From January 2021 to March 2021, I worked with Resultid as a natural language processing (NLP) intern. Over the course of my internship, I developed code that allows for automated extraction of the names of a company's competitors given the company's 10-K financial report.

💬 According to Resultid's NLP Research Lead, the named entity recognition (NER) model that I developed:
> - "is the center of a module that helped build out Resultid's MVP by demonstrating and proving out discrete usage of an NLP model for informing larger data narratives."
> - "is now a central module in the data ingestion step in the developing platform."
> - "laid the groundwork for future development on that module and adjacent ones through clear and precise engineering choices on Yanal's part."

🗄 Included above are each of the following files:
- `basic_ner_test.py`: the pipeline's main file and entry point. A company's 10-K report is supplied via command line, and a list of competitors found in the report is outputted, with the competitors' names and company IDs as found in Resultid's company database (if applicable).
- `company.py`: code defining the "Company" class and associated methods.
- `resultid_es_query.py`: defines the `crunchbase_query(queryString)` function which queries Resultid's Crunchbase database for potential matches to the provided `queryString`. The structure of the returned result is outlined in the file's comments.
- `run.py`: short script that passes each of the available 10-K reports to the NER model.
- `out.txt`: sample output containing the competitors of Guided Therapeutics, Inc. as extracted from their 10-K report.
- `guided_10k.txt`: the 10-K report belonging to Guided Therapeutics, Inc. from which the competitors found in `out.txt` were extracted.
