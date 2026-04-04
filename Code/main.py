def main():
    pass


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()  # This loads the variables from .env into your system

    name = os.getenv("NAME")
    print(f"Logging in as: {name}")
