<h1> Forecasting the Spread of COVID-19 in Ukraine using hospitalization data </h1>

<p>🇺🇦 Due to the war, the government website is down but you can go to another one and <a href="help us">https://health-security.rnbo.gov.ua/</a>🇺🇦</p>

<p>Data ingestion was done from ukrainian state resource: <a href="https://health-security.rnbo.gov.ua/">https://health-security.rnbo.gov.ua/</a><br> For extracting data on a daily basis was created <a href="https://github.com/sharp000000/covid19-forecasting/tree/master/HospitalizationDataReplenishment(Timer)">python Azure Function</a> with timer trigger configured using CRON expression 0 0 7 * * *</p> 

<p>For forecasting was developed serverless API using <a href="https://github.com/sharp000000/covid19-forecasting/tree/master/HospitalizationForecast">HTTP triggered Azure Function</a></p>
<p>Three methods were used for forecasting: 
<br>  – ARIMA 
<br>  – XGBoost 
<br>  – Custom algorithm, which on the basis of the basic forecast adjusts the results in accordance with similar time series in the past
 </p>
<img width="640" alt="Picture2" src="https://user-images.githubusercontent.com/35422257/130325006-2349cf11-4d40-4d4a-bd66-b86cdec59093.png">

<p><a href="https://github.com/sharp000000/covid19-forecasting-web">Web application</a> development was done using Angular 11 framework</p>
<img width="640" alt="Picture1" src="https://user-images.githubusercontent.com/35422257/130324524-de82487a-3315-44c9-9b22-6a001a0f59cd.png"> 

<h3> Project architecture </h3>
<img class="center" width="640" alt="Architecture" src="https://user-images.githubusercontent.com/35422257/129712267-e26cd4f5-d703-4dcb-9ce6-c5386d1c6901.png">
