from src.storage.repositories.user_repo import UserRepo


def main():

    print("Clean")
    # Get all and Delete
    users = UserRepo.get_all()
    for user in users:
        print(user)
        UserRepo.delete(user.id)

    # Create
    print("Create")
    user_id = UserRepo.create(name="Teste", email="teste@test1.com")
    print(user_id)

    # Read
    print("Read")
    user = UserRepo.get_by_id(user_id)
    print(user)

    # Update
    print("Update")
    user = UserRepo.update(user_id, name="Jane Doe")
    print(user)

    print("Hello World")
