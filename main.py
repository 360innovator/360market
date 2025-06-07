from storage import AzureStorage
from alerts import send_alert


def main():
    storage = AzureStorage()
    send_alert("Azure stack initialized")


if __name__ == "__main__":
    main()
