// use str.replace() to substitute

var str = 'regexes are awesome';
console.log(str.replace(/awesome/, 'amazing'));
console.log(str.replace(/e/g, 'E'));
console.log(str.replace(/^(\w+)/, "$1 --$1--"));
console.log(str.replace(/^(\w+)/, function (s) { return s.toUpperCase(); }));
