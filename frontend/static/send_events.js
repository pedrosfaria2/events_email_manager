document.addEventListener('DOMContentLoaded', function () {
    // Função para carregar tags no filtro
    function loadTags() {
        fetch('/events')
            .then(response => response.json())
            .then(events => {
                var tags = new Set();
                events.forEach(event => {
                    event.tags.split(',').forEach(tag => {
                        tags.add(tag.trim());
                    });
                });

                var tagSelect = document.getElementById('tag');
                tagSelect.innerHTML = '<option value="">Todas</option>'; // Resetando as opções
                tags.forEach(tag => {
                    if (tag) { // Ignorar tags vazias
                        var option = document.createElement('option');
                        option.value = tag;
                        option.textContent = tag;
                        tagSelect.appendChild(option);
                    }
                });
            })
            .catch(error => {
                console.error('Erro ao buscar tags:', error);
            });
    }

    // Função para carregar eventos na tabela de enviar eventos
    function loadSendEvents(tag, startDate, endDate) {
        var eventsTableBody = document.getElementById('events-table').getElementsByTagName('tbody')[0];
        eventsTableBody.innerHTML = ''; // Limpar tabela antes de recarregar

        fetch('/events')
            .then(response => response.json())
            .then(events => {
                // Filtragem dos eventos
                if (tag) {
                    events = events.filter(event => event.tags.split(',').map(t => t.trim()).includes(tag));
                }
                if (startDate) {
                    events = events.filter(event => new Date(event.date) >= new Date(startDate));
                }
                if (endDate) {
                    events = events.filter(event => new Date(event.date) <= new Date(endDate));
                }

                events.forEach(event => {
                    var row = eventsTableBody.insertRow();

                    var selectCell = row.insertCell(0);
                    var checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.value = event.id;
                    selectCell.appendChild(checkbox);

                    row.insertCell(1).textContent = event.title;
                    row.insertCell(2).textContent = event.description.length > 50 ? event.description.substring(0, 30) + '...' : event.description; // Limitar descrição a 30 caracteres
                    row.insertCell(3).textContent = event.date;
                    row.insertCell(4).textContent = event.startTime || 'N/A';
                    row.insertCell(5).textContent = event.endTime || 'N/A';
                    row.insertCell(6).textContent = event.tags || 'N/A';
                });
            })
            .catch(error => {
                console.error('Erro ao buscar eventos:', error);
            });

        var form = document.getElementById('send-events-form');
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            var selectedEvents = [];
            var checkboxes = document.querySelectorAll('#events-table input[type="checkbox"]:checked');
            checkboxes.forEach(checkbox => {
                selectedEvents.push(checkbox.value);
            });

            if (selectedEvents.length === 0) {
                alert('Por favor, selecione pelo menos um evento para enviar.');
                return;
            }

            fetch('/send_events', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ event_ids: selectedEvents })
            })
            .then(response => response.json())
            .then(data => {
                if (!data.events || data.events.length === 0) {
                    throw new Error('Nenhum evento retornado.');
                }

                console.log('Sucesso:', data);

                // Criar o conteúdo do email
                var emailBody = `Dear Client,\n\nWe would like to inform you about the following events at B3:\n\n`;
                
                data.events.forEach(event => {
                    emailBody += `- ${event.title} on ${event.date} from ${event.startTime} to ${event.endTime}\n  Description: ${event.description}\n\n`;
                });

                emailBody += `Best regards and good trading,\n\nHFT Team of Nova Futura Investimentos.`;

                // Abrir o cliente de email com o conteúdo gerado
                var mailto_link = `mailto:?subject=${encodeURIComponent('Important B3 Events')}&body=${encodeURIComponent(emailBody)}`;
                window.location.href = mailto_link;
            })
            .catch((error) => {
                console.error('Erro ao enviar os eventos:', error);
                alert('Ocorreu um erro ao enviar os eventos.');
            });
        });
    }

    // Inicialização da tabela de enviar eventos e tags
    if (document.getElementById('send-events-form')) {
        loadTags();
        loadSendEvents();

        // Adicionando evento de submit ao formulário de filtragem
        var filterForm = document.getElementById('filter-form');
        filterForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var tag = document.getElementById('tag').value;
            var startDate = document.getElementById('start-date').value;
            var endDate = document.getElementById('end-date').value;

            loadSendEvents(tag, startDate, endDate);
        });
    }
});
