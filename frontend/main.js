document.addEventListener("DOMContentLoaded", function () {
    const eventForm = document.getElementById('event-form');
    if (eventForm) {
        eventForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(eventForm);
            const data = {
                title: formData.get('title'),
                description: formData.get('description'),
                date: formData.get('date')
            };

            fetch('http://127.0.0.1:5000/events', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                window.location.href = "manage_events.html";
            })
            .catch(error => console.error('Error:', error));
        });
    }

    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(filterForm);
            const startDate = formData.get('start-date');
            const endDate = formData.get('end-date');

            fetch(`http://127.0.0.1:5000/events?start=${startDate}&end=${endDate}`)
            .then(response => response.json())
            .then(data => {
                const eventsList = document.getElementById('events-list');
                eventsList.innerHTML = '';
                data.forEach(event => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${event.title}: ${event.description} on ${event.date}`;
                    eventsList.appendChild(listItem);
                });
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
