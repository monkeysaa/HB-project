// 

const button = document.querySelector('#angry-button');

button.addEventListener('click', () => {
    alert('Stop clicking me!');
});

// To-Do: clean up jQuery / JS conflict
const btn2 = document.querySelector('#file-upload');

btn2.addEventListener('submit', () => {
    $('.upload_form').append($.cloudinary.unsigned_upload_tag("egmnkaly", 
   { cloud_name: 'hackbright' }));
});