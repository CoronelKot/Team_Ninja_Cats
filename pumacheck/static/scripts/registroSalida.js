document.addEventListener("DOMContentLoaded", function () {
    const mensaje = document.getElementById("mensaje-salida")?.dataset.mensaje;
    const redirectUrl = document.getElementById("mensaje-salida")?.dataset.redirect;

    if (mensaje && redirectUrl) {
        alert(mensaje);
        window.location.href = redirectUrl;
    }
});
