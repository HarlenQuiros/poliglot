import argparse
from upload.drive import get_groups, get_exercises

def drive_group(path):
    get_groups(path + "grupos.xlsx") # Assume the standarized file name


def drive_exercises(path):
    get_exercises(path)


def main():
    parser = argparse.ArgumentParser(description='Welcome to Poliglot')
    
    # Options
    parser.add_argument('-dg', '--drive_group', type=str, 
                        help='Download groups from drive path and upload them to DB.\nThe path must be \"DATOS/year-semester/\".')
    parser.add_argument('-de', '--drive_exercises', type=str, 
                        help='Download exercises from drive path and upload them to DB.\nThe path must be \"DATOS/year-semester/professor full name\".')

    args = parser.parse_args()

    # Cases
    if args.drive_group:
        drive_group(args.drive_group) 
    if args.drive_exercises:
        drive_exercises(args.drive_exercises)

if __name__ == '__main__':
    main()
