const sortableList2 = document.querySelector(".sortable-pattern");
const items2 = sortableList2.querySelectorAll(".pattern");

items2.forEach(item2 => {
    item2.addEventListener("dragstart", () => {
        // Adding dragging class to item after a delay
        setTimeout(() => item2.classList.add("dragging"), 0);
    });
    // Removing dragging class from item on dragend event
    item2.addEventListener("dragend", () => item2.classList.remove("dragging"));
});

const initSortableList2 = (e) => {
    e.preventDefault();
    const draggingItem2 = document.querySelector(".dragging");
    // Getting all items except currently dragging and making array of them
    let siblings2 = [...sortableList2.querySelectorAll(".pattern:not(.dragging)")];

    // Finding the sibling after which the dragging item should be placed
    let nextSibling2 = siblings2.find(sibling2 => {
        return e.clientY <= sibling2.offsetTop + sibling2.offsetHeight / 2;
    });

    // Inserting the dragging item before the found sibling
    sortableList2.insertBefore(draggingItem2, nextSibling2);
}

sortableList2.addEventListener("dragover", initSortableList2);
sortableList2.addEventListener("dragenter", e => e.preventDefault());