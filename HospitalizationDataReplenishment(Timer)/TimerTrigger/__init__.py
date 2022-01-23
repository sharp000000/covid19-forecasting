import os 
import datetime
import logging
import json
from urllib.request import urlopen
import pandas as pd
from azure.storage.blob import BlobServiceClient
import azure.functions as func
from io import StringIO

connstr = os.environ['connstr']

def get_blob_data(blob_client):
    """Returns a Pandas DataFrame with data from blob
    
    This function takes a blob_client object, uploads data from blob, and adjusts the data types for the columns
    """
    s = str(blob_client.download_blob().readall(),'utf-8')
    data = pd.read_csv(StringIO(s)).interpolate()
    data['Date']= data['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
    data['Hospitalization'] = data['Hospitalization'].astype(int)
    return data

def get_missing_dates(blob_client):
    """Returns a list with missing dates
    
    This function takes a blob_client_object, generates a list with dates depending on the last date in the blob, if it exists. 
    Otherwise generates the entire list of existing dates (from November 2020)
    """
    base = datetime.date(2020,11,16)
    
    if blob_client.exists():
        data = get_blob_data(blob_client)
        base = data['Date'].max()

    numdays = (datetime.date.today() - base).days
    date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
    dates = []
    [dates.append(i.strftime('%Y-%m-%d')) for i in date_list]
    return dates
    
def get_hospitalization_data(dates):
    """Returns a Pandas DataFrame with data to be added
    
    This function takes a list of dates, makes requests for data collection
    """
    hospitalization_df = pd.DataFrame()
    i = 0
    for date in dates:
        try:
            url = 'https://health-security.rnbo.gov.ua/api/beds/hospitalization/ranking?bedType=hospitalized&regionId=&otgId=&aggLevel=regions&date={}&hospitalType='.format(dates[i+1])
            response = urlopen(url)
            html_doc = response.read()
            hospitalization = json.loads(html_doc)['header']['i1'][0]
            hospitalization_df.loc[i,['Date','Hospitalization']] = [date,hospitalization] 
        except:
            continue
        i += 1

    return hospitalization_df

def main(mytimer: func.TimerRequest) -> None:
    """Returns None 

    Timer trigger function for daily data collection. Loads data from a blob, combines it with new data, and uploads the blob 
    """
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    blob_service_client = BlobServiceClient.from_connection_string(connstr)
    blob_client = blob_service_client.get_blob_client(container='hospitalization', blob='hospitalization.csv')

    if blob_client.exists():
        data = get_blob_data(blob_client)

    dates = get_missing_dates(blob_client)

    hospitalization_df = get_hospitalization_data(dates)

    blob_client.upload_blob(pd.concat([data,hospitalization_df.interpolate()]).to_csv(index=False),overwrite=True)
