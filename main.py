from play_game import main
from sys import argv


def exit_program():
    print("Invalid argument!\n")
    print("Usage: python3 main.py --> player vs player")
    print("Usage: python3 main.py [algorithm] --> player vs algorithm (algorithms: monteCarlo, miniMax, alphaBeta, random)")
    print("Usage: python3 main.py [algorithm] [algorithm]--> algorithm vs algorithm (algorithms: monteCarlo, miniMax, alphaBeta, random)\n")
    print("IMPORTANT: Don't repeat the same algorithm!\n")
    print("Usable arguments: (--terminal/-t) to play on terminal. Default is on GUI.")
    exit()


def start_program(algorithm1=None, algorithm2=None, GUI=True):
    print("Welcome to Connect 4!")
    print("The first to get 4 in a row wins!\n")
    if algorithm1 is None:
        print("Now playing: Player vs Player\n")
        main(algorithm1, algorithm2, GUI)
    elif algorithm2 is None:
        print("Now playing: Player vs " + str(algorithm1) + "\n")
        main(algorithm1, algorithm2, GUI)
    else:
        print("Now playing: " + str(algorithm1) + " vs " + str(algorithm2) + "\n")
        main(algorithm1, algorithm2, GUI)


def verify(argv1=None, argv2=None, argv3=None):
    if argv1 is None:
        start_program()
    elif argv2 is None:
        if argv1 == "--terminal" or argv1 == "-t":
            start_program(GUI=False)
        elif argv1 == "monteCarlo" or argv1 == "miniMax" or argv1 == "alphaBeta" or argv1 == "random":
            start_program(algorithm1=argv1)
        else:
            exit_program()
    elif argv3 is None:
        if argv1 == "monteCarlo" or argv1 == "miniMax" or argv1 == "alphaBeta" or argv1 == "random":
            if argv2 == "--terminal" or argv2 == "-t":
                start_program(algorithm1=argv1, GUI=False)
            elif argv2 == "monteCarlo" or argv2 == "miniMax" or argv2 == "alphaBeta" or argv2 == "random":
                if argv1 == argv2:
                    exit_program()

                start_program(algorithm1=argv1, algorithm2=argv2)

            else:
                exit_program()
        else:
            exit_program()
    else:
        if argv3 == "--terminal" or argv3 == "-t":
            if argv1 == "monteCarlo" or argv1 == "miniMax" or argv1 == "alphaBeta" or argv1 == "random":
                if argv2 == "monteCarlo" or argv2 == "miniMax" or argv2 == "alphaBeta" or argv2 == "random":
                    if argv1 == argv2:
                        exit_program()
                    start_program(algorithm1=argv1, algorithm2=argv2, GUI=False)
                else:
                    exit_program()
            else:
                exit_program()
        else:
            exit_program()


if __name__ == '__main__':
    try:
        len(argv[1])
    except:
        # there is no arguments
        verify()
    else:
        # there is at least one argument
        try:
            len(argv[2])
        except:
            # there is only one argument
            verify(argv1=argv[1])
        else:
            # there is at least two arguments
            try:
                len(argv[3])
            except:
                # there is only two arguments
                verify(argv1=argv[1], argv2=argv[2])
            else:
                # there is at least three arguments
                verify(argv1=argv[1], argv2=argv[2], argv3=argv[3])
