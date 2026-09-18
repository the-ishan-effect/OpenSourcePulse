from api_helper import BASE_URL, github_get, get_rate_limit


def main():
    # Test 1: Check rate limit
    rate_limit = get_rate_limit()

    print("API Helper Test")
    print("=" * 40)
    print("Remaining requests:", rate_limit["remaining"])
    print()

    # Test 2: Fetch ONE known repository
    url = f"{BASE_URL}/repos/python/cpython"

    repository = github_get(url)

    print("Repository test")
    print("-" * 40)
    print("Repository :", repository["full_name"])
    print("Stars      :", repository["stargazers_count"])
    print("Forks      :", repository["forks_count"])
    print("Language   :", repository["language"])
    print("Archived   :", repository["archived"])
    print("Is Fork    :", repository["fork"])


if __name__ == "__main__":
    main()