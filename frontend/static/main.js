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
                startTimeInput.disabled = true;
                endTimeInput.disabled = true;
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
                        cell.colSpan = 8;
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

                            var actionsCell = row.insertCell(7);
                            actionsCell.classList.add('action-buttons');
                            var editButton = document.createElement('button');
                            editButton.classList.add('btn', 'btn-sm', 'btn-primary', 'edit-event');
                            editButton.innerHTML = '<i class="fas fa-pencil-alt"></i>';
                            editButton.onclick = function () {
                                openEditModal(event);
                            };
                            actionsCell.appendChild(editButton);

                            var deleteButton = document.createElement('button');
                            deleteButton.classList.add('btn', 'btn-sm', 'btn-danger', 'delete-event');
                            deleteButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
                            deleteButton.onclick = function () {
                                deleteEvent(event.id);
                            };
                            actionsCell.appendChild(deleteButton);
                        });
                    }

                    $('#eventsModal').modal('show');
                })
                .catch(error => {
                    console.error('Error fetching events:', error);
                });
        });
    }

    function openEditModal(event) {
        document.getElementById('edit-event-id').value = event.id;
        document.getElementById('edit-title').value = event.title;
        document.getElementById('edit-description').value = event.description;
        document.getElementById('edit-date').value = event.date.split(' ')[0];
        document.getElementById('edit-start-time').value = event.start_time;
        document.getElementById('edit-end-time').value = event.end_time;
        document.getElementById('edit-recurrence').value = event.recurrence;
        document.getElementById('edit-all-day').checked = event.all_day;

        $('#editEventModal').modal('show');
    }

    var editForm = document.getElementById('edit-event-form');
    if (editForm) {
        editForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var eventId = document.getElementById('edit-event-id').value;
            var title = document.getElementById('edit-title').value;
            var description = document.getElementById('edit-description').value;
            var date = document.getElementById('edit-date').value;
            var startTime = document.getElementById('edit-start-time').value;
            var endTime = document.getElementById('edit-end-time').value;
            var recurrence = document.getElementById('edit-recurrence').value;
            var allDay = document.getElementById('edit-all-day').checked;

            var updatedEvent = {
                title: title,
                description: description,
                date: date,
                startTime: startTime,
                endTime: endTime,
                recurrence: recurrence,
                allDay: allDay
            };

            fetch(`/events/${eventId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedEvent)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                alert('Evento atualizado com sucesso!');
                $('#editEventModal').modal('hide');
                filterForm.submit();  // Recarregar a lista de eventos
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Ocorreu um erro ao atualizar o evento.');
            });
        });
    }

    function deleteEvent(eventId) {
        fetch(`/events/${eventId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Evento excluído com sucesso!');
            filterForm.submit();  // Recarregar a lista de eventos
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Ocorreu um erro ao excluir o evento.');
        });
    }
});
