import daemon
from main import main


context = daemon.DaemonContext()
context.files_preserve = [open('config.ini', 'r')]

if __name__ == '__main__':
    with daemon.DaemonContext():
        main()
