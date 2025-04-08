# esd_project_hehe


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

ngrok http 5005 (DrinkMenuAPI)
ngrok http 5006 (DrinkIngredientAPI)
ngrok http 5007 (DrinkCustomisationAPI)
ngrok http 6000 (SendSMSToCompletedOrder)