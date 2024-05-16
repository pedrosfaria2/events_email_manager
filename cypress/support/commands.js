// cypress/support/commands.js

Cypress.Commands.add('fillEventForm', (event) => {
  cy.get('#title').type(event.title);
  cy.get('#description').type(event.description);
  cy.get('#date').type(event.date);
  if (event.startTime) {
      cy.get('#start-time').type(event.startTime);
  }
  if (event.endTime) {
      cy.get('#end-time').type(event.endTime);
  }
  if (event.recurrence) {
      cy.get('#recurrence').type(event.recurrence);
  }
  if (event.allDay) {
      cy.get('#all-day').check();
  }
});

Cypress.Commands.add('submitEventForm', () => {
  cy.get('#event-form').submit();
});

Cypress.Commands.add('filterEvents', (startDate, endDate) => {
  cy.get('#start-date').type(startDate);
  cy.get('#end-date').type(endDate);
  cy.get('#filter-form').submit();
});

Cypress.Commands.add('verifyModalVisible', () => {
  cy.get('#eventsModal').should('be.visible');
});

Cypress.Commands.add('verifyEventsInTable', (count) => {
  cy.get('#events-table tbody tr').should('have.length', count);
});
