import ApiService from "./api.js";

const todoInput = document.querySelector(".todo-input input");
const addButton = document.querySelector(".todo-input button");
const todoList = document.querySelector(".todo-list");
const logoutButton = document.getElementById("logout-btn");

function renderTodo(note) {
    const li = document.createElement("li");
    li.className = "todo-item";
    li.dataset.id = note.id;

    li.innerHTML = `
        <span>${note.title}</span>
        <div class="actions">
            <button class="edit-btn">Edit</button>
            <button class="delete-btn">Delete</button>
        </div>
    `;

    li.querySelector(".edit-btn").addEventListener("click", () => handleEdit(note.id, note.title));
    li.querySelector(".delete-btn").addEventListener("click", () => handleDelete(note.id));

    todoList.appendChild(li);
}

async function loadTodos() {
    todoList.innerHTML = "";
    try {
        const notes = await ApiService.getNotes();
        notes.forEach(renderTodo);
    } catch (error) {
        alert("Failed to load todos: " + error.message);
    }
}

async function handleAdd() {
    const title = todoInput.value.trim();
    if (!title) return;

    try {
        await ApiService.createNote(title);
        todoInput.value = "";
        await loadTodos();
    } catch (error) {
        alert("Failed to add todo: " + error.message);
    }
}

async function handleEdit(id, currentTitle) {
    const newTitle = prompt("Edit task:", currentTitle);
    if (!newTitle || newTitle.trim() === "") return;

    try {
        await ApiService.updateNote(id, newTitle.trim());
        await loadTodos();
    } catch (error) {
        alert("Failed to update todo: " + error.message);
    }
}

async function handleDelete(id) {
    if (!confirm("Delete this task?")) return;

    try {
        await ApiService.deleteNote(id);
        await loadTodos();
    } catch (error) {
        alert("Failed to delete todo: " + error.message);
    }
}

function handleLogout() {
    if (!confirm("Are you sure you want to logout?")) return;
    ApiService.logout();
}

// Wire up events
addButton.addEventListener("click", handleAdd);
todoInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") handleAdd();
});
logoutButton.addEventListener("click", handleLogout);

// Auth guard + initial load
document.addEventListener("DOMContentLoaded", async () => {
    const isAuthed = await ApiService.checkAuth();
    if (isAuthed) {
        loadTodos();
    }
});