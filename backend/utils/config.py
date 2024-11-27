import os


def check_env_variables():
    env_vars: list[str] = [
        "OPENAI_API_KEY",
        "OPENAI_ASSISTANT_ID",
        "OPENAI_THREAD_ID",
        "GOOGLE_MAPS_API_KEY",
        "LINE_CLIENT_ID",
        "LINE_CLIENT_SECRET",
        "PINATA_API_KEY",
        "PINATA_SECRET_API_KEY",
        "NFT_ACCOUNT_ADDRESS",
        "NFT_PRIVATE_KEY",

    ]
    missing_vars = [var for var in env_vars if os.getenv(var) is None]
    if missing_vars:
        raise EnvironmentError(
            f"Missing environment variables: {', '.join(missing_vars)}"
        )


def get_openai_api_key() -> str | None:
    return os.getenv("OPENAI_API_KEY")


def get_openai_assistant_id() -> str | None:
    return os.getenv("OPENAI_ASSISTANT_ID")


def get_openai_thread_id() -> str | None:
    return os.getenv("OPENAI_THREAD_ID")


def get_google_maps_api_key() -> str | None:
    return os.getenv("GOOGLE_MAPS_API_KEY")

def get_line_client_id() -> str | None:
    return os.getenv("LINE_CLIENT_ID")

def get_line_secret() -> str | None:
    return os.getenv("LINE_CLIENT_SECRET")

def get_pinata_api_key() -> str | None:
    return os.getenv("PINATA_API_KEY")

def get_pinata_secret_api_key() -> str | None:
    return os.getenv("PINATA_SECRET_API_KEY")

def get_nft_acount_address() -> str | None:
    return os.getenv("NFT_ACCOUNT_ADDRESS")

def get_nft_private_key() -> str | None:
    return os.getenv("NFT_PRIVATE_KEY")








