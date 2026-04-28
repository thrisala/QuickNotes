document.addEventListener("DOMContentLoaded", loadNotes);

function loadNotes() {
    fetch('/get_notes')
        .then(res => res.json())
        .then(data => {
            let container = document.getElementById("notesContainer");
            container.innerHTML = "";

            data.forEach(note => {
                container.innerHTML += `
                    <div class="note">
                        <h3>${note[1]}</h3>
                        <p>${note[2]}</p>
                        <button class="delete-btn" onclick="deleteNote(${note[0]})">Delete</button>
                    </div>
                `;
            });
        });
}

function addNote() {
    let title = document.getElementById("title").value;
    let content = document.getElementById("content").value;

    fetch('/add_note', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content })
    })
    .then(res => res.json())
    .then(() => {
        document.getElementById("title").value = "";
        document.getElementById("content").value = "";
        loadNotes();
    });
}

function deleteNote(id) {
    fetch(`/delete_note/${id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(() => loadNotes());
}