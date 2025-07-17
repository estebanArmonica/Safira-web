from decouple import config

print(config('POSTGRESQL_NAME'))
print(config('POSTGRESQL_USER'))
print(config('POSTGRESQL_PASSWORD'))
print(config('POSTGRESQL_HOST'))
print(config('POSTGRESQL_PORT'))
