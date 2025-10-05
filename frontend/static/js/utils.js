const $ = (sel, root=document) => root.querySelector(sel);

function toast(message, danger=false){
  const t = $("#toast");
  if(!t) return;
  t.textContent = message;
  t.className = "toast" + (danger ? " danger" : "");
  requestAnimationFrame(() => t.classList.add("show"));
  setTimeout(() => t.classList.remove("show"), 2200);
}

function formToJSON(form){
  const data = {};
  new FormData(form).forEach((v,k)=> data[k]=v);
  return data;
}

async function api(path, opts={}){
  const options = {
    method: 'GET',
    credentials: 'include',
    headers: {'Content-Type':'application/json'},
    ...opts
  };
  const res = await fetch(API_BASE + path, options);
  let body = null;
  try { body = await res.json(); } catch { /* maybe empty */ }
  if(!res.ok){
    const msg = (body && (body.error || body.message)) || res.statusText;
    throw new Error(msg);
  }
  return body;
}

// Fill auth badge on every page
(async function hydrateAuthBadge(){
  const badge = $("#authBadge");
  if(!badge) return;
  try{
    const me = await api('/auth/me');
    badge.innerHTML = `Signed in as <strong>${me.email || 'user'}</strong> <button id="logoutBtn" title="Logout">Logout</button>`;
    $("#logoutBtn")?.addEventListener('click', async () => {
      try { await api('/auth/logout', {method:'POST'}); toast('Logged out'); location.href = 'index.html'; }
      catch(e){ toast(e.message, true); }
    });
  }catch{
    badge.textContent = "Not signed in";
  }
})();
