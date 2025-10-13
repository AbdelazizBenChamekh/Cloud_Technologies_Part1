from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
import uvicorn

# Create a Starlette application
app = Starlette(debug=True)

# Define a route (a path that users can visit)
@app.route("/")
async def homepage(request):
    return PlainTextResponse("Hello from Project 1!")

# Run the app when executing directly
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001)
