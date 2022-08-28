# Client

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 13.3.7.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.


# UluRecSys 

## Web API

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
if you in the project's root folder
`
cd Client
ng s
`

if you are already in the client dir, you can start the webapi using:
`
cd .. && cd WebApi && uvicorn main:app
`
or for hot reload for development or debugging purpose.
`
cd .. && cd WebApi && uvicorn main:app --reload
`
