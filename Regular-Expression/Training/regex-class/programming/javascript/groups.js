// groups.js

var str = 'regexes are awesome';

var result = str.match(/\w+/g);
console.log(result);
console.log(result[0]);
console.log(result[1]);
console.log(result[2]);

console.log('-----');
var result = str.match(/\s(\w+)\s/);
console.log(result);
console.log(result[0]);
console.log(result[1]);
console.log(result.index);
console.log(result.input);

console.log('-----');
var result = str.match(/^(\w+).*\s(\w+)/);
console.log(result);
console.log(result[0]);
console.log(result[1]);
console.log(result[2]);
