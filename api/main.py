from fastapi import FastAPI

# Creat an instance of the class FastAPI
# This will be the same instance referenced by uvicorn in the command "uvicorn main:app --reload"
app = FastAPI()


# GET
@app.get("/")
async def root():
    return {"message": "Main Page"}


app.get("/docs")


async def docs():
    return {"message": "Docs Page"}


app.get("/docs/jupyter")


async def jupyterdocs():
    return {"message": "Jupyter Page"}


app.get("/login")


async def login():
    return {"message": "Login Page"}


app.get("/admin")


async def admin():
    return {"message": "Admin Page"}


app.get("/catalog")


async def catalog():
    return {"message": "Catalog Page"}


app.get("/weaver")


async def weaver():
    return {"message": "Weaver Page"}
