document.addEventListener('DOMContentLoaded', function() {
  console.log("JS cargado y DOM listo");
  const btnEliminacion = document.querySelectorAll(".btnEliminacion");
  console.log("Botones encontrados:", btnEliminacion.length);

  btnEliminacion.forEach(btn => {
    btn.addEventListener('click', function(e) {
      console.log("Click detectado en botón de eliminación");
      const confirmacion = confirm("¿Deseas borrar esta materia?");
      if (!confirmacion) {
        e.preventDefault();
        console.log("Eliminación cancelada");
      } else {
        console.log("Eliminación confirmada");
      }
    });
  });
});
