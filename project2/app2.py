from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
import uvicorn

app = Starlette(debug=True)

@app.route("/")
async def homepage(request):
    return PlainTextResponse("Hello from Project 2!")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8002)

