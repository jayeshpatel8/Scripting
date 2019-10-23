// match.js

// use str.match() to match a regex

var str = 'hello, world!';
if (str.match(/(.)\1/)) {
    console.log('MATCH 1!');
}

if (str.match(/^\w+,\s\w+!$/)) {
    console.log('MATCH 2!');
}

// for all of PCRE
// npm install xregexp
var XRegExp = require('xregexp');
var re = XRegExp("                      \
        ^      # begin the string       \
        \\w+   # one or more word chars \
        ,      # comma                  \
        \\s    # a space                \
        \\w+   # one or more word chars \
        !      # exclamation point      \
        $      # end the string         \
        ",'x');

if (str.match(re)) {
    console.log('MATCH 3!');
}

// can also use re.text to match
if (re.test(str)) {
    console.log('MATCH 4!');
}
