## Interface for getting the Queue status of university restaurant online

#### Current status

- BE and FE in repository
- Site is up and running on siibs.swider.dev
- Site status and upcoming updates on site FAQ

#### Upcoming updates

- Data source to repo
- Pipeline for CI/CD serverside and datasource


#### How to use it

Detailed instructions for the data interface ground up setup will follow later.
For a more basic setup:
- Setup raspberry pi so that it autoconnects to the internet
- Install required packages from camReq.txt
- Set up a cron job for the scripts that are included *.sh files
- Cron should run as often as possible for the data source, check from btop how fast it can process cycles

For the serverside:
- Again more details will follow.
- Download scripts as they are
- run FEhost.js for hosting all the .html files
- uvicorn uvicorn api:app --port 5000 --proxy-headers | ts '[%H:%M:%S %d:%m:%Y]' >> apiLog.txt for the API and basic logging

