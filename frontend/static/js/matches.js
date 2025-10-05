// static/js/matches.js
const homeSel = $("#homeTeam");
const awaySel = $("#awayTeam");
const matchForm = $("#matchForm");
const recentTbody = $("#recentMatches tbody");
const recentLocalKey = "recent_matches";
const dbTbody = document.querySelector("#dbMatches tbody"); 

async function loadTeamsForSelects(){
  try{
    const teams = await api('/teams');
    const options = teams.map(t => `<option value="${t.id}">${t.name}</option>`).join('');
    homeSel.innerHTML = `<option value="" disabled selected>Select team</option>${options}`;
    awaySel.innerHTML = `<option value="" disabled selected>Select team</option>${options}`;
  }catch(e){ toast(e.message, true); }
}

function pushRecent(row){
  const list = JSON.parse(localStorage.getItem(recentLocalKey) || "[]");
  list.unshift(row);
  localStorage.setItem(recentLocalKey, JSON.stringify(list.slice(0,8)));
}

function renderRecent(){
  const list = JSON.parse(localStorage.getItem(recentLocalKey) || "[]");
  recentTbody.innerHTML = list.map(r =>
    `<tr><td>${r.home}</td><td>${r.home_score} : ${r.away_score}</td><td>${r.away}</td></tr>`
  ).join('');
}


async function loadDbMatches(){
  try{
    const rows = await api('/matches?played=1');
    dbTbody.innerHTML = rows.map(r =>
      `<tr><td>${r.home_team_name}</td><td>${r.home_score} : ${r.away_score}</td><td>${r.away_team_name}</td></tr>`
    ).join('');
  }catch(e){
    console.warn("Could not load matches from DB:", e);
  }
}

matchForm?.addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{
    const form = formToJSON(matchForm);

    const home_team_id = Number(form.home_team_id);
    const away_team_id = Number(form.away_team_id);
    const home_score   = Number(form.home_score);
    const away_score   = Number(form.away_score);

    if (Number.isNaN(home_team_id) || Number.isNaN(away_team_id)) {
      toast("Please select both teams", true); return;
    }
    if (home_team_id === away_team_id) {
      toast("Home and away team must be different", true); return;
    }
    if (Number.isNaN(home_score) || Number.isNaN(away_score) || home_score < 0 || away_score < 0) {
      toast("Scores must be non-negative numbers", true); return;
    }

  
    const created = await api('/matches', {
      method: 'POST',
      body: JSON.stringify({ home_team_id, away_team_id })
    });

    await api(`/matches/${created.id}/result`, {
      method: 'PUT',
      body: JSON.stringify({ home_score, away_score })
    });

   
    const homeName = homeSel.options[homeSel.selectedIndex].text;
    const awayName = awaySel.options[awaySel.selectedIndex].text;
    pushRecent({ home: homeName, away: awayName, home_score, away_score });
    renderRecent();
    toast('Match saved');

    loadDbMatches();

    matchForm.reset();
    homeSel.selectedIndex = 0;
    awaySel.selectedIndex = 0;

  }catch(err){
    toast(err.message || 'Failed to save match', true);
  }
});


loadTeamsForSelects();
renderRecent();
loadDbMatches();

