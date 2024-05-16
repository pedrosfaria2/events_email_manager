describe('Event Form', () => {
    beforeEach(() => {
        // Add an event before each test
        cy.request('POST', '/events', {
            title: 'Initial Event',
            description: 'Initial Description',
            date: '2024-12-31',
            startTime: '10:00',
            endTime: '11:00',
            recurrence: 'weekly',
            allDay: false
        }).then(response => {
            expect(response.status).to.eq(201);
        });

        // Visit the page
        cy.visit('/check_events.html');

        // Filter events for the desired date range
        cy.get('#start-date').type('2024-01-01');
        cy.get('#end-date').type('2024-12-31');
        cy.get('#filter-form').submit();

        // Wait for the events to be fetched and displayed
        cy.wait(1000); // Adjust this value if needed
    });

    it('should display modal when events are fetched', () => {
        cy.get('#eventsModal').should('be.visible');
        cy.get('#events-table tbody tr').should('have.length.at.least', 1);
    });

    it('should edit an event', () => {
        cy.get('#events-table tbody tr').first().find('.edit-event').click();
        cy.get('#edit-title').clear().type('Updated Event');
        cy.get('#edit-description').clear().type('Updated Description');
        cy.get('#edit-event-form').submit();
        cy.wait(20000); // Adjust this value if needed
        cy.get('#events-table tbody tr').should('have.length.at.least', 1);
        cy.get('#events-table tbody tr').first().contains('Updated Event');
        cy.get('#events-table tbody tr').first().contains('Updated Description');
    });

    it('should delete an event', () => {
        cy.get('#events-table tbody tr').first().find('.delete-event').click();
        cy.wait(1000); // Adjust this value if needed
        cy.get('#events-table tbody tr').should('have.length', 0);
    });
});
