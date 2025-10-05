const homeSel = $("#homeTeam");
const awaySel = $("#awayTeam");
const matchForm = $("#matchForm");
const recentTbody = $("#recentMatches tbody");
const recentLocalKey = "recent_matches";

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
  recentTbody.innerHTML = list.map(r => `<tr><td>${r.home}</td><td>${r.home_score} : ${r.away_score}</td><td>${r.away}</td></tr>`).join('');
}

matchForm?.addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{
    const payload = formToJSON(matchForm);
    // Ensure numbers
    payload.home_team_id = Number(payload.home_team_id);
    payload.away_team_id = Number(payload.away_team_id);
    payload.home_score = Number(payload.home_score);
    payload.away_score = Number(payload.away_score);

    // Prevent same-team matches
    if(payload.home_team_id === payload.away_team_id){
      toast("Home and away team must be different", true);
      return;
    }

    await api('/matches', {method:'POST', body: JSON.stringify(payload)});
    toast('Match saved');

    // Store a friendly recent-row (names)
    const homeName = homeSel.options[homeSel.selectedIndex].text;
    const awayName = awaySel.options[awaySel.selectedIndex].text;
    pushRecent({home:homeName, away:awayName, home_score:payload.home_score, away_score:payload.away_score});
    renderRecent();

    matchForm.reset();
    homeSel.selectedIndex = 0; awaySel.selectedIndex = 0;
  }catch(e){ toast(e.message, true); }
});

loadTeamsForSelects();
renderRecent();
