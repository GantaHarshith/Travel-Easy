"""TravelEasy data and local web server."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import json

places = [
    {
        "city": "goa",
        "name": "Goa Beach Resort",
        "type": "Hotel",
        "price": "₹1500/night",
        "rating": "⭐ 4.5",
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945"
    },
    {
        "city": "goa",
        "name": "Sea View Restaurant",
        "type": "Restaurant",
        "price": "Budget Friendly",
        "rating": "⭐ 4.7",
        "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"
    },
    {
        "city": "hyderabad",
        "name": "Royal Palace Hotel",
        "type": "Hotel",
        "price": "₹1200/night",
        "rating": "⭐ 4.3",
        "image": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa"
    },
    {
        "city": "hyderabad",
        "name": "Biryani House",
        "type": "Restaurant",
        "price": "Famous for Biryani",
        "rating": "⭐ 4.8",
        "image": "https://images.unsplash.com/photo-1552566626-52f8b828add9"
    },
    {
        "city": "mumbai",
        "name": "Mumbai Grand Hotel",
        "type": "Hotel",
        "price": "₹1800/night",
        "rating": "⭐ 4.6",
        "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267"
    },
    {
        "city": "mumbai",
        "name": "Marine Drive Cafe",
        "type": "Restaurant",
        "price": "Seafood Special",
        "rating": "⭐ 4.9",
        "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836"
    }
]


def search_place(city):
    """Return places matching a city name."""
    city = city.strip().lower()
    return [place for place in places if city in place["city"]]


class TravelEasyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        request = urlparse(self.path)
        if request.path == "/api/search":
            city = parse_qs(request.query).get("city", [""])[0]
            response = json.dumps(search_place(city)).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)
            return
        super().do_GET()


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parent
    handler = lambda *args, **kwargs: TravelEasyHandler(
        *args, directory=str(project_dir), **kwargs
    )
    server = ThreadingHTTPServer(("localhost", 8000), handler)
    print("TravelEasy is running at http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nTravelEasy server stopped.")
    finally:
        server.server_close()