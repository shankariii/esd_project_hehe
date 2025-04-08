# esd_project_hehe

## Brew Haven

 Brew Haven is an online coffee application that allows customers to order their favourite drinks on the go. With multiple outlets across Singapore, customers can easily select the nearest location from their current location, streamlining the ordering process and saving valuable time.

## Getting Started
To Run Frontend:
- cd .\my-coffeeshop-app\
- npm install
- npm run dev

To run the backend:
- Run Docker
- Import coffeeShop_database.sql
- cd .\my-coffeeshop-app\Backend\
- docker compose up --build


Create an account on ngrok.com
Install ngrok via Homebrew with the following command:
brew install ngrok

Configure and run by replacing <token> with the AuthToken found on your account:
ngrok config add-authtoken <token>

Start an endpoint: 

* ngrok http 5005 (DrinkMenuAPI)
* ngrok http 5006 (DrinkIngredientAPI)
* ngrok http 5007 (DrinkCustomisationAPI)
* ngrok http 6000 (SendSMSToCompletedOrder)