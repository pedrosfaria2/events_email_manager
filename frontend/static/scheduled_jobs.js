document.addEventListener("DOMContentLoaded", function() {
  fetchScheduledJobs();
});

async function fetchScheduledJobs() {
  try {
      const response = await fetch('/api/scheduled-jobs');
      const jobs = await response.json();
      console.log('Jobs fetched:', jobs); // Log para depuração
      displayJobs(jobs);
  } catch (error) {
      console.error('Error fetching scheduled jobs', error);
  }
}

function displayJobs(jobs) {
  const jobsContainer = document.getElementById('scheduled-jobs-container');
  jobsContainer.innerHTML = ''; // Limpa o conteúdo anterior
  if (jobs.length > 0) {
      jobs.forEach(job => {
          const jobElement = document.createElement('div');
          jobElement.classList.add('job');
          jobElement.innerHTML = `
              <p>ID: ${job.id}</p>
              <p>Nome: ${job.name}</p>
              <p>Frequência: ${job.frequency}</p>
              <p>Hora: ${job.time}</p>
              <p>Status: ${job.enabled ? 'Enabled' : 'Disabled'}</p>
              <button onclick="toggleJob(${job.id}, ${job.enabled})">
                  ${job.enabled ? 'Disable' : 'Enable'}
              </button>
          `;
          jobsContainer.appendChild(jobElement);
      });
  } else {
      jobsContainer.innerHTML = '<p>No jobs available</p>';
  }
}

async function toggleJob(jobId, enabled) {
  console.log('Toggling job:', jobId, enabled); // Log para depuração
  try {
      const endpoint = enabled ? 'disable' : 'enable';
      const response = await fetch(`/api/scheduled-jobs/${jobId}/${endpoint}`, {
          method: 'POST',
      });
      const result = await response.json();
      console.log('Toggle result:', result); // Log para depuração
      fetchScheduledJobs(); // Recarrega a lista de jobs
  } catch (error) {
      console.error(`Error ${enabled ? 'disabling' : 'enabling'} job`, error);
  }
}
