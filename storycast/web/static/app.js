const topicInput = document.querySelector("#topic");
const form = document.querySelector("#storycast-form");
const statusList = document.querySelector("#status-list");
const statusPill = document.querySelector("#status-pill");
const resultEmpty = document.querySelector("#result-empty");
const resultContent = document.querySelector("#result-content");
const resultVideo = document.querySelector("#result-video");
const resultSummary = document.querySelector("#result-summary");
const sceneGrid = document.querySelector("#scene-grid");

document.querySelectorAll(".chip").forEach((button) => {
  button.addEventListener("click", () => {
    topicInput.value = button.dataset.example;
    topicInput.focus();
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  resetView();

  const topic = topicInput.value.trim();
  if (!topic) {
    return;
  }

  const response = await fetch("/api/storycasts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic }),
  });

  const payload = await response.json();
  statusPill.textContent = payload.status;
  renderMessages(payload.messages || []);
  pollJob(payload.job_id);
});

async function pollJob(jobId) {
  const response = await fetch(`/api/storycasts/${jobId}`);
  const payload = await response.json();
  statusPill.textContent = payload.status;
  renderMessages(payload.messages || []);

  if (payload.status === "completed") {
    renderResult(payload);
    return;
  }

  if (payload.status === "failed") {
    appendMessage(payload.error || "StoryCast failed.");
    return;
  }

  window.setTimeout(() => pollJob(jobId), 2200);
}

function renderMessages(messages) {
  statusList.innerHTML = "";
  messages.forEach((message) => appendMessage(message));
}

function appendMessage(message) {
  const item = document.createElement("li");
  item.textContent = message;
  statusList.appendChild(item);
}

function renderResult(payload) {
  const manifest = payload.manifest;
  resultEmpty.classList.add("hidden");
  resultContent.classList.remove("hidden");
  resultVideo.src = payload.final_video_url;

  const blueprint = manifest.blueprint;
  resultSummary.innerHTML = `
    <strong>${blueprint.title}</strong><br />
    ${blueprint.logline}<br /><br />
    <strong>Style:</strong> ${blueprint.visual_style_bible}
  `;

  sceneGrid.innerHTML = "";
  manifest.scenes.forEach((scene) => {
    const card = document.createElement("article");
    card.className = "scene-card";
    card.innerHTML = `
      <h3>Scene ${scene.scene_index}: ${scene.title}</h3>
      <p>${scene.duration_seconds}s of narration-led animation.</p>
    `;
    sceneGrid.appendChild(card);
  });
}

function resetView() {
  statusList.innerHTML = "";
  resultEmpty.classList.remove("hidden");
  resultContent.classList.add("hidden");
  resultVideo.removeAttribute("src");
  resultSummary.innerHTML = "";
  sceneGrid.innerHTML = "";
}
