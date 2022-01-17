import datetime
import logging
import json
from urllib.request import urlopen
import pandas as pd
from azure.storage.blob import BlobServiceClient
import azure.functions as func
import os

connstr = os.environ["connstr"]

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    base = datetime.datetime(2020,11,16)
    numdays = (datetime.datetime.now() - base).days
    date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]

    dates = []
    for i in date_list:
        dates.append(i.strftime("%Y-%m-%d"))

    hospitalization_df = pd.DataFrame()
    i = 0
    for date in dates:
        try:
            url = 'https://health-security.rnbo.gov.ua/api/beds/hospitalization/ranking?bedType=hospitalized&regionId=&otgId=&aggLevel=regions&date={}&hospitalType='.format(dates[i+1])
            response = urlopen(url)
            html_doc = response.read()
            hospitalization = json.loads(html_doc)['header']['i1'][0]
            hospitalization_df = pd.concat([hospitalization_df,pd.DataFrame({'Date':date,'Hospitalization':hospitalization},index=[0])])
        except:
            continue
        i = i + 1
    blob_service_client = BlobServiceClient.from_connection_string(connstr)
    blob_client = blob_service_client.get_blob_client(container='hospitalization', blob='hospitalization.csv')
    blob_client.upload_blob(hospitalization_df.to_csv(index=False),overwrite=True)