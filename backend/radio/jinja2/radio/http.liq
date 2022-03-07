harbor.http.register("^/reload/?$", fun(~protocol, ~data, ~headers, uri) -> begin
    response = json()

    if headers["X-Secret-Key"] == SECRET_KEY then
        let (success, error_detail) = reload()
        if success then
            response.add("status", "okay")
        else
            response.add("status", "error")
            response.add("error", error_detail)
        end
    else
        response.add("status", "error")
        response.add("error", "Invalid secret key")
    end

    data = json.stringify(response, compact=true)
    http.response(protocol=protocol, content_type='application/json', data=data)
end)

harbor.http.register("^/ping/?$", fun(~protocol, ~data, ~headers, uri) -> begin
    # For healthcheck
    http.response(protocol=protocol, data="pong")
end)
