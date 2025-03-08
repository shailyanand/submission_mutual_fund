"""
Api to fetch mutual fund data from RapidAPI
API endpoints: /get_fund_family, /get_fund_family_data

"""
from fastapi import APIRouter, HTTPException,Depends
import requests
import sys
sys.path.append('../')

from userpage.signup import get_current_user

app = APIRouter()


def fetch_mutual_fund_data(fund_family):
    url = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"

    if fund_family:
        querystring = {
            "Scheme_Type": "Open",
            "Mutual_Fund_Family": fund_family,
        }
    else:
        querystring = {
            "Scheme_Type": "Open",
        }

    headers = {
	    "x-rapidapi-key": "57ce8c390bmsh39d77222cc206aap1c90e4jsn8755a508669d",
	    "x-rapidapi-host": "latest-mutual-fund-nav.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from RapidAPI")
    return response.json()


@app.get("/get_fund_family")
async def get_fund_family(current_user: dict = Depends(get_current_user)):
    data = fetch_mutual_fund_data()
   
    fund_families = {item['Mutual_Fund_Family'] for item in data if 'Mutual_Fund_Family' in item}
    # background_tasks.add_task(fetch_mutual_fund_data)
    return {"fund_families": list(fund_families)}

@app.get("/get_fund_family_data/{fund_family}")
async def get_fund_family_data(fund_family: str, current_user: dict = Depends(get_current_user)):
    data = fetch_mutual_fund_data()
    fund_data = [item for item in data if item.get('Mutual_Fund_Family') == fund_family]
    return {"fund_data": fund_data}

