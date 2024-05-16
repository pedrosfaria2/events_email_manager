// cypress/e2e/event_form.cy.js

describe('Event Form', () => {
  beforeEach(() => {
    cy.visit('/check_events.html');
  });

  it('should display modal when events are fetched', () => {
    cy.filterEvents('2024-01-01', '2024-12-31');

    // Adicionar uma espera explícita mais longa e logs
    cy.wait(1000); // espera por 1 segundo (ajuste conforme necessário)
    cy.log('Submitted the filter form');

    cy.verifyModalVisible();
    cy.verifyEventsInTable(1);
  });
});
