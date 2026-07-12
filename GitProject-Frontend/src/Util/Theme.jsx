export function setTheme(theme) {

    const root = document.documentElement;

    root.classList.remove(
        "dark",
        "dev"
    );

    if (theme !== "light")
        root.classList.add(theme);

    localStorage.setItem("theme", theme);
}

const themes = ["light", "dark"];
export function cycleThemes() {
    const current_theme = localStorage.getItem("theme") || "light";
    console.log("Theme Changed");
    console.log(current_theme);
    const index = themes.indexOf(current_theme);
    setTheme(themes[(index + 1) % themes.length]);
}
