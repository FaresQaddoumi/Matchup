const teamForm = $("#teamForm");
const tbody = $("#teamsTable tbody");

async function loadTeams(){
  try{
    const teams = await api('/teams');
    tbody.innerHTML = teams.map(t => `<tr><td>${t.id}</td><td>${t.name}</td></tr>`).join('');
  }catch(e){ toast(e.message, true); }
}

teamForm?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  try{
    const payload = formToJSON(teamForm);
    await api('/teams', {method:'POST', body: JSON.stringify(payload)});
    teamForm.reset();
    toast('Team created');
    await loadTeams();
  }catch(e){ toast(e.message, true); }
});

loadTeams();
