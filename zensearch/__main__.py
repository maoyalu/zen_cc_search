from zensearch.database import *


def main():
    """Entry point for the application script"""
    print("Call your main application code here")

if __name__ == '__main__':
    db = Database()
    db.init()
    print(db.search_user_id(1))