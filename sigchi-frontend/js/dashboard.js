// dashboard.js
const BASE_URL = 'http://localhost:8000';  // Ajusta la URL si es necesario

// Función para obtener la información del usuario
async function getUserInfo() {
    const token = localStorage.getItem('token');

    if (!token) {
        alert('Please log in first');
        window.location.href = 'index.html';
        return;
    }

    const response = await fetch(`${BASE_URL}/api/users/me`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        alert('Failed to fetch user info!');
        return;
    }

    const user = await response.json();
    displayUserInfo(user);
}

// Mostrar la información del usuario y verificar si es admin
function displayUserInfo(user) {
    const userInfoDiv = document.getElementById('userInfo');
    userInfoDiv.innerHTML = `
        <p><strong>ID:</strong> ${user.id}</p>
        <p><strong>Email:</strong> ${user.email}</p>
        <p><strong>Name:</strong> ${user.first_name} ${user.last_name}</p>
        <p><strong>Role:</strong> ${user.role.name}</p>
    `;

    // Mostrar u ocultar botones según el rol
    const role = user.role.name;
    const roleActionsDiv = document.getElementById('roleActions');
    const createUserFormDiv = document.getElementById('createUserFormDiv');

    if (role === 'admin') {
        roleActionsDiv.style.display = 'block';
        createUserFormDiv.style.display = 'block'; // Mostrar formulario de crear usuario
    } else if (role === 'doctor') {
        roleActionsDiv.innerHTML = '<button onclick="goToAppointments()">Manage Appointments</button>';
    } else if (role === 'patient') {
        roleActionsDiv.innerHTML = '<button onclick="goToAppointments()">View My Appointments</button>';
    }
}


// Función para crear un nuevo usuario (solo admin)
async function createUser(event) {
    event.preventDefault();

    const email = document.getElementById('newEmail').value;
    const roleId = document.getElementById('newRoleId').value;  // Obtener role_id desde el dropdown
    const token = localStorage.getItem('token');

    if (!token) {
        alert('No token found. Please log in first!');
        return;
    }

    const response = await fetch(`${BASE_URL}/api/users/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            email: email,
            role_id: parseInt(roleId),  // Convertir role_id a número entero
        }),
    });

    const data = await response.json();

    if (response.ok) {
        document.getElementById('createUserResponse').innerText = 'User created successfully!';
        // Puedes agregar más lógica para limpiar el formulario o redirigir a otra página
    } else {
        document.getElementById('createUserResponse').innerText = `Error: ${data.detail || 'Something went wrong!'}`;
    }
}

// Agregar el evento de submit al formulario de crear usuario
document.getElementById('createUserForm').addEventListener('submit', createUser);


// Llamar a getUserInfo() para cargar la información del usuario y mostrar la interfaz adecuada
getUserInfo();
