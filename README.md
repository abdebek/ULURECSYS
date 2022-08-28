#UluRecSys 

##Web API

activated conda env:
`source activate {user_home_dir}/anaconda3/envs/{env_name}`

e.g. given:
user_home_dir = /home/ileri
env_name = py9transformers
`source activate /home/ileri/anaconda3/envs/py9transformers`

run app: 
`uvicorn main:app --reload`

swaager doc will be running on: http://127.0.0.1:8000/docs

## Angular Frontend

`
cd client
ng s
`
