"use strict";
console.log('JS activated!');

// update lesson stuff
// on lose focus, event-handler that tells title to update in the back end

// update component stuff
const add_pdf = () => {
  document.querySelector('#pdf-div').show();
  document.querySelector('#pdf-div').append(`
    <h1>Add pdf</h1>
    <form action='/upload-comp-img' method='post' enctype='multipart/form-data'>
      <input type='pdf' name='my-pdf'>
      <input type='submit'>
    </form>
  `);
};

document.querySelector('#add-content').addEventListener('click', () => {
    add_pdf();
    random2();
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
