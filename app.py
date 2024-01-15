from quart import Quart
from refresh_flats import refresh_flats

app = Quart('flats')

@app.route("/refresh_flats")
async def refresh_flats_route():
    await refresh_flats()
    return 'Refreshed'

if __name__ == "__main__":
    app.run(debug=False)