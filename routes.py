# Обработчики маршрутов
def handle_routes(path, method, data=None):
    if method == "GET":
        if path == "/":
            return {"message": "Welcome to the backend!"}, 200
        elif path == "/health":
            return {"status": "OK"}, 200
        else:
            return {"error": "Not Found"}, 404

    elif method == "POST":
        if path == "/data":
            return {"received": data}, 200
        else:
            return {"error": "Not Found"}, 404
