from webkit import Server

if __name__ == "__main__":

    # start server
    server = Server("0.0.0.0", 8080, False, "/dev/ttyUSB0")
    server.setDaemon(True)
    server.start()
    server.run_parser()