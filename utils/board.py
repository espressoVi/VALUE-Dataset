import chess
import toml

config_dict = toml.load('config.toml')

class BoardData:
    pass


def main():
    print(config_dict['board'])
    
if __name__ == "__main__":
    main()
