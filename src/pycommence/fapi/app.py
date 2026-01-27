from fastapi import FastAPI

from .routes import router

app = FastAPI(title='PyCommence FAPI')
app.include_router(router)


@app.get('/global_status')
async def read_root():
    return {'message': 'Welcome to the PyCommence FastAPI!'}
