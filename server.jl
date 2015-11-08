using HttpServer
using WebSockets

function decodeMessage( msg )
    bytestring(msg)
end

function base64decode(data)
    Base.HTML() do io
        print(io, """<img src="data:image/png;base64,""")
        print(io, stringmime(MIME"image/png"(), data))
        print(io, "\" />")
    end

    decodePipe = Base64DecodePipe(IOBuffer(encoded_data))
end

wsh = WebSocketHandler() do req, client
    while true
        msg = read(client)
        msg = decodeMessage(msg)
        println("received message $(msg)")
        img = base64decode(msg)
        write(client, "received")
    end
  end

server = Server(wsh)
println("Starting server on port 8088")
run(server, 8088)