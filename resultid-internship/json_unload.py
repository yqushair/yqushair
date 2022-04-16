import json

f = open('mass_dump\scraped_data_sec_filing_202103152005.json', encoding ='utf-8')
j = json.load(f)['scraped_data_sec_filing']

for entry in j:
    write = open('securitybank.txt', 'w', encoding='utf-8')
    write.write(entry['scraped_text'])