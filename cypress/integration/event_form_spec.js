// cypress/integration/event_form_spec.js

describe('Event Form', () => {
    beforeEach(() => {
      cy.visit('/check_events.html');
    });
  
    it('should display modal when events are fetched', () => {
      cy.get('#start-date').type('2024-01-01');
      cy.get('#end-date').type('2024-12-31');
      cy.get('#filter-form').submit();
  
      cy.wait(500);
  
      cy.get('#eventsModal').should('be.visible');
      cy.get('#events-table tbody tr').should('have.length.at.least', 1);
    });
  });
  