#UluRecSys API

activated conda env:
`source activate {user_home_dir}/anaconda3/envs/{env_name}`

e.g. given:
user_home_dir = /home/ileri
env_name = py9transformers
`source activate /home/ileri/anaconda3/envs/py9transformers`

run app: 
`uvicorn main:app --reload`


## Login Info:
``` curl -i -X POST -F "username=ab@cd.ef" -F "password=abcuiop0" http://localhost:8000/auth/token ```
 return: ```{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqb2huZG9lQGUubWFpbCIsImV4cCI6MTYyMDU3MzgwMn0.Mkzpm6rVC58sUWQC```


if you are already in the WebApi dir, you can start the client using:
`
cd .. && cd Client && ng s
`