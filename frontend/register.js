async function register() {

    const email = document.getElementById("email").value;

    const password = document.getElementById("password").value;

    const response = await fetch("https://student-notes-api-a4lm.onrender.com/register", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            email,

            password

        })

    });

    const data = await response.json();

    alert(data.message || data.detail);

    if (response.ok) {

        window.location.href = "index.html";

    }

}