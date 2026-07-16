const API = "https://student-notes-api-a4lm.onrender.com";

const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "login.html";
}

async function loadNotes() {

    const response = await fetch(API + "/notes", {

        headers: {
            Authorization: `Bearer ${token}`
        }

    });

    const notes = await response.json();

    const notesDiv = document.getElementById("notes");

    notesDiv.innerHTML = "";

    notes.forEach(note => {

        notesDiv.innerHTML += `
            <div style="border:1px solid gray;padding:10px;margin:10px;">
                <h3>${note.title}</h3>
                <p>${note.note}</p>
                <button onclick="deleteNote(${note.id})">Delete</button>
            </div>
        `;

    });

}

async function addNote() {

    const title = document.getElementById("title").value;

    const note = document.getElementById("note").value;

    await fetch(API + "/notes", {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },

        body: JSON.stringify({
            title,
            note
        })

    });

    document.getElementById("title").value = "";
    document.getElementById("note").value = "";

    loadNotes();

}

async function deleteNote(id) {

    await fetch(API + "/notes/" + id, {

        method: "DELETE",

        headers: {
            Authorization: `Bearer ${token}`
        }

    });

    loadNotes();

}

function logout() {

    localStorage.removeItem("token");

    window.location.href = "login.html";

}

loadNotes();