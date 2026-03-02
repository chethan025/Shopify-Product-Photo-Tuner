from shopify.collections import get_collections

def select_collection():
    collections = get_collections()

    if not collections:
        raise Exception("No collections found.")

    print("\nAvailable Collections:\n")

    for i, col in enumerate(collections):
        print(
            f"{i+1}. {col['title']} "
            f"(ID: {col['id']})"
        )

    while True:
        try:
            choice = int(input("\nSelect collection: ")) - 1

            if 0 <= choice < len(collections):
                return collections[choice]
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Enter a valid number.")