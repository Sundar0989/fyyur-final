# Coffee Shop Full Stack

## Link to login
https://udacity-coffee-stack.us.auth0.com/authorize?audience=drinks&response_type=token&client_id=2lu4mLSEou1chqkFS8EcC3dz3WMvjo6n&redirect_uri=http://localhost:8100/tabs/user-page

## Users, Roles & Tokens
### Barista

```
Username - sundarstyles89@gmail.com
Password - #Udacity3
Token - 
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5qMmttY3Zfd0diNkhsbzlRY0pmViJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY29mZmVlLXN0YWNrLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTA5MWZkY2UxNmI5MTAwNmFkNGZiOWQiLCJhdWQiOiJkcmlua3MiLCJpYXQiOjE2MjgwMDY2MTIsImV4cCI6MTYyODAxMzgxMiwiYXpwIjoiMmx1NG1MU0VvdTFjaHFrRlM4RWNDM2R6M1dNdmpvNm4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MtZGV0YWlsIl19.n83o6F9PDm5KicFpDtN730zLnNX7l5wTPtOT50tdWF0fAsKcU-GtmMWk8kW3fEFpv6AcpsxknH0sWK1qyBmfi4YGDNI2yYoDCKkZ_xwUIoJ11Lf8W5Y96D0Rw3SuFOybRvm6fRwILsfSViCxNvE_miA2riV1SAfS3YAvJ2Wn87W6N_hQuZPNDVKbiOhEd1T2OkMg_ZdkzfqcInBk5z-JcRJ-tutvboRdaXauaZTr_oi_gp2Nt02ZpvRy1RxRp0cDgbPQlD0iebcao7Nhf-F6Qn8Sxh_3xKGxEesS4FfhbFUOUMrv6GG9Jc_b05FhI7YlEgzNfDxRSL1y99d8XZlPlw
```

### Manager

```
Username - c.kishore47@gmail.com
Password - #Udacity3
Token - 
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5qMmttY3Zfd0diNkhsbzlRY0pmViJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY29mZmVlLXN0YWNrLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTA5MjA5NDM1ODJiYzAwNjk0N2M5NjgiLCJhdWQiOiJkcmlua3MiLCJpYXQiOjE2MjgwMDY1NTEsImV4cCI6MTYyODAxMzc1MSwiYXpwIjoiMmx1NG1MU0VvdTFjaHFrRlM4RWNDM2R6M1dNdmpvNm4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.D5uhAnsuFQ4riO4aXd0ysIVpSK8fnS6r6SPrZVc8bitV8SIdp_EiTBmSt1Z2mXeIJQtpOZS8gfHyIJAMDoZ0M9JygJYOXem8Y2s4x8a4oRYFX8nwZ4IayNTrlaH-RbMxsy4w7drQYlCbLVC6L37RSPO2-rN-7mHBEpIrSAM89LYBvzNnuRWPLdF8Pz0F1Qy06wmKEUK88iNoZGHmTjtXqhP2QE4bzaXj2EVs7Liwupeo0q945TEQhBGuRmVkSrGgI7brrFuXjW_EwfjtmrxYsxBcippRxP-eKUmIX3k0A2yUlA2h_CoYhUIpnyMi29hVnwo47z-KdkPte4-yvmSdZQ
```


## Full Stack Nano - IAM Final Project

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

You have been called on to demonstrate your newly learned skills to create a full stack drink menu application. The application must:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## Tasks

There are `@TODO` comments throughout the project. We recommend tackling the sections in order. Start by reading the READMEs in:

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. You will need to complete the required endpoints, configure, and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app.

[View the README.md within ./frontend for more details.](./frontend/README.md)
