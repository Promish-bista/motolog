# MotoLog Changelog

All notable changes to this project are documented here.

## [v1.5.0] - 2026-07-11
### Added
Password strength indicator on registration page
Trip duration days column on trips list
Trip expense total column on trips list
Trip notes preview on trips list
Last login tracking on user model and profile page
Getting started welcome card for new riders
Total distance and completed trips stat cards
Admin delete for maintenance logs
Maintenance logs stat card on admin dashboard
Footer with module info on all pages
Meta tags for description, author and theme color
Notes column on maintenance log table

### Improved
Input validation on maintenance and expense controllers
Profile page button sizing
Admin dashboard search for users and trips
TESTING.md updated with TC33-TC44

## [v1.3.0] - 2026-07-08
### Added
Expense category breakdown widget on rider dashboard
Live search and filter on expenses list
Password change functionality on profile page
Live search and filter on trips list

## [v1.2.0] - 2026-07-07
### Added
Rider profile page with username and bike model update
Custom 404 error page
Role-based access redirect with flash message
Maintenance service reminder on rider dashboard
Input validation in trip controller
.env.example for secure setup documentation
Manual testing documentation with 32 test cases

## [v1.1.0] - 2026-07-01
### Added
Admin Control Panel with full user, trip and expense management
Role-based access control with @role_required decorator
Controller classes for Auth, Trip, Maintenance, Expense
Admin secret code registration system
Role field added to User model

## [v1.0.0] - 2026-06-29
### Added
Initial project setup with Flask and MySQL
User registration and login with Bcrypt password hashing
Four database models: User, Trip, Maintenance, Expense
Full CRUD routes for all models
Dark theme UI with Safety Orange design system
Jinja2 templates with base.html inheritance
Fuel efficiency calculator
Budget monitor with alerts
Pre-ride safety checklist
Responsive mobile navigation
Git version control setup

## [v1.4.0] - 2026-07-10
### Added
- Getting started welcome card for new riders on dashboard
- Total distance stat card on rider dashboard
- Completed trips counter stat card
- Admin delete functionality for maintenance logs
- Input validation for maintenance controller
- Footer with module information on all pages
- Inline trip status quick-update dropdown
- Admin search for users and trips
- Password change on profile page
- Expense category breakdown on dashboard

### Fixed
- Profile page button sizes
- Removed pycache from version control