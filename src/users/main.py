import fastapi as fa
from .routes import router

app = fa.FastAPI()


app.include_router(router)


@app.get('/health-check')
def health_check():
    return {"message": "Everything is ok"}
