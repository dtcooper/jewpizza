def mimic_protocol(~rlog=_, ~maxtime=_, arg) =
    [process_uri(extname="wav", "mimic -t #{process.quote(arg)} -o $(output) -voice rms")]
end

add_protocol(static=true ,"mimic", mimic_protocol,
             doc="Generate speech synthesis using mimic. Result may be mono.",
             syntax="mimic:Text to read")
