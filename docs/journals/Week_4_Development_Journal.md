# Week 4 Development Journal

## Monday – August 17, 2026

### What did I complete?

- Started the Week 4 development sprint following the completion of the Week 3 frontend integration work.
- Reviewed the existing Flask application, database models, routes, templates, and user/adoption workflows.
- Began Milestone 4.1 focusing on improving the relationship between users, pets, and adoption requests.
- Reviewed and corrected the SQLAlchemy relationships between the `User`, `Pet`, and `AdoptionRequest` models.
- Verified the one-to-many relationship between users and their pets.
- Improved the adoption workflow so that administrators can approve or reject adoption requests.
- Corrected the adoption status workflow so that:
  - Approved requests change the pet status to `Adopted`.
  - Rejected requests change the pet status back to `Available`.
  - The original adoption request remains stored in the database as historical information.
- Added protection to prevent administrators from submitting adoption requests.
- Tested the updated adoption workflow using multiple users and pets.

### What am I working on next?

- Continue testing the updated database relationships and adoption workflow.
- Begin the next Week 4 milestone focusing on additional application pages and functionality.
- Review the navigation bar and complete the remaining navigation features.

### What is blocking me?

- No major blockers. Some adoption-status scenarios required additional testing and correction before the workflow behaved consistently.

---

## Tuesday – August 18, 2026

### What did I complete?

- Completed testing for Milestone 4.1 and confirmed that the updated user, pet, and adoption-request relationships were working correctly.
- Made a logical Git commit after completing and testing the milestone.
- Continued Milestone 4.2 by implementing the **About Us** and **Contact** pages.
- Connected the About Us page to the main navigation bar.
- Connected the Contact page to the main navigation bar.
- Improved the Contact page with a functional "Send Us a Message" form.
- Added a `ContactMessage` database model so submitted contact form information can be stored instead of being discarded.
- Connected contact form submissions to the logged-in user.
- Added a relationship between the contact message and the user who submitted it.
- Updated the Contact form so the logged-in user's identification and email information can be populated from the account instead of requiring duplicate manual entry.
- Added contact message status management for administrators.
- Implemented the **Mark as Read** functionality for contact messages.
- Tested contact form submission and verified that records were successfully stored in the SQLite database.
- Verified that the administrator can view submitted contact messages and mark them as read.

### What am I working on next?

- Continue improving the Admin section.
- Improve the Manage Users functionality.
- Add useful account-management functionality for administrators.
- Continue testing the database relationships and administrative workflows.

### What is blocking me?

- No major blockers. Minor form and database-integration issues were identified during testing and corrected.

---

## Wednesday – August 19, 2026

### What did I complete?

- Continued Week 4 development and administrative feature improvements.
- Improved the Admin Dashboard with navigation to:
  - Add New Pet
  - Manage Pets
  - Manage Users
  - Contact Messages
- Improved the **Manage Pets** page by displaying the user who adopted a pet.
- Ensured that the adopter information remains empty when a pet is still available.
- Verified that approved adoption requests correctly identify the associated adopter.
- Implemented the **Delete User** feature in the Admin Manage Users section.
- Added an Action column to the Manage Users table.
- Prevented administrators from deleting administrator accounts.
- Added confirmation before deleting a user account.
- Tested user deletion using multiple test scenarios.
- Improved the Manage Users page by displaying the number of adoption requests associated with each user.
- Verified that user adoption-request history is associated with the correct user.
- Completed and tested the Week 4 administrative improvements.
- Made a logical Git commit after successfully testing the new functionality.

### What am I working on next?

- Complete final Week 4 testing and cleanup.
- Review all required Deliverable 4 features against the teacher's requirements.
- Complete the project README with setup and usage instructions.
- Review validation, accessibility, responsive design, and error handling.
- Document any remaining known issues.
- Freeze the project scope before the Deliverable 4 demonstration.

### What is blocking me?

- No major blockers.
- Final documentation and verification remain before the Deliverable 4 presentation.

---

## Thursday – August 20, 2026

# Deliverable 4 – Feature-Complete Beta

### What did I complete?

- Completed the major Week 4 development milestones and prepared the project for Deliverable 4.
- Verified that the required application features are implemented and connected to the Flask backend and SQLite database.
- Verified authentication and authorization for normal users and administrators.
- Tested user registration, login, logout, dashboard access, and administrator access.
- Tested the complete pet adoption workflow:
  - Browse pets
  - View pet details
  - Submit adoption request
  - Admin approval
  - Admin rejection
  - Pet status updates
  - User adoption history
- Verified that rejected adoption requests remain stored as historical records while the pet becomes available again.
- Verified that administrators cannot adopt pets through the normal user adoption workflow.
- Verified the User–Pet and User–AdoptionRequest database relationships.
- Completed the About Us and Contact navigation features.
- Verified that Contact form submissions are stored in the database.
- Verified the relationship between contact messages and the logged-in user.
- Tested the administrator Contact Messages page and **Mark as Read** functionality.
- Completed Admin Manage Users functionality.
- Added and tested user deletion.
- Protected administrator accounts from deletion.
- Added adoption-request counts to the Manage Users page.
- Completed Admin Manage Pets improvements, including displaying the adopter for adopted pets.
- Verified that available pets do not display an adopter.
- Reviewed form validation and error handling across major workflows.
- Reviewed responsive layouts using Bootstrap.
- Reviewed accessibility considerations including labels, navigation structure, button text, image `alt` attributes, and readable status indicators.
- Completed the project README draft with setup and usage instructions.
- Reviewed the project for major known issues.
- Confirmed that the project scope is now frozen according to the Deliverable 4 requirements.

### What am I working on next?

- Prepare and rehearse the Deliverable 4 demonstration.
- Review the final Git history and ensure logical commits are present.
- Review the README and setup instructions one final time.
- Prepare to demonstrate authentication, authorization, database relationships, forms, validation, adoption workflow, admin features, and responsive UI.
- After Deliverable 4, focus only on bug fixes, cleanup, and presentation preparation rather than adding major new features.

### What is blocking me?

- No major blockers.
- The project has reached the feature-complete beta stage and is ready for the Deliverable 4 review.
- Any remaining work should be limited to minor bug fixes, documentation updates, testing, and presentation preparation.