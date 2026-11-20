// Minimal Chrome DevTools Protocol driver for the TRAE preview browser (127.0.0.1:9222).
// Usage:
//   node cdp.mjs targets
//   node cdp.mjs nav <url>
//   node cdp.mjs eval "<js expression>"
//   node cdp.mjs shot <path>
import fs from "node:fs";

const CDP = "http://127.0.0.1:9222";

async function pickTarget() {
  const list = await (await fetch(`${CDP}/json/list`)).json();
  const pages = list.filter((t) => t.type === "page");
  return (
    pages.find((p) => /16000|:8000|:16000/.test(p.url)) ||
    pages.find((p) => p.url !== "about:blank") ||
    pages[0]
  );
}

function connect(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    let id = 0;
    const pending = new Map();
    ws.addEventListener("open", () => resolve({
      send(method, params = {}) {
        const mid = ++id;
        return new Promise((res, rej) => {
          pending.set(mid, { res, rej });
          ws.send(JSON.stringify({ id: mid, method, params }));
        });
      },
      close: () => ws.close(),
    }));
    ws.addEventListener("error", reject);
    ws.addEventListener("message", (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && pending.has(msg.id)) {
        const { res, rej } = pending.get(msg.id);
        pending.delete(msg.id);
        msg.error ? rej(new Error(JSON.stringify(msg.error))) : res(msg.result);
      }
    });
  });
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const [cmd, ...rest] = process.argv.slice(2);

if (cmd === "targets") {
  const list = await (await fetch(`${CDP}/json/list`)).json();
  for (const t of list) console.log(t.type, "|", t.title, "|", t.url);
} else {
  const target = await pickTarget();
  if (!target) throw new Error("no page target found");
  const c = await connect(target.webSocketDebuggerUrl);

  if (cmd === "nav") {
    await c.send("Page.enable").catch(() => {});
    await c.send("Page.navigate", { url: rest[0] });
    await sleep(1500);
    console.log("navigated:", rest[0]);
  } else if (cmd === "eval") {
    const r = await c.send("Runtime.evaluate", {
      expression: rest.join(" "),
      awaitPromise: true,
      returnByValue: true,
    });
    console.log(JSON.stringify(r.result?.value ?? r.result, null, 2));
  } else if (cmd === "shot") {
    const r = await c.send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(rest[0], Buffer.from(r.data, "base64"));
    console.log("saved:", rest[0]);
  }
  c.close();
}
