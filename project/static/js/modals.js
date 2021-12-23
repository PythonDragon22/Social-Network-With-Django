let signupBox = document.getElementById('signup-box');
let signinBox = document.getElementById('signin-box');
let tweetBox = document.getElementById('tweet-box');

let signupRaiseBtn = document.getElementById('signup-raise-btn');
let signinRaiseBtn = document.getElementById('signin-raise-btn');
let tweetRaiseBtn = document.getElementById('tweet-raise-btn');

let signupCancelBtn = document.getElementById('signup-cancel-btn');
let signinCancelBtn = document.getElementById('signin-cancel-btn');
let tweetCancelBtn = document.getElementById('tweet-cancel-btn');

// popup box
function Raise_Box() {
    signupBox.style.display = 'block';
    signinBox.style.display = 'block';
    tweetBox.style.display = 'block';
}
signupRaiseBtn.onclick = Raise_Box;
signinRaiseBtn.onclick = Raise_Box;
tweetRaiseBtn.onclick = Raise_Box;


// hidden box
function Hide_Box() {
    signupBox.style.display = 'none';
    signinBox.style.display = 'none';
    tweetBox.style.display = 'none';
}
signupCancelBtn.onclick = Hide_Box;
signinCancelBtn.onclick = Hide_Box;
tweetCancelBtn.onclick = Hide_Box;
