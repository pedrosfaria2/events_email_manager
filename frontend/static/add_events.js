document.addEventListener('DOMContentLoaded', function () {
    // Função para adicionar evento
    function addEvent() {
        var form = document.getElementById('event-form');
        if (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();

                var title = document.getElementById('title').value;
                var description = document.getElementById('description').value;
                var date = document.getElementById('date').value;
                var startTime = document.getElementById('start-time').value;
                var endTime = document.getElementById('end-time').value;
                var tags = document.getElementById('tags').value;

                var event = {
                    title: title,
                    description: description,
                    date: date,
                    startTime: startTime,
                    endTime: endTime,
                    tags: tags
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
    }
    // Inicialização
    if (document.getElementById('send-events-form')) {
        loadSendEvents();
    }

    if (document.getElementById('filter-form')) {
        loadCheckEvents();
    }

    if (document.getElementById('event-form')) {
        addEvent();
    }
});
