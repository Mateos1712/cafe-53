const apiUrl = (window.CAFE53_CONFIG?.apiUrl || "").replace(/\/$/, "");
const statusElement = document.querySelector("#api-status");
const form = document.querySelector("#order-form");
const result = document.querySelector("#result");
const ordersList = document.querySelector("#orders-list");
const refreshOrdersButton = document.querySelector("#refresh-orders");

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

function formatDate(value) {
  if (!value) return "Sin fecha";
  return new Intl.DateTimeFormat("es-MX", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(value));
}

function renderOrders(orders) {
  if (!orders.length) {
    ordersList.innerHTML = '<p class="empty-state">Todavía no hay órdenes.</p>';
    return;
  }

  ordersList.innerHTML = orders.map((order) => `
    <article class="order-row">
      <div>
        <strong>${order.item || "Pedido de café"}</strong>
        <span>${order.size || "—"} · ${formatDate(order.createdAt)}</span>
      </div>
      <span class="order-status order-status--${(order.status || "unknown").toLowerCase()}">
        ${order.status || "UNKNOWN"}
      </span>
    </article>
  `).join("");
}

async function loadOrders() {
  if (!apiUrl) return;
  refreshOrdersButton.disabled = true;
  try {
    const response = await fetch(`${apiUrl}/orders`);
    if (!response.ok) throw new Error("No se pudo cargar el historial");
    const body = await response.json();
    renderOrders(body.orders || []);
  } catch (error) {
    ordersList.innerHTML = `<p class="empty-state">${error.message}</p>`;
  } finally {
    refreshOrdersButton.disabled = false;
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
    await loadOrders();
    form.reset();
  } catch (error) {
    result.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});

refreshOrdersButton.addEventListener("click", loadOrders);
checkHealth();
loadOrders();

