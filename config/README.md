# Contents of Directory

## configuration.yaml

**File containing authentication related data e.g.**
```yaml
client: 'app'
api_key: 'MONGO_DB_PASSWORD'
base_url: 'API_URL'
host_name: 'MONGO_DB_HOST_NAME'
authenticator: 'MONGO_AUTHENTICATOR'
oauth:
  key: 'API_KEY'
  secret: 'API_SECRET'
time_zone: 'YOUR_TIME_ZONE'
# One of the following: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
log_level: 'INFO'
header:
  user_agent: 'USER_AGENT'
  accept_encoding: 'ACCEPT_ENCODING'
  accept: 'ACCEPT'
  accept_language: 'ACCEPT_LANGUAGE'
```

The `timezone` expects a **tz** timezone e.g. `Europe/Amsterdam`, please see [wiki](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for additional examples

