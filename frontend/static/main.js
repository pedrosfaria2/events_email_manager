document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('event-form');
    if (form) {
        var allDayCheckbox = document.getElementById('all-day');
        var startTimeInput = document.getElementById('start-time');
        var endTimeInput = document.getElementById('end-time');

        allDayCheckbox.addEventListener('change', function () {
            if (allDayCheckbox.checked) {
                startTimeInput.value = '09:00';
                endTimeInput.value = '18:00';
            } else {
                startTimeInput.disabled = false;
                endTimeInput.disabled = false;
                startTimeInput.value = '';
                endTimeInput.value = '';
            }
        });

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            var title = document.getElementById('title').value;
            var description = document.getElementById('description').value;
            var date = document.getElementById('date').value;
            var startTime = startTimeInput.value;
            var endTime = endTimeInput.value;
            var recurrence = document.getElementById('recurrence').value;

            var event = {
                title: title,
                description: description,
                date: date,
                startTime: startTime,
                endTime: endTime,
                recurrence: recurrence,
                allDay: allDayCheckbox.checked
            };

            fetch('/events', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(event)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                alert('Evento adicionado com sucesso!');
                form.reset();
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Ocorreu um erro ao adicionar o evento.');
            });
        });
    }

    var filterForm = document.getElementById('filter-form');
    if (filterForm) {
        var eventsTableBody = document.getElementById('events-table').getElementsByTagName('tbody')[0];

        filterForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var startDate = document.getElementById('start-date').value;
            var endDate = document.getElementById('end-date').value;

            fetch(`/events?start=${startDate}&end=${endDate}`)
                .then(response => response.json())
                .then(events => {
                    eventsTableBody.innerHTML = '';

                    if (events.length === 0) {
                        var row = eventsTableBody.insertRow();
                        var cell = row.insertCell(0);
                        cell.colSpan = 7;
                        cell.textContent = 'Nenhum evento encontrado para as datas selecionadas.';
                    } else {
                        events.forEach(event => {
                            var row = eventsTableBody.insertRow();
                            row.insertCell(0).textContent = event.title;
                            row.insertCell(1).textContent = event.description;
                            row.insertCell(2).textContent = event.date;
                            row.insertCell(3).textContent = event.start_time || '';
                            row.insertCell(4).textContent = event.end_time || '';
                            row.insertCell(5).textContent = event.recurrence || '';
                            row.insertCell(6).textContent = event.all_day ? 'Sim' : 'Não';
                        });
                    }

                    $('#eventsModal').modal('show');
                })
                .catch(error => {
                    console.error('Error fetching events:', error);
                });
        });
    }
});
