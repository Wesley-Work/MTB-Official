import fastapi

# /getToppic
# /getHeaderList
# /getFooterList
# /getBanner

app = fastapi.FastAPI()

@app.get("/getToppic")
def getToppic():
    return {"data": "getToppic"}
