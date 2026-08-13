# Week 3 Development Journal

## Monday – August 10, 2026

### What did I complete?

- Started the Week 3 frontend integration sprint.
- Connected the frontend pages with the Flask backend and database functionality.
- Implemented and tested the Browse Pets page using real pet records from the SQLite database.
- Connected pet images stored in `static/images` with pet records from the database.
- Implemented the Pet Details page with dynamic pet information.
- Added functional navigation between the Home, Browse Pets, Pet Details, Login, Register, Dashboard, and Admin pages.
- Tested the application using real database records instead of placeholder pet data.

### What am I working on next?

- Continue integrating the adoption workflow between the user interface, Flask routes, and database.
- Improve the visual design and responsiveness of the frontend.
- Continue testing the application from the user's perspective.

### What is blocking me?

- No major blockers. Minor template and routing issues were identified during testing and corrected as development continued.


---

## Tuesday – August 11, 2026

### What did I complete?

- Continued frontend integration and testing of the Pet Adoption Management System.
- Implemented the user adoption workflow from the Pet Details page.
- Added visual status handling for pets:
  - Available
  - Adoption Pending
  - Adopted
- Connected adoption requests to the database so that real request information is displayed.
- Implemented admin adoption request management, including approving and rejecting requests.
- Added successful-action and error feedback using Flask flash messages.
- Tested authentication and access control for normal users and administrators.
- Improved the navigation bar and removed unnecessary or redundant navigation elements.

### What am I working on next?

- Continue improving the user dashboard.
- Refine the Home page and Browse Pets interface.
- Improve the overall visual consistency with the Figma design.
- Test the complete application workflow.

### What is blocking me?

- Minor issues with adoption status display were identified during testing. These were investigated and most of the status-handling issues were resolved.


---

## Wednesday – August 12, 2026

### What did I complete?

- Finalized major frontend integration work for the Week 3 sprint.
- Improved the Home page and connected Featured Pet cards to real database pet records.
- Fixed the View Details links on the Home page.
- Improved the Browse Pets page with search and filtering functionality.
- Implemented pagination so that more than eight pets can be displayed across multiple pages.
- Improved the Pet Details page and made the Adopt button respond correctly to:
  - Available
  - Adoption Pending
  - Adopted
- Implemented Admin Pet Management features:
  - Add Pet
  - Edit Pet
  - Delete Pet
- Improved the User Dashboard with:
  - Account information
  - Adoption summary
  - Adoption request history
  - Request status
  - Pet status
- Simplified the footer and refined the navbar according to the project's design direction.
- Removed unnecessary Login/Register decorative icons and redundant dashboard navigation buttons.
- Tested the application using real users, pets, and adoption requests stored in the database.
- Verified that the main application workflow functions from beginning to end.

### What am I working on next?

- Perform final testing and cleanup before the Week 3 Deliverable 3 presentation.
- Review the application for remaining edge cases.
- Verify that all navigation, validation, feedback, and responsive elements work correctly.
- Prepare the Week 3 presentation and demonstrate the integrated working prototype.

### What is blocking me?

- No major blockers. One minor adoption-status edge case remains under review: ensuring that a rejected request remains associated with the original user while the pet becomes available for other users.


---

## Thursday – August 13, 2026

# Deliverable 3 – Integrated Working Prototype

### What did I complete?

- Completed the Week 3 Integrated Working Prototype.
- Verified that the frontend is connected to the Flask backend and SQLite database.
- Demonstrated real database content through the Home, Browse Pets, Pet Details, User Dashboard, and Admin Dashboard pages.
- Tested the primary workflow from user registration and login through browsing pets, submitting an adoption request, and administrative approval or rejection.
- Verified server-side validation for user and pet-related inputs.
- Tested successful-action feedback and visible error messages.
- Verified navigation across the main application pages.
- Tested the responsive layout using Bootstrap's responsive grid and navigation components.
- Reviewed the interface against the Figma design direction and refined the navbar, footer, cards, buttons, and dashboard.
- Confirmed that major application features no longer depend on hard-coded placeholder data.
- Verified the Admin Pet Management workflow for adding, editing, and deleting pets.
- Verified the Browse Pets pagination functionality for more than eight pets.
- Prepared the project for the Week 3 sprint review and Deliverable 3 presentation.

### What am I working on next?

- Continue with final cleanup and edge-case testing.
- Resolve the remaining adoption-request status scenario where a rejected request must remain associated with the original user while the pet becomes available to other users.
- Review the Git repository and Trello board.
- Prepare for the next Agile sprint and upcoming project requirements.

### What is blocking me?

- No major blockers affecting the integrated prototype.
- A minor adoption workflow edge case remains for final cleanup and can be addressed without affecting the main working prototype.