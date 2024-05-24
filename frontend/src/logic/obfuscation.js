import jscookies from 'js-cookie';

const substitution = {
    'a': 'Q', 'b': 'W', 'c': 'E', 'd': 'R', 'e': 'T', 'f': 'Y', 'g': 'U', 'h': 'I',
    'i': 'O', 'j': 'P', 'k': 'A', 'l': 'S', 'm': 'D', 'n': 'F', 'o': 'G', 'p': 'H',
    'q': 'J', 'r': 'K', 's': 'L', 't': 'Z', 'u': 'X', 'v': 'C', 'w': 'V', 'x': 'B',
    'y': 'N', 'z': 'M', 'A': 'q', 'B': 'w', 'C': 'e', 'D': 'r', 'E': 't', 'F': 'y',
    'G': 'u', 'H': 'i', 'I': 'o', 'J': 'p', 'K': 'a', 'L': 's', 'M': 'd', 'N': 'f',
    'O': 'g', 'P': 'h', 'Q': 'j', 'R': 'k', 'S': 'l', 'T': 'z', 'U': 'x', 'V': 'c',
    'W': 'v', 'X': 'b', 'Y': 'n', 'Z': 'm', '0': '1', '1': '2', '2': '3', '3': '4',
    '4': '5', '5': '6', '6': '7', '7': '8', '8': '9', '9': '0', '{' : '!', '}': '@',
    '[': '#', ']': '$', ';': '%', ':': '^', "'": '&', '"': '*', ',': '(', '.': ')',
};


export function encrypt(plaintext) {
    if (!plaintext) {return};
    let substituted = '';
    for (let char of plaintext) {
        substituted += substitution[char] || char;
    }

    let encrypted = substituted.split('').reverse().join('');
    return encrypted;
}

export function cleartext(str){
    if (!str) {return};
    let reversed = str.split('').reverse().join('');
    let cleartext = '';
    for (let char of reversed) {
        cleartext += Object.keys(substitution).find(key => substitution[key] === char) || char;
    }
    return cleartext;
}

export const Cookies = {
    set: (key, value) => {
        jscookies.set(key, encrypt(value));
    },
    get: (key) => {
        return cleartext(jscookies.get(key));
    },
    remove: (key) => {
        jscookies.remove(key);
    }
}