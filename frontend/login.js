async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const formData = new URLSearchParams();

    formData.append("username", email);
    formData.append("password", password);

    const response = await fetch("https://student-notes-api-a4lm.onrender.com", {

        method: "POST",

        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },

        body: formData

    });

    const data = await response.json();

    if (response.ok) {

        localStorage.setItem("token", data.access_token);

        alert("Login Successful");

        window.location.href = "dashboard.html";

    } else {

        alert(data.detail);

    }

}