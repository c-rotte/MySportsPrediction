# MySportsPrediction
Crawls and predicts the occupancy rate of MySports gyms (like FitStar).

## Initialization
```bash
$ pip3 install -r requirements.txt
```

## Crawler
You can get the `STUDIO_ID` as well as the `X_TENANT` header value by opening any overview page on https://www.mysports.com and analysing the call to https://www.mysports.com/nox/public/v1/studios/.

**Example:**
- https://www.mysports.com/studio/c3BlZWRmaXRuZXNzOjEyMTcxMjAxOTA%3D
- API call (`Chrome -> F11 -> Network`):
  ```bash
  $ curl 'https://www.mysports.com/nox/public/v1/studios/1217120190' \
  -H 'authority: www.mysports.com' \
  -H 'accept: */*' \
  -H 'accept-language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H ...
  -H 'content-type: application/json' \
  -H 'dnt: 1' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H ...
  -H 'x-nox-client-type: WEB' \
  -H 'x-nox-web-context;' \
  -H 'x-tenant: speedfitness' \
  --compressed
- `STUDIO_ID`: `1217120190`
- `X_TENANT`: `speedfitness`

**Running**
```bash
$ cd crawler/
$ python3 main.py
```
This will crawl the studio's occupancy rate once a minute and save the data in `crawler/data.csv`

## Prediction
```bash
$ cd prediction/
$ python3 main.py
```
![image](https://user-images.githubusercontent.com/54217818/230766384-f8e29119-5a2d-445c-be61-00fa07b5499a.png)
