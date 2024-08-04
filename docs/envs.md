# Environments
Daytistics uses different .env files in the backend for production, development & testing. These files are stored under `backend/envs`. The production and development environment is loaded through `backend/.env`. Only the current environment is stored in this file. Loading the test environment is described later.
- **preset.env**: Empty preset for all .env files
- **dev.env**: .env file for development
- **prod.env**: .env file for production
- **testing.env**: .env file for testing

**!!!** When adding a new environment variable in one of the files, please also add it to the other .env files and mark it as `<Not Configured>`.

## App Configuration
Please use Flask's app configuration if possible. Therefore, new environment variables should also be entered into this. This is done in the `config.py` file. If changes are made in this file, the changes should be made to both the `Config` and the `TestConfig` classes.

## Testing
The test environment is loaded automatically when PyTests is executed. If this is not the case, the tests cannot be performed to avoid data loss.

## Current variables
Environment variables marked with * are required. Environment variables marked with * are required. For all other environment variables, **no** change is recommended.

### JSON Web Token
```
*JWT_SECRET_KEY = <OpenSSL Key>
JWT_TOKEN_LOCATION = <headers/cookies/query_string> 
JWT_HEADER_NAME = <Authorization/X-Access-Token> 
JWT_HEADER_TYPE = <Bearer/JWT> 
```

### Database (PostgreSQL)
```
*DATABASE_USER = <String>
*DATABASE_PASSWORD = <String>
*DATABASE_HOST = <IP-Address>
*DATABASE_PORT = <Int>
*DATABASE_NAME = <String>
SQLALCHEMY_DATABASE_URI = <Connection-Address>
SQLALCHEMY_TRACK_MODIFICATIONS = <Boolean>
```

### SMTP Mail Server
```
*MAIL_SERVER = <IP-Address>
*MAIL_PORT = <Int>
*MAIL_USERNAME= <String>
*MAIL_PASSWORD = <String>
*MAIL_USE_TLS = <Boolean> 
*MAIL_USE_SSL = <Boolean> 
```

### Allowed Origins
```
*FRONTEND_IP = <IP-Address>
*BACKEND_IP = <IP-Address>
```