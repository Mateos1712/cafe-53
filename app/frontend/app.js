const apiUrl = (window.CAFE53_CONFIG?.apiUrl || "").replace(/\/$/, "");
const statusElement = document.querySelector("#api-status");
const form = document.querySelector("#order-form");
const result = document.querySelector("#result");

const wait = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

async function waitForReady(orderId) {
  for (let attempt = 0; attempt < 6; attempt += 1) {
    await wait(1500);
    const response = await fetch(`${apiUrl}/orders/${orderId}`);
    if (!response.ok) continue;
    const order = await response.json();
    if (order.status === "READY") return order;
  }
  return null;
}

async function checkHealth() {
  if (!apiUrl) {
    statusElement.textContent = "API pendiente de desplegar";
    return;
  }
  try {
    const response = await fetch(`${apiUrl}/health`);
    statusElement.textContent = response.ok ? "API disponible" : "API con incidencias";
  } catch {
    statusElement.textContent = "API sin conexion";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!apiUrl) {
    result.textContent = "Despliega Terraform para conectar el formulario con AWS.";
    return;
  }

  const button = form.querySelector("button");
  const data = Object.fromEntries(new FormData(form));
  button.disabled = true;
  result.textContent = "Enviando tu pedido por la nube...";

  try {
    const response = await fetch(`${apiUrl}/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.message || "No se pudo crear el pedido");
    result.textContent = `Pedido ${body.orderId} recibido. Esperando preparación...`;
    const completedOrder = await waitForReady(body.orderId);
    result.textContent = completedOrder
      ? `¡${completedOrder.item} listo! Pedido ${body.orderId}: READY.`
      : `Pedido ${body.orderId} recibido. Consulta su estado en unos segundos.`;
    form.reset();
  } catch (error) {
    result.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});

checkHealth();

