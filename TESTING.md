# MotoLog — Manual Testing Documentation

## Test Environment
- OS: Windows 10/11
- Browser: Google Chrome
- Python: 3.13.5
- Flask: 3.1.3
- Database: MySQL 8.0

---

## 1. User Authentication Tests

| Test ID | Feature | Steps | Expected Result | Actual Result | Status |
|---------|---------|-------|-----------------|---------------|--------|
| TC01 | User Registration | 1. Go to /register 2. Fill all fields 3. Click Create Account | Account created, redirected to login | Account created successfully |  Pass |
| TC02 | Duplicate Email | 1. Register with existing email | Error: Email already registered | Flash message shown |  Pass |
| TC03 | Duplicate Username | 1. Register with existing username | Error: Username already taken | Flash message shown |  Pass |
| TC04 | User Login | 1. Go to /login 2. Enter valid credentials | Redirected to dashboard | Dashboard loads correctly |  Pass |
| TC05 | Wrong Password | 1. Login with wrong password | Error: Invalid email or password | Flash message shown |  Pass |
| TC06 | Admin Registration | 1. Register with correct admin code | Account created as admin | Redirected to admin panel |  Pass |
| TC07 | Wrong Admin Code | 1. Register with wrong admin code | Account created as rider | Role set to rider |  Pass |
| TC08 | Logout | 1. Click Logout | Redirected to login page | Session cleared correctly |  Pass |

---

## 2. Role-Based Access Control Tests

| Test ID | Feature | Steps | Expected Result | Actual Result | Status |
|---------|---------|-------|-----------------|---------------|--------|
| TC09 | Rider Access Admin | 1. Login as rider 2. Go to /admin | Access denied, redirected to dashboard | Flash message shown |  Pass |
| TC10 | Admin Access Panel | 1. Login as admin 2. View /admin | Admin dashboard loads | All users/trips visible |  Pass |
| TC11 | Unauthenticated Access | 1. Logout 2. Go to / | Redirected to login | Login page shown |  Pass |

---

## 3. Trip Management Tests

| Test ID | Feature | Steps | Expected Result | Actual Result | Status |
|---------|---------|-------|-----------------|---------------|--------|
| TC12 | Create Trip | 1. Go to Trips 2. Click New Trip 3. Fill form 4. Submit | Trip saved and shown in list | Trip appears in table |  Pass |
| TC13 | Empty Trip Form | 1. Submit trip form empty | Validation error shown | Flash error message |  Pass |
| TC14 | Edit Trip | 1. Click Edit on a trip 2. Change status 3. Save | Trip updated | Changes reflected |  Pass |
| TC15 | Delete Trip | 1. Click Delete on a trip 2. Confirm | Trip removed from list | Trip deleted |  Pass |

---

## 4. Maintenance Log Tests

| Test ID | Feature | Steps | Expected Result | Actual Result | Status |
|---------|---------|-------|-----------------|---------------|--------|
| TC16 | Add Service Log | 1. Go to Service 2. Click Add Service 3. Fill form 4. Save | Log saved | Log appears in table |  Pass |
| TC17 | Service Reminder | 1. Add log with next due km 2. Go to dashboard | Reminder shown on dashboard | Yellow reminder card visible |  Pass |
| TC18 | Delete Service Log | 1. Click Delete on log 2. Confirm | Log removed | Log deleted from table |  Pass |

---

## 5. Expense Tracker Tests

| Test ID | Feature | Steps | Expected Result | Actual Result | Status |
|---------|---------|-------|-----------------|---------------|--------|
| TC19 | Add Expense | 1. Go to Expenses 2. Click Add Expense 3. Fill form 4. Save | Expense saved | Expense in table |  Pass |
| TC20 | Link to Trip | 1. Add expense 2. Select a trip | Expense linked to trip | Trip name shown |  Pass |
| TC21 | Budget Alert | 1. Set budget limit 2. Enter amount near limit | Warning shown | Alert message appears |  Pass |
| TC22 | Delete Expense | 1. Click Delete on expense | Expense removed | Deleted from table |  Pass |

---

## 6. Profile Page Tests

| Test ID | Feature | Steps | Expected Result | Actual Result | Status |
|---------|---------|-------|-----------------|---------------|--------|
| TC23 | View Profile | 1. Click Profile in navbar | Profile page loads with user data | All fields populated |  Pass |
| TC24 | Update Profile | 1. Change username 2. Click Save | Profile updated | Changes reflected |  Pass |

---

## 7. Admin Panel Tests

| Test ID | Feature | Steps | Expected Result | Actual Result | Status |
|---------|---------|-------|-----------------|---------------|--------|
| TC25 | View All Users | 1. Login as admin 2. View admin panel | All registered users shown | Users table populated |  Pass |
| TC26 | View All Trips | 1. Login as admin | All trips from all riders shown | Trips with rider names visible |  Pass |
| TC27 | Delete User | 1. Click Delete on a user | User and all their data deleted | User removed from table |  Pass |
| TC28 | Delete Own Account | 1. Try to delete own admin account | Error: Cannot delete own account | Flash error shown |  Pass |

---

## 8. JavaScript Feature Tests

| Test ID | Feature | Steps | Expected Result | Actual Result | Status |
|---------|---------|-------|-----------------|---------------|--------|
| TC29 | Fuel Calculator | 1. Enter km, litres, price | Mileage and cost calculated live | Results shown instantly |  Pass |
| TC30 | Budget Alert JS | 1. Set limit below current spend | Warning alert shown | Alert appears in red |  Pass |
| TC31 | Pre-ride Checklist | 1. Click checklist items | Items toggle done state | Progress bar updates |  Pass |
| TC32 | 404 Page | 1. Go to /randompage | Custom 404 page shown | MotoLog 404 page loads |  Pass |