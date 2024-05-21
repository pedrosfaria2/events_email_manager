function fetchEmails() {
    const startDate = document.getElementById('start_date').value;
    const endDate = document.getElementById('end_date').value;
    const query = document.getElementById('search').value;
    let url = `/email_logs?`;
    if (startDate) {
        url += `start_date=${startDate}&`;
    }
    if (endDate) {
        url += `end_date=${endDate}&`;
    }
    if (query) {
        url += `query=${query}`;
    }
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('email-logs-container');
            container.innerHTML = '';
            data.forEach(log => {
                const div = document.createElement('div');
                div.classList.add('email-log');
                div.innerHTML = `
                    <p>ID: ${log.id}</p>
                    <p>Subject: ${log.subject}</p>
                    <p>Date Sent: ${log.date_sent}</p>
                `;
                div.onclick = () => showEmail(log.id);
                container.appendChild(div);
            });
        });
}

function showEmail(emailId) {
    fetch(`/email_logs/${emailId}`)
        .then(response => response.text())
        .then(html => {
            const modal = document.getElementById('emailModal');
            const content = document.getElementById('email-content');
            content.innerHTML = html;

            // Adicionar botão para enviar email
            const sendButton = document.createElement('button');
            sendButton.textContent = 'Enviar Email';
            sendButton.onclick = () => sendEmail(emailId);
            content.appendChild(sendButton);

            modal.style.display = 'block';
        });
}

function sendEmail(emailId) {
    fetch(`/send_email/${emailId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function closeModal() {
    const modal = document.getElementById('emailModal');
    modal.style.display = 'none';
}
