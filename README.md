# Deep Attention and Online Learning for A Hybrid Article Recommendation System
(Hibrit Makale Öneri Sistemine Yönelik Derin Dikkat ve Çevrimiçi Öğrenme).
## Web API

activated conda env:
`source activate {user_home_dir}/anaconda3/envs/{env_name}`

e.g. given:
user_home_dir = /home/ileri
env_name = py9transformers
`source activate /home/ileri/anaconda3/envs/py9transformers`

run app: 
`cd WebAPi && uvicorn main:app --reload`

swaager doc will be running on: http://127.0.0.1:8000/docs

## Angular Frontend

`
cd Client && ng s
`

### Sample Page:
[![Sample page screenshot](src/../Client/src/assets/ulurecsys_screenshot.jpg)]