// Used in edit-mode of lesson view ("Lesson_Details.html")

"use strict";

console.log('Add_comp activated!');

const add_pdf = () => {
  $('#pdf-div').show();
  $('#pdf-div').append(`
    <h1>Add pdf</h1>
    <form action='/upload-comp-img' method='post' enctype='multipart/form-data'>
      <input type='pdf' name='my-pdf'>
      <input type='submit'>
    </form>
  `);
};

const random2 = () => {
  console.log('test');
};

document.querySelector('#add-content').addEventListener('click', () => {
  add_pdf();
  random2();
  }
);

const edit_title = () => {
  console.log('now edit title.');
}
document.querySelector('#add-pdf').addEventListener('click', () => {
  console.log('Tried to add add-pdf functionality');
  }
);

document.querySelector('#edit_title').addEventListener('click', () => {
  edit_title();
}
);