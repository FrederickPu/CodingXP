// task is the string name for the task
function markTask(task, check){
    let index = 0
    for (let a in acheivements){
        if (acheivements[a].includes(task)){
            check ? progress[index]++ : progress[index]--;
            const progressbar = document.getElementById(`ach-${index}`).querySelectorAll("div[class=\"progress-bar\"]")[0]
            progressbar.style = `width:${progress[index] / maxs[index] * 100}%`;
            progressbar.textContent = `${progress[index]}/${maxs[index]}`
        }
        index++;
    }
}
document.addEventListener("DOMContentLoaded", () => {
    // Attach an event listener to all checkboxes
    document.querySelectorAll('input[type="checkbox"]').forEach((checkbox) => {
        checkbox.addEventListener("change", (event) => {
            const clickedId = event.target.id; // Get the ID of the clicked checkbox (e.g., "checkbox-3")
            const documentId = clickedId.replace("checkbox-", ""); // Extract the document ID (e.g., "3")
            const isChecked = event.target.checked; // Determine whether the checkbox is checked
           
            markTask(event.target.parentElement.querySelectorAll("label")[0].textContent, isChecked)

            // Sync all checkboxes with the same document ID
            document.querySelectorAll(`[id="checkbox-${documentId}"]`).forEach((otherCheckbox) =>
                Array.from(otherCheckbox.parentElement.querySelectorAll('input[type="checkbox"]')).map(child => {
                    if (child.checked != isChecked)
                        markTask(child.parentElement.querySelectorAll("label")[0].textContent, isChecked)
                    child.checked = isChecked
            }));
        
            if (!isChecked)
                return
            let curr = checkbox.parentElement
            while (curr?.tagName == "LI") {
                const direct = curr.querySelectorAll('ul')
                if (direct.length != 0 && Array.from(direct[0].querySelectorAll('li')).every((child) => 
                        child.querySelectorAll('input[type="checkbox"]')[0].checked)) {
                    if (!curr.querySelectorAll('input[type="checkbox"]')[0].checked)
                        markTask(curr.querySelectorAll("label")[0].textContent, true)
                    curr.querySelectorAll('input[type="checkbox"]')[0].checked = true
                }
                curr = curr.parentElement.parentElement
            }
        });
    });
});
