import Cookies from 'js-cookie';

export function check() {
    let gameOptions = Cookies.get('gameOptions');
    if (gameOptions) {
        return true;
    }
    return false;
}