let socket = null;
let currentUser = null;

// Initialize Socket.IO connection
function initSocket() {
    socket = io();
    
    socket.on('connect', function() {
        console.log('WebSocket connected');
    });
    
    socket.on('task_updated', function(data) {
        console.log('Task update received:', data);
        loadTasks();
        loadAnalytics();
    });
    
    socket.on('connected', function(data) {
        console.log(data.message);
    });
}

// Tab switching
function showTab(tab) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const buttons = document.querySelectorAll('.tab-btn');
    
    if (tab === 'login') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        buttons[0].classList.add('active');
        buttons[1].classList.remove('active');
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        buttons[0].classList.remove('active');
        buttons[1].classList.add('active');
    }
}

// Authentication functions
async function register() {
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    
    if (!username || !email || !password) {
        alert('Please fill all fields');
        return;
    }
    
    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, email, password})
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Registration successful! Please login.');
            showTab('login');
            document.getElementById('reg-username').value = '';
            document.getElementById('reg-email').value = '';
            document.getElementById('reg-password').value = '';
        } else {
            alert(data.error || 'Registration failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred');
    }
}

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    if (!username || !password) {
        alert('Please enter username and password');
        return;
    }
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.user;
            document.getElementById('username-display').textContent = currentUser.username;
            document.getElementById('auth-section').style.display = 'none';
            document.getElementById('main-app').style.display = 'block';
            
            initSocket();
            loadTasks();
            loadAnalytics();
        } else {
            alert(data.error || 'Login failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred');
    }
}

async function logout() {
    try {
        await fetch('/api/auth/logout', {method: 'POST'});
        currentUser = null;
        if (socket) {
            socket.disconnect();
        }
        document.getElementById('auth-section').style.display = 'flex';
        document.getElementById('main-app').style.display = 'none';
        document.getElementById('login-username').value = '';
        document.getElementById('login-password').value = '';
    } catch (error) {
        console.error('Error:', error);
    }
}

// Task functions
async function addTask() {
    const title = document.getElementById('task-title').value;
    const description = document.getElementById('task-desc').value;
    const priority = document.getElementById('task-priority').value;
    
    if (!title) {
        alert('Please enter task title');
        return;
    }
    
    try {
        const response = await fetch('/api/tasks/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({title, description, priority, status: 'Pending'})
        });
        
        if (response.ok) {
            document.getElementById('task-title').value = '';
            document.getElementById('task-desc').value = '';
            loadTasks();
            loadAnalytics();
        } else {
            const data = await response.json();
            alert(data.error || 'Failed to add task');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred');
    }
}

async function loadTasks() {
    try {
        const response = await fetch('/api/tasks/');
        const data = await response.json();
        
        if (response.ok) {
            displayTasks(data.tasks);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayTasks(tasks) {
    const tasksList = document.getElementById('tasks-list');
    tasksList.innerHTML = '';
    
    tasks.forEach(task => {
        const taskCard = document.createElement('div');
        taskCard.className = 'task-card';
        taskCard.innerHTML = `
            <h4>${escapeHtml(task.title)}</h4>
            <p>${escapeHtml(task.description || 'No description')}</p>
            <div>
                <span class="task-priority priority-${task.priority}">${task.priority}</span>
                <span class="task-status">${task.status}</span>
            </div>
            <div class="task-actions">
                ${task.status !== 'Completed' ? `<button class="complete-btn" onclick="updateTaskStatus(${task.id}, 'Completed')">Complete</button>` : ''}
                <button class="update-btn" onclick="editTask(${task.id})">Edit</button>
                <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
            </div>
        `;
        tasksList.appendChild(taskCard);
    });
}

async function updateTaskStatus(taskId, status) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({status})
        });
        
        if (response.ok) {
            loadTasks();
            loadAnalytics();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function editTask(taskId) {
    const newTitle = prompt('Enter new title:');
    if (newTitle) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title: newTitle})
            });
            
            if (response.ok) {
                loadTasks();
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

async function deleteTask(taskId) {
    if (confirm('Are you sure you want to delete this task?')) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                loadTasks();
                loadAnalytics();
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

async function loadAnalytics() {
    try {
        const response = await fetch('/api/analytics/dashboard');
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('total-tasks').textContent = data.total_tasks;
            document.getElementById('completed-tasks').textContent = data.completed_tasks;
            document.getElementById('pending-tasks').textContent = data.pending_tasks;
            document.getElementById('completion-rate').textContent = `${Math.round(data.completion_percentage)}%`;
            
            const breakdownDiv = document.getElementById('priority-breakdown');
            breakdownDiv.innerHTML = `
                <h4>Priority Breakdown</h4>
                <p>High: ${data.priority_breakdown.High || 0}</p>
                <p>Medium: ${data.priority_breakdown.Medium || 0}</p>
                <p>Low: ${data.priority_breakdown.Low || 0}</p>
            `;
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Load analytics every 30 seconds
setInterval(loadAnalytics, 30000);