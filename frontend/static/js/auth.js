const loginForm = $("#loginForm");
const signupForm = $("#signupForm");

loginForm?.addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{
    await api('/auth/login', {method:'POST', body: JSON.stringify(formToJSON(loginForm))});
    toast('Logged in'); location.href='index.html';
  }catch(err){ toast(err.message, true); }
});

signupForm?.addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{
    await api('/auth/signup', {method:'POST', body: JSON.stringify(formToJSON(signupForm))});
    toast('Account created — you can login now');
  }catch(err){ toast(err.message, true); }
});
