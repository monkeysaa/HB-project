"use strict";
console.log('JS activated!');

// update lesson stuff
// on lose focus, event-handler that tells title to update in the back end

// update component stuff
const add_pdf = () => {
  document.querySelector('#pdf-div').style.display = "block";
  document.querySelector('#pdf-div').innerHTML = "<h2>Add pdf </h2>";
    
  document.querySelector('#pdf-div').innerHTML += 
    "<form action='/component' method='POST' enctype='multipart/form-data'>\
    <input type='file' name='my-file'><input type='submit'></form>";

};

document.querySelector('#add-content').addEventListener('click', () => {
    console.log('Add content tripped.');
    add_pdf();
    }
  );
  
  const edit_title = () => {
    console.log('now editing title.');
    const newTitle = $('new_title').val();
    const title_el = document.querySelector('#title');
    title_el.textContent = newTitle;
  }

//   document.querySelector('#add-pdf').addEventListener('click', () => {
//     console.log('Tried to add add-pdf functionality');
//     }
//   );
  
document.querySelector('#edit_title').addEventListener('click', () => {
    edit_title();
 }
);
