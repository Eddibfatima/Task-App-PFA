const sideMenu = document.querySelector("aside ");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const darkMode = document.getElementById("dark");
const lightMode = document.getElementById("light");

menuBtn.addEventListener("click", () => {
  sideMenu.style.display = "block";
});
closeBtn.addEventListener("click", () => {
  sideMenu.style.display = "none";
});
darkMode.addEventListener("click", function (e) {
  e.preventDefault();
  document.body.classList.add("dark-theme-variables");
});
lightMode.addEventListener("click", function (e) {
  e.preventDefault();
  document.body.classList.remove("dark-theme-variables");
});
