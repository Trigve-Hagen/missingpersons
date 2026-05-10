
/* document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("prompt-question-button");
  btn.addEventListener("click", () => {
    console.log("Button clicked!");
    const prompt = document.getElementById('prompt-question').value;
    const resDiv = document.getElementById('prompt-response');
    resDiv.innerText = "Thinking...";

    const response = await fetch('/prompt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: prompt })
    });
    const data = await response.json();
    resDiv.innerText = data.response;
  });
});

async function sendMessage() {
  const input = document.getElementById('prompt-question').value;
  console.log(input)
  const response = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: input})
  });
  const data = await response.json();
  document.getElementById('prompt-response').innerHTML += `<p><b>You:</b> ${input}</p>`;
  document.getElementById('prompt-response').innerHTML += `<p><b>AI:</b> ${data.response}</p>`;
} */
