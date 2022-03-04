harbor.http.register("^/ping/?$", fun(~protocol, ~data, ~headers, uri) -> begin
    # For healthcheck
    http.response(protocol=protocol, data="pong")
end)
