class Server:
    def __init__(self, config):
        self.host = config["host"]
        self.port = config["port"]
        self.workers = config["workers"]

    def start(self):
        admin_port = self.port + 1
        return (
            f"Server on {self.host}:{self.port} "
            f"(admin {admin_port}, workers {self.workers})"
        )
