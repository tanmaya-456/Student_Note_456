const button = document.getElementById("addBtn");
const notesDiv = document.getElementById("notes");

async function loadNotes() {

    const response = await fetch("http://127.0.0.1:8000/notes");

    const notes = await response.json();

    notesDiv.innerHTML = "";

 notes.forEach(note => {

    notesDiv.innerHTML += `

    <div class="note">

        <h3>${note.title}</h3>

        <p>${note.note}</p>

        <button onclick="deleteNote(${note.id})">

            Delete

        </button>

    </div>

    `;

});

}

button.addEventListener("click", async function () {

    const title = document.getElementById("title").value;

    const note = document.getElementById("note").value;

    await fetch("http://127.0.0.1:8000/notes", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            title,

            note

        })

    });

    document.getElementById("title").value = "";

    document.getElementById("note").value = "";

    loadNotes();

});

loadNotes();

async function deleteNote(id){

    await fetch(`http://127.0.0.1:8000/notes/${id}`,{

        method:"DELETE"

    });

    loadNotes();

}