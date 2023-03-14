/**
 * Support functions to search and browse images from PromptHero.com
 */

const ph_click_image = function() {
    const idx = this.getAttribute("idx");
    const field_index = gradioApp().getElementById("ph_field_index");
    if (field_index.value != idx) {
        field_index.value = idx;
        const ph_image = gradioApp().getElementById("ph_image");
        ph_image.value = this.querySelector("img").getAttribute("src");
        gradioApp().getElementById("ph_but_refresh").click();
    }
}

const ph_current_index = function(data) {
    const field_index = gradioApp().getElementById('ph_field_index');
    const idx = parseInt(field_index.value);
    var width = 512;
    var height = 512;
    let result = Object.keys(data[idx]).map(e => {
        if (e == "Prompt") {
            return `${data[idx][e]}\n`;
        } else if (e == "Negative prompt") {
            return `Negative prompt: ${data[idx][e]}\n`;
        } else if (e == "width") {
            width = data[idx][e];
            return;
        } else if (e == "height") {
            height = data[idx][e];
            return;
        }
        return `${e}: ${data[idx][e]}, `;
    });
    result.push(`Size: ${width}x${height}`);
    return result.join("");
}

document.addEventListener("DOMContentLoaded", function() {
    const mutationObserver = new MutationObserver(function(m) {
        const galleries = gradioApp().querySelectorAll('[id^="field_gallery"]');
        idx = 0;
        galleries.forEach(function(gallery) {
            // get all the items in this gallery and index...
            const items = gallery.querySelectorAll('.gallery-item');
            items.forEach(function(item) {
                // removeEventListener(item, 'click');
                item.addEventListener('click', ph_click_image, true);
                item.setAttribute('idx', idx);
                idx += 1;
            });
        });
    });
    mutationObserver.observe(gradioApp(), { childList:true, subtree:true });
});
