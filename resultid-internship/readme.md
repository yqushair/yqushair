## Resultid Internship

This folder contains code that I developed for my internship with Resultid.

Resultid is an AI-powered business intelligence company whose platform allows for automated market assessments of new technologies. The platform synthesizes data from patents, grants, market data, and company information, enabling investors and market researchers to make better-informed evaluations of early-stage innovations.

From January 2021 to March 2021, I worked with Resultid as a natural language processing (NLP) intern. Over the course of my internship, I developed code that allows for automated extraction of the names of a company's competitors given the company's 10-K financial report.

You can access each of the following files:
- `basic_ner_test.py`: the pipeline's main file and entry point. A company's 10-K report is supplied via command line, and a list of competitors found in the report is outputted, with the competitors' names and company IDs as found in Resultid's company database (if applicable).
- `company.py`: code defining the "Company" class and associated methods.
- `resultid_es_query.py`: defines the `crunchbase_query(queryString)` function which queries Resultid's Crunchbase database for potential matches to the provided `queryString`. The structure of the returned result is outlined in the file's comments.
- `test.py`: short script that passes each of the available 10-K reports to the named entity recognition (NER) pipeline.
