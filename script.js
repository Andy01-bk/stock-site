const socket = io();
const statusEl = document.getElementById("status");

socket.on("connect", () => {
  statusEl.textContent = "Live";
  statusEl.className = "status online";
});

socket.on("disconnect", () => {
  statusEl.textContent = "Offline";
  statusEl.className = "status offline";
});

socket.on("price_update", (quotes) => {
  quotes.forEach((stock) => {
    const row = document.getElementById(`row-${stock.symbol}`);
    if (!row) return;

    const ltpCell = row.querySelector(".ltp");
    const changeCell = row.querySelector(".change");
    const pChangeCell = row.querySelector(".pchange");
    const volumeCell = row.querySelector(".volume");

    const direction = stock.change >= 0 ? "up" : "down";
    const arrow = stock.change >= 0 ? "▲" : "▼";

    ltpCell.textContent = stock.ltp.toFixed(2);
    changeCell.textContent = `${arrow} ${stock.change}`;
    changeCell.className = `change ${direction}`;
    pChangeCell.textContent = `${stock.pChange}%`;
    pChangeCell.className = `pchange ${direction}`;
    volumeCell.textContent = stock.volume.toLocaleString("en-IN");

    row.classList.add("flash");
    setTimeout(() => row.classList.remove("flash"), 600);
  });
});
