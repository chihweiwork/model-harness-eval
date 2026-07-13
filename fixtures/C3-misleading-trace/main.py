from config import load_config
from server import Server


def main():
    config = load_config()
    server = Server(config)
    print(server.start())


if __name__ == "__main__":
    main()
