# Users
Users are managed via the file `backend/core/models/users.py`. This file contains various functions for creating and editing users, as well as the database model.

## Structure
Users are stored in the PostgreSQL table "users". This contains the following columns. Values ​​marked with * are required when creating the user via a constructor:
- **ID (id)***: ID of the user; counts up automatically
- **Username (username)***: User's user name; does not have to be unique
- **Email (email)**: User's email; must be unique
- **Created At (created_at)**: Time the user was created
- **Role (role)**: User's role; default: `user`
- **Verification State (verification)**: User's verification status; `pending`, `done` or `temporarily_rejected`
- **Verification Rejections (verification_rejections)**: How often a user's verification has already been rejected; if greater than 3, the user is temporarily blocked (5 minutes).

## Requests
The following REST requests are related to user creation and management.

### Exists Registration Request