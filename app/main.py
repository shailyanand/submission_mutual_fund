"""
This is a Mutual Fund Broker Web Application project
"""
from fastapi import FastAPI # import fastapi
from pydantic import BaseModel # import base model
from userpage.signup import router as users_router # import router
from fetchdata.fetch_data import app as fetch_data_app # import app


app = FastAPI() #create fastapi instance
app.include_router(users_router) # include router
app.include_router(fetch_data_app) # include app





