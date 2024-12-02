from fastapi import FastAPI

app = FastAPI(
    description='Tour Agency'
)


@app.get('/')
def index():
    return {'status': 200}
