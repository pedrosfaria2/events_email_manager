document.addEventListener('DOMContentLoaded', function () {

    // Função para carregar eventos na tabela de checar eventos
    function loadCheckEvents() {
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
                                var descriptionCell = row.insertCell(1);
                                descriptionCell.textContent = event.description.length > 30 ? event.description.substring(0, 50) + '...' : event.description; // Limitar descrição a 30 caracteres
                                row.insertCell(2).textContent = event.date;
                                row.insertCell(3).textContent = event.startTime || 'N/A';
                                row.insertCell(4).textContent = event.endTime || 'N/A';
                                row.insertCell(5).textContent = event.tags || 'N/A';

                                var actionsCell = row.insertCell(6);
                                var editButton = document.createElement('button');
                                editButton.classList.add('btn', 'btn-sm', 'btn-primary', 'edit-event');
                                editButton.innerHTML = '<i class="fa fa-pencil"></i>';
                                editButton.onclick = function () {
                                    openEditModal(event);
                                };
                                actionsCell.appendChild(editButton);

                                var deleteButton = document.createElement('button');
                                deleteButton.classList.add('btn', 'btn-sm', 'btn-danger', 'delete-event');
                                deleteButton.innerHTML = '<i class="fa fa-trash"></i>';
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
            document.getElementById('edit-date').value = event.date;
            document.getElementById('edit-start-time').value = event.startTime;
            document.getElementById('edit-end-time').value = event.endTime;
            document.getElementById('edit-tags').value = event.tags;

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
                var tags = document.getElementById('edit-tags').value;

                var updatedEvent = {
                    title: title,
                    description: description,
                    date: date,
                    startTime: startTime,
                    endTime: endTime,
                    tags: tags
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
    }

    // Inicialização
    if (document.getElementById('filter-form')) {
        loadCheckEvents();
    }
});
