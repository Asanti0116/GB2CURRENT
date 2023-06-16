const quotes = [
  "Believe you can and you're halfway there. -Theodore Roosevelt",
  'You are never too old to set another goal or to dream a new dream. -C.S. Lewis',
  'Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle. -Christian D. Larson',
  'The only way to do great work is to love what you do. -Steve Jobs',
  'Success is not final, failure is not fatal: It is the courage to continue that counts. -Winston S. Churchill',
  "I can't change the direction of the wind, but I can adjust my sails to always reach my destination. -Jimmy Dean",
  "Don't watch the clock; do what it does. Keep going. -Sam Levenson",
  'What you get by achieving your goals is not as important as what you become by achieving your goals. -Zig Ziglar',
  'Believe in the power of your dreams and the rest will follow. -Unknown',
  "You miss 100% of the shots you don't take. -Wayne Gretzky",
];

// function to create a new Quote
function newQuote() {
	let randomNumber = Math.floor(Math.random() * (quotes.length));
  document.getElementById('quoteDisplay').innerHTML = quotes[randomNumber];
}



