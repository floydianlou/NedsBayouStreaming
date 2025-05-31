# NED'S BAYOU STREAMING WEB APP


### 🔹 Custom User Model
- Created `BayouUser` class extending `AbstractUser`
- Added profile fields:
  - Profile picture (with default image)
  - Short biography
  - Phone number
  - Favorite band

### 🔹 Authentication
- Custom user **registration form**
- Custom user **login form**
- Logout system using Django’s built-in `LogoutView`
- After login/logout, users are redirected to the homepage

### 🔹 Templates & Pages
- `home.html` created (global templates folder)
- `register.html` and `login.html` in `users/templates/users/`
- `base.html` prepared for shared header/navigation

### 🔹 Profile Display
- If logged in, the base template shows username and small profile picture
- If not logged in, shows buttons for login and registration