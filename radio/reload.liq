SECRET_KEY = {{ settings.SECRET_KEY|liqval }}
DEBUG = {{ settings.DEBUG|liqval }}
SCRIPT_PATH = "/radio/script.liq"
RELOAD_DELAY = 0.5

def reload(~delay=true)
    response = http.get(headers=[("X-Secret-Key", SECRET_KEY)], "http://app:8000/internal/radio/liquidsoap/script/")
    if response.status_code == 200 then
        file.write(data=response, SCRIPT_PATH)
        log("Wrote downloaded script to #{SCRIPT_PATH}. Restarting in #{string_of(RELOAD_DELAY)}s.")
        if DEBUG then
            script_debug = process.read("pygmentize -l ruby #{process.quote(SCRIPT_PATH)} | cat -n")
            print("===== script.liq =====\n#{script_debug}\n======================")
        end
        if delay then
            thread.run(delay=RELOAD_DELAY, restart)
        else
            restart()
        end
        (true, response)
    else
        log("Failed to download script: #{response.status_message}")
        (false, response.status_message)
    end
end

# {# Won't run on jinja2 rendering from app (only on first load)
# Keep trying to reload script on first run
thread.run(every=2.5, { ignore(reload(delay=false)) })
#}
