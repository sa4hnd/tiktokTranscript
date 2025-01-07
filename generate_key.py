import secrets

# Generate a secure API key
api_key = secrets.token_urlsafe(32)
print("\nYour API Key:")
print("------------------------")
print(api_key)
print("------------------------")
print("\nAdd this to your .env file as:")
print(f'API_KEY="{api_key}"') 