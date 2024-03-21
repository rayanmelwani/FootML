# FootML

Built a machine learning platform for the 2020-2021 Fantasy Premier League Season. Worked with Charlie Robertson, Katie Miles, Fraser Ralston & James Rosen. 


## Development

This platform was built using a Flask backend and a simple HTML / CSS frontend with injections of JavaScript. We used a recurrent neural net (RNN) to predict player points for following gameweeks during the 2021-2022 PL season. 

## Data Sources

The data sources for this platform include the [Fantasy Premier League API](https://fpl.readthedocs.io/en/latest/#) and a publicly available FPL data github under the name [vastaav](https://github.com/vaastav/Fantasy-Premier-League).

## Running Locally 

After cloning the repo, create a virtual environment, install the required packages and run flask run from the root directory. These instructions are provided below.
```
python -m venv venv
```
```
pip install -r requirements.txt
```
```
flask run
```

## Functionality

During the 2020-2021 PL season, the premise of this platform was to give transaction advice to FPL players to maximise total points. Users would input their current teams as below.

![image](https://github.com/rayanmelwani/FootML/assets/47063984/de9c4196-c04e-43d8-8f97-628941ab21ef)

Using our ML model's predictions, we would recommend transfers that fit the constraints of their team and the game (cost, position & team constraints).

![image](https://github.com/rayanmelwani/FootML/assets/47063984/4a5673e8-9000-4df5-9e17-f8b446896a25)

Additionally, we allowed users to interact directly with the model's weekly predictions through the format of 'Top players' and 'Search Pages'.

![image](https://github.com/rayanmelwani/FootML/assets/47063984/072d30d0-f45c-472c-8594-913cfa2683fa)

![image](https://github.com/rayanmelwani/FootML/assets/47063984/46f670ca-32d8-4320-bd0a-b3ead1e43aa1)
