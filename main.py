from fastapi import FastAPI,Path,HTTPException,Query
import pandas as pd
import json

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

app=FastAPI()

@app.get("/")
def hello():
    return {'message':'Patient Managment API System'}

@app.get('/about')
def about():
    return {'about':'Fully functional patients data'}

@app.get('/view')
def view():
    data=load_data()
    return pd.DataFrame(data)
    
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of patient in DB',example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="patient ID not found")

@app.get('/sort')
def sort_patient(sort_by:str = Query(...,description='sort on basis of height, name, city'),order:str=Query('asc',description='sort in ascending or descending ordeer')):
    valid_fields=['height','name','city','age']

    if sort_by not in valid_fields:
        raise HTTPException (status_code=400,detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid order select from ['asc','desc']")
    
    data=load_data()
    sort_order=True if (order=='desc') else False
    # sorted_data=sorted(data.values(),key=lambda x:x[sort_by],reverse=sort_order)
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data