from quart import Quart
from refresh_flats import refresh_flats
from get_flats import get_flats

app = Quart('flats')

@app.route("/refresh_flats")
async def refresh_flats_route():
    await refresh_flats()
    return 'Refreshed'

@app.route("/flats")
async def get_flats_route():
    data = await get_flats()
    return data

@app.route("/")
async def dummy():
    return "Refresh service"

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0',port=8080)