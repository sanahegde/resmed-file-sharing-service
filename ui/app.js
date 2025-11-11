const BASE = "http://127.0.0.1:8000";
const $ = (id) => document.getElementById(id);
const fmt = (t) => new Date(t * 1000).toLocaleString();

function toast(msg) {
    const t = $("toast");
    t.textContent = msg;
    t.classList.add("show");
    setTimeout(() => t.classList.remove("show"), 1800);
}

$("btnUpload").addEventListener("click", async () => {
    const f = $("fileInput").files[0];
    const status = $("uploadStatus");
    const out = $("uploadOut");
    out.style.display = "none";
    out.textContent = "";
    status.className = "status muted";
    status.textContent = "";

    if (!f) { status.textContent = "choose a file"; return; }
    if (f.size > 20 * 1024 * 1024) { status.className = "status err"; status.textContent = "file too large"; return; }

    const form = new FormData();
    form.append("file", f);
    status.textContent = "uploading…";

    try {
        const res = await fetch(`${BASE}/upload`, { method: "POST", body: form });
        const txt = await res.text();
        out.textContent = txt;
        out.style.display = "block";
        if (res.ok) {
            status.className = "status ok"; status.textContent = "upload ok";
            toast("Upload successful");
            await refresh();
        } else {
            status.className = "status err"; status.textContent = `upload failed (${res.status})`;
        }
    } catch {
        status.className = "status err"; status.textContent = "network error";
    }
});

$("btnRefresh").addEventListener("click", refresh);

$("btnHealth").addEventListener("click", async () => {
    const s = $("healthOut");
    s.textContent = "checking…";
    try {
        const r = await fetch(`${BASE}/health`);
        s.textContent = await r.text();
    } catch { s.textContent = "error"; }
});

async function refresh() {
    const body = $("filesBody");
    const status = $("listStatus");
    body.innerHTML = "";
    status.textContent = "loading…";
    try {
        const r = await fetch(`${BASE}/files`);
        const data = await r.json();
        status.textContent = `found ${data.length} item(s)`;
        for (const row of data) {
            const tr = document.createElement("tr");
            tr.innerHTML = `
        <td class="mono id" title="${row.id}">${row.id}</td>
        <td class="filename" title="${row.name}">${row.name}</td>
        <td>${row.size.toLocaleString()}</td>
        <td>${fmt(row.uploaded_at)}</td>
        <td><a class="btn" style="padding:6px 10px" href="${BASE}/files/${row.id}" download>Download</a></td>
      `;
            body.appendChild(tr);
        }
    } catch {
        status.textContent = "error";
    }
}
refresh();
