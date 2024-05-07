prompt("working")
const input = document.getElementById('value');
const progressValue = document.querySelector('.Progressbar__value');
const progress = document.querySelector('progress');

function setValue(value) {
  progressValue.style.width = `${value}%`;
  progress.value = value;
}

setValue(input.value);

input.addEventListener('change', e => {
  const value = e.target.value;
  setValue(value);
});