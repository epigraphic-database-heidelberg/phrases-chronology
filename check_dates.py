import csv
import pysolr

solr = pysolr.Solr('http://localhost:8983/solr/edhText')
writer = csv.writer(open('dates_diff.csv', 'w', encoding='utf-8'))
writer.writerow(['hd_no', 'province', 'date_start_ln', 'date_end_ln', 'date_start_edh', 'date_end_edh'])

with open('LatinNow_DisManibvs_edh_only.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # skip first line
    cnt = 1
    for row in reader:
        hd_nr = row[4]
        date_start_ln = row[10].strip()
        date_end_ln = row[12].strip()
        results = solr.search('hd_nr:' + hd_nr)
        for result in results:
            try:
                date_start_edh = str(result['dat_jahr_a'][0]).strip()
            except KeyError:
                date_start_edh = '0'
            try:
                date_end_edh = str(result['dat_jahr_e'][0]).strip()
            except KeyError:
                date_end_edh = '0'
            province = result['provinz'][0].strip()
            if date_start_ln == date_end_ln and date_start_ln == date_start_edh:
                continue # EDH leaves date_end blank if identical to date_start
            if (date_start_ln != date_start_edh) or (date_end_ln != date_end_edh):
                writer.writerow([result['hd_nr'], province, date_start_ln, date_end_ln, date_start_edh, date_end_edh])
                cnt += 1



