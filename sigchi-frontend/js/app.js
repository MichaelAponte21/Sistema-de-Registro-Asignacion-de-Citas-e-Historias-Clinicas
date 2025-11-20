// app.js
const BASE_URL = 'http://localhost:8000';  // Ajusta la URL si es necesario

async function loginUser(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    const response = await fetch(`${BASE_URL}/api/auth/token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            username: email,
            password: password
        }),
    });

    if (!response.ok) {
        document.getElementById('errorMessage').style.display = 'block';
        return;
    }

    const data = await response.json();
    localStorage.setItem('token', data.access_token);

    // Redirigir a la página de dashboard
    window.location.href = 'dashboard.html';
}

document.getElementById('loginForm').addEventListener('submit', loginUser);
