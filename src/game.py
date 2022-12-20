import combat
import cyberdao

def start():
    game_is_running = True
    while game_is_running:
        command = input("> ")
        if command == '/e' or command == '/q':
            print('exiting cyberpunk game')
            game_is_running = False
        if command.startswith('/st'):
            match command.split(' '):
                case ['command']:
                    print('Need more values [/st <param>]')
                case ['command', a]:
                    print('..better')
                case _:
                    print('default')