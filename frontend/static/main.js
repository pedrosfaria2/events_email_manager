document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('event-form');
    var editForm = document.getElementById('edit-form');
    var allDayCheckbox = document.getElementById('all-day');
    var startTimeInput = document.getElementById('start-time');
    var endTimeInput = document.getElementById('end-time');
    var currentEventId = null; // Variable to store the ID of the event being edited

    if (allDayCheckbox) {
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
    }

    if (form) {
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

    if (editForm) {
        editForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var title = document.getElementById('edit-title').value;
            var description = document.getElementById('edit-description').value;
            var date = document.getElementById('edit-date').value;
            var startTime = document.getElementById('edit-start-time').value;
            var endTime = document.getElementById('edit-end-time').value;
            var recurrence = document.getElementById('edit-recurrence').value;
            var allDay = document.getElementById('edit-all-day').checked;

            var event = {
                title: title,
                description: description,
                date: date,
                startTime: startTime,
                endTime: endTime,
                recurrence: recurrence,
                allDay: allDay
            };

            fetch(`/events/${currentEventId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(event)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                alert('Evento atualizado com sucesso!');
                editForm.reset();
                $('#editEventModal').modal('hide');
                filterForm.submit(); // Refresh the events list
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Ocorreu um erro ao atualizar o evento.');
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
                            var editIcon = document.createElement('i');
                            editIcon.className = 'fas fa-edit';
                            editIcon.style.cursor = 'pointer';
                            editIcon.addEventListener('click', function () {
                                openEditModal(event);
                            });

                            var deleteIcon = document.createElement('i');
                            deleteIcon.className = 'fas fa-trash';
                            deleteIcon.style.cursor = 'pointer';
                            deleteIcon.style.marginLeft = '10px';
                            deleteIcon.addEventListener('click', function () {
                                deleteEvent(event.id);
                            });

                            actionsCell.appendChild(editIcon);
                            actionsCell.appendChild(deleteIcon);
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
        currentEventId = event.id;
        document.getElementById('edit-title').value = event.title;
        document.getElementById('edit-description').value = event.description;
        document.getElementById('edit-date').value = event.date;
        document.getElementById('edit-start-time').value = event.start_time;
        document.getElementById('edit-end-time').value = event.end_time;
        document.getElementById('edit-recurrence').value = event.recurrence;
        document.getElementById('edit-all-day').checked = event.all_day;

        $('#editEventModal').modal('show');
    }

    function deleteEvent(eventId) {
        if (confirm('Tem certeza de que deseja excluir este evento?')) {
            fetch(`/events/${eventId}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                alert('Evento excluído com sucesso!');
                filterForm.submit();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocorreu um erro ao excluir o evento.');
            });
        }
    }
});
