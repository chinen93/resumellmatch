from src.storage.repositories.user_repo import UserRepo


def main():

    print("Clean")
    # Get all and Delete
    users = UserRepo.get_all_users()
    for user in users:
        print(user)
        UserRepo.delete_user(user.id)

    # Create
    print("Create")
    user_id = UserRepo.create_user(name="Teste", email="teste@test1.com")
    print(user_id)

    # Read
    print("Read")
    user = UserRepo.get_user_by_id(user_id)
    print(user)

    # Update
    print("Update")
    user = UserRepo.update_user(user_id, name="Jane Doe")
    print(user)

    print("Hello World")
