const bodyEl = document.querySelector("#lbTable tbody");

async function loadLeaderboard(){
  try{
    const rows = await api('/leaderboard');
    rows.sort((a,b) =>
      (b.points - a.points) || (b.goal_diff - a.goal_diff) || (b.goals_for - a.goals_for) || a.team.localeCompare(b.team)
    );
    bodyEl.innerHTML = rows.map((r, i) => `
      <tr>
        <td>${i+1}</td>
        <td>${r.team}</td>
        <td><strong>${r.points}</strong></td>
        <td>${r.played}</td>
        <td>${r.wins}</td>
        <td>${r.draws}</td>
        <td>${r.losses}</td>
        <td>${r.goals_for}</td>
        <td>${r.goals_against}</td>
        <td>${r.goal_diff}</td>
      </tr>
    `).join('');
  } catch (e) {
    toast(e.message, true);
  }
}

loadLeaderboard();

