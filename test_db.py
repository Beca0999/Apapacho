from database import init_db, verify_user, create_user
init_db()
print("DB Initialized")
# verify if migration worked, let's create a test user
create_user("test", "test@example.com", "password")
user = verify_user("test@example.com", "password")
print("User Verified:", user)
